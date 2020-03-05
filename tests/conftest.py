import pytest
from click.testing import CliRunner

from .utils.helpers import Helpers


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture
def helpers():
    return Helpers
