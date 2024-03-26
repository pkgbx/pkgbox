import os
from unittest import mock

import pytest

from pkgbox import env


def test_get_pkgbox_dirs_pkgbox_home_ok(tmpdir):
    env_mock = {
        'PKGBOX_HOME': str(tmpdir)
    }
    cfg = {
        'config_dir': f'{tmpdir}/config',
        'data_dir': f'{tmpdir}/data'
    }

    with mock.patch.dict(os.environ, env_mock):
        paths = env.get_pkgbox_dirs()

    assert paths == cfg


def test_get_pkgbox_dirs_xdg_ok(tmpdir):
    env_mock = {
        'XDG_DATA_HOME': os.path.join(str(tmpdir), 'xdg_data_home'),
        'XDG_CONFIG_HOME': os.path.join(str(tmpdir), 'xdg_config_home')
    }
    cfg = {
        'config_dir': f'{tmpdir}/xdg_config_home/pkgbox',
        'data_dir': f'{tmpdir}/xdg_data_home/pkgbox'
    }

    with mock.patch.dict(os.environ, env_mock):
        paths = env.get_pkgbox_dirs()

    assert paths == cfg


def test_get_pkgbox_dirs_home_ok(tmpdir):
    env_mock = {
        'HOME': f'{tmpdir}/home'
    }
    cfg = {
        'config_dir': f'{tmpdir}/home/.config/pkgbox',
        'data_dir': f'{tmpdir}/home/.local/share/pkgbox'
    }

    with mock.patch.dict(os.environ, env_mock):
        paths = env.get_pkgbox_dirs()

    assert paths == cfg


def test_get_pkgbox_dirs_default_ok(tmpdir):
    env_mock = {}
    cfg = {
        'config_dir': f'/opt/pkgbox/config',
        'data_dir': f'/opt/pkgbox/data'
    }

    with mock.patch.dict(os.environ, {}):
        del os.environ['HOME']
        paths = env.get_pkgbox_dirs()

    assert paths == cfg


def test_ensure_pkgbox_dirs_ok(tmpdir):
    d = tmpdir / 'pkgbox'

    paths = {
        'config_dir': f'{d}/config',
        'data_dir': f'{d}/data'
    }

    env.ensure_pkgbox_dirs(paths)

    assert os.path.exists(f'{d}/config')
    assert os.path.exists(f'{d}/data')


def test_bootstrap_ok(tmpdir):
    d = tmpdir / 'pkgbox'

    paths = {
        'config_dir': f'{d}/config',
        'data_dir': f'{d}/data'
    }

    env.bootstrap(paths)

    assert os.path.exists(f'{d}/config/crun/config.json')
