import os
from unittest import mock

from pkgbox import errors
from pkgbox.cli import cli


def test_ok(clirunner, tmp_path):
    d = tmp_path / 'pkgbox'
    d.mkdir()

    with mock.patch.dict(os.environ, {'PKGBOX_HOME': str(d)}):
        res = clirunner.invoke(cli, ['init'])
    
    expected = '\n'.join([
        f'config_dir: {d}/config',
        f'data_dir: {d}/data',
        ''
    ])

    assert res.exit_code == 0
    assert res.output == expected
