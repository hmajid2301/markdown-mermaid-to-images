import shutil
import subprocess

import pytest

from markdown_mermaid_to_images.cli import cli


@pytest.mark.parametrize(
    "args, exit_code",
    [
        ([], 2),
        (["-m", "hello"], 2),
        (["-m", "hello"], 2),
        (["-m", "tests/data/example.md"], 2),
        (["-o", "does_not_exist"], 2),
        (["-o", "tests/data/output"], 1),
    ],
)
def test_fail_args(runner, args, exit_code):
    result = runner.invoke(cli, args)
    assert result.exit_code == exit_code


@pytest.mark.parametrize(
    "args",
    [
        (["-m", "tests/data/example.md", "-o", "tests/data/output"]),
        (
            [
                "-f",
                "tests/data",
                "-i",
                "tests/data/another_folder",
                "-i",
                "tests/data/expected/",
                "-o",
                "tests/data/output",
            ]
        ),
    ],
)
def test_success(mocker, helpers, runner, args):
    uuid_return = [
        mocker.MagicMock(hex="a18fcc0f6bf14950b5115b22752471cc"),
        mocker.MagicMock(hex="7d2490309c1c4bf48069dd7399944ff4"),
        mocker.MagicMock(hex="183db8116412491abb8ecc7871067dda"),
    ]
    mocker.patch("uuid.uuid4", side_effect=uuid_return)
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    helpers.compare_files()
    helpers.remove_files_in_output()


def test_fail_install_node_modules(mocker, helpers, runner):
    shutil.rmtree("node_modules")
    args = ["-m", "tests/data/example.md", "-o", "tests/data/output"]
    mock = mocker.patch("subprocess.check_output")
    mock.side_effect = subprocess.CalledProcessError(returncode=1, cmd="")
    result = runner.invoke(cli, args)
    assert result.exit_code == 1


def test_success_install_node_modules(mocker, helpers, runner):
    uuid_return = [
        mocker.MagicMock(hex="a18fcc0f6bf14950b5115b22752471cc"),
        mocker.MagicMock(hex="7d2490309c1c4bf48069dd7399944ff4"),
        mocker.MagicMock(hex="183db8116412491abb8ecc7871067dda"),
    ]
    mocker.patch("uuid.uuid4", side_effect=uuid_return)
    args = ["-m", "tests/data/example.md", "-o", "tests/data/output"]
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
    helpers.compare_files()
    helpers.remove_files_in_output()


@pytest.mark.parametrize("exception", [subprocess.CalledProcessError(returncode=1, cmd=""), OSError])
def test_fail_export_images(mocker, runner, exception):
    args = ["-m", "tests/data/example.md", "-o", "tests/data/output"]
    mocker.patch("subprocess.check_output", side_effect=[True, exception])
    result = runner.invoke(cli, args)
    assert result.exit_code == 1


def test_fail_convert_markdown_to_json(mocker, runner):
    args = ["-m", "tests/data/example.md", "-o", "tests/data/output"]
    mocker.patch("pypandoc.convert_file", side_effect=OSError)
    result = runner.invoke(cli, args)
    assert result.exit_code == 1


def test_fail_convert_json_to_markdown(mocker, runner):
    args = ["-m", "tests/data/example.md", "-o", "tests/data/output"]
    mocker.patch("pypandoc.convert_text", side_effect=OSError)
    result = runner.invoke(cli, args)
    assert result.exit_code == 1
