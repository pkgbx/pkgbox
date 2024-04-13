from unittest import mock

import pytest
import requests_mock

from pkgbox import errors, io


def test_io_reader_file_ok():
    r = io.FileReader('file', '/some_path')

    with mock.patch('builtins.open', mock.mock_open(read_data='foobar')) as m:
        assert r.read() == 'foobar'


def test_io_reader_file_err():
    r = io.FileReader('file', '/some_path')

    with pytest.raises(errors.PBError):
        r.read()


def test_io_reader_http_ok():
    r = io.HttpReader('http', 'www.pkgbox.org/Ccntainerfile')
    with requests_mock.Mocker() as m:
        m.get('http://www.pkgbox.org/Ccntainerfile', text='foobar')
        
        assert r.read() == 'foobar'


def test_io_reader_http_err():
    r = io.HttpReader('http', 'www.pkgbox.org/Ccntainerfile')
    with requests_mock.Mocker() as m, pytest.raises(errors.PBError) as e:
        m.get('http://www.pkgbox.org/Ccntainerfile', status_code=404)
        
        r.read()

        assert e.value.status == 404


@pytest.mark.parametrize('scheme,path,expected', [
    ('file', '/tmp/Containerfile', io.FileReader),
    ('http', 'www.pkgbox.org/Ccntainerfile', io.HttpReader),
    ('https', 'www.pkgbox.org/Ccntainerfile', io.HttpReader),
    ('something_else', '/tmp/Containerfile', io.FileReader)
])
def test_builder_ok(scheme, path, expected):
    r = io.build_reader(scheme, path)

    assert type(r) == expected
