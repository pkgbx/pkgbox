import os

import pytest
from click.testing import CliRunner


@pytest.fixture
def clirunner():
    return CliRunner()


@pytest.fixture
def tmpdir(tmp_path):
    tmp_path.mkdir(exist_ok=True)

    return tmp_path


@pytest.fixture
def fixdir():
    realpath = os.path.realpath(__file__)

    return os.path.join(os.path.dirname(realpath), 'fixtures')


@pytest.fixture
def manifest_json(fixdir):
    with open(f'{fixdir}/manifest.json', 'r') as f:
        return f.read()
