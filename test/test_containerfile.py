import json
import pathlib

from pkgbox import containerfile


def test_parse_simple_ok(fixdir):
    basedir = f'{fixdir}/containerfiles/simple'
    path = pathlib.Path(f'{basedir}/Containerfile')
    parser = containerfile.from_filepath(path)

    assert parser.baseimage == 'registry.fedoraproject.org/fedora:latest'
    assert parser.labels == {
        'org.pkgbox.package.name': 'simple',
        'org.pkgbox.package.version': '0.1.0',
        'org.pkgbox.package.release': '1',
        'org.pkgbox.schema.version': '1',
    }
    with open(f'{basedir}/Containerfile.json', 'r') as f:
        assert json.load(f) == containerfile.as_dict(parser)
