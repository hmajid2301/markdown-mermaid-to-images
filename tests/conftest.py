import pytest
from click.testing import CliRunner

from .utils.helpers import Helpers


@pytest.fixture(scope="module")
def helpers():
    return Helpers


@pytest.fixture(scope="module")
def runner(helpers):
    helpers.remove_files_in_output()
    return CliRunner()
