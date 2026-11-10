"""Smoke tests for the installed CLI, without model or Docker dependencies."""

import shutil
import subprocess
import sys
import sysconfig

import pytest


@pytest.mark.parametrize("arguments", [[], ["--help"], ["--version"]])
def test_module_entry_point(arguments: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "repopilot", *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "repopilot" in result.stdout.lower()
    if arguments != ["--version"]:
        assert "not implemented yet" in result.stdout


def test_installed_console_entry_point() -> None:
    executable = shutil.which("repopilot", path=sysconfig.get_path("scripts"))
    assert executable is not None, "Install the package before running tests."
    result = subprocess.run(
        [executable, "--version"], capture_output=True, text=True, timeout=10, check=False
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.startswith("repopilot ")


def test_unimplemented_run_is_rejected() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "repopilot", "run"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
        check=False,
    )
    assert result.returncode != 0
    assert "unrecognized arguments" in result.stderr
