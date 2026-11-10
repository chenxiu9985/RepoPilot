"""Check configuration boundaries and prevent accidental credential output."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from repopilot.config import Settings


def test_configuration_does_not_require_credentials() -> None:
    settings = Settings()
    assert settings.llm_api_key is None
    assert settings.llm_base_url is None
    assert settings.max_steps > 0


def test_environment_overrides_dotenv(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("REPOPILOT_MAX_STEPS=7\n", encoding="utf-8")
    assert Settings().max_steps == 7
    monkeypatch.setenv("REPOPILOT_MAX_STEPS", "9")
    assert Settings().max_steps == 9
    assert Settings(max_steps=11).max_steps == 11


def test_empty_optional_settings_are_ignored(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text(
        "REPOPILOT_LLM_API_KEY=\nREPOPILOT_LLM_BASE_URL=\nREPOPILOT_LLM_MODEL=\n",
        encoding="utf-8",
    )
    settings = Settings()
    assert settings.llm_api_key is None
    assert settings.llm_base_url is None
    assert settings.llm_model is None


def test_api_key_is_excluded_from_common_outputs(monkeypatch: pytest.MonkeyPatch) -> None:
    secret = "test-only-credential-not-a-real-key"
    monkeypatch.setenv("REPOPILOT_LLM_API_KEY", secret)
    settings = Settings()
    assert settings.llm_api_key is not None
    assert settings.llm_api_key.get_secret_value() == secret
    assert "llm_api_key" not in settings.model_dump()
    assert secret not in repr(settings)
    assert secret not in settings.model_dump_json()


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("REPOPILOT_MAX_STEPS", "0"),
        ("REPOPILOT_LLM_TIMEOUT_SECONDS", "-1"),
        ("REPOPILOT_TEST_TIMEOUT_SECONDS", "0"),
        ("REPOPILOT_LLM_MAX_RETRIES", "-1"),
        ("REPOPILOT_LLM_MAX_RETRIES", "6"),
        ("REPOPILOT_LLM_BASE_URL", "not-a-url"),
    ],
)
def test_invalid_configuration_is_rejected(
    monkeypatch: pytest.MonkeyPatch, name: str, value: str
) -> None:
    monkeypatch.setenv(name, value)
    with pytest.raises(ValidationError):
        Settings()
