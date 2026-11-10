"""Keep tests independent of developer credentials and local .env files."""

import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolate_configuration(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for name in tuple(os.environ):
        if name.upper().startswith("REPOPILOT_"):
            monkeypatch.delenv(name)
    monkeypatch.chdir(tmp_path)
