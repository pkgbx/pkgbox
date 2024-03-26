import os
import pathlib

import requests_mock

from pkgbox import image


def test_from_str():
    name = 'registry.fedoraproject.org/fedora:39'
    img = image.from_str(name)

    assert img.registry == 'registry.fedoraproject.org'
    assert img.namespace == 'fedora'
    assert img.tag == '39'
    assert str(img) == name
    assert img == image.Image('registry.fedoraproject.org', 'fedora', '39')


def test_info(manifest_json):
    name = 'registry.fedoraproject.org/fedora:39'
    img = image.from_str(name)

    with requests_mock.Mocker() as m:
        m.get('https://registry.fedoraproject.org/v2/fedora/manifests/39', 
              headers={'docker-content-digest': 'sha256:718a00fe32127ad01ddab9fc4b7c968ab2679c92c6385ac6865ae6e2523275e4'},
              text=manifest_json)
        info = image.info(img)

    assert info.schema_version == 1
    assert info.name == 'fedora'
    assert info.tag == '39'
    assert info.architecture == 'amd64'
    assert len(info.layers) == 1
    assert len(info.history) == 1
    assert len(info.signatures) == 1


def test_fetch(manifest_json, tmp_path):
    dest = tmp_path / 'pkgbox-test'
    dest.mkdir()
    name = 'registry.fedoraproject.org/fedora:39'
    img = image.from_str(name) 

    with requests_mock.Mocker() as m:
        m.get('https://registry.fedoraproject.org/v2/fedora/manifests/39', 
              headers={'docker-content-digest': 'sha256:718a00fe32127ad01ddab9fc4b7c968ab2679c92c6385ac6865ae6e2523275e4'},
              text=manifest_json)
        m.get('https://registry.fedoraproject.org/v2/fedora/blobs/sha256:718a00fe32127ad01ddab9fc4b7c968ab2679c92c6385ac6865ae6e2523275e4', 
              text='')
        # calls
        info = image.info(img)
        image.fetch(img, info, dest)

    for layer in info.layers:
        assert os.path.exists(f'{dest}/{layer.digest}.tar.gz')
