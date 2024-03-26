from pkgbox import errors
from pkgbox.cli import cli


def test_ok(clirunner):
    res = clirunner.invoke(cli, ['build'])
    
    assert res.exception == errors.PBNotImplementedError()
