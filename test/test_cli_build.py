import pathlib

from pkgbox import errors, containerfile
from pkgbox.cli import cli


def test_ok(clirunner, fixdir):
    path = f'{fixdir}/containerfiles/simple/Containerfile'
    parser = containerfile.from_filepath(pathlib.Path(path))
    res = clirunner.invoke(cli, ['build', path])

    assert res.stdout == containerfile.as_json(parser, pretty=True) + '\n'
