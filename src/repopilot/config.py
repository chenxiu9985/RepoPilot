"""Validated configuration shared by future agent and execution modules."""

from pydantic import AnyHttpUrl, Field, PositiveFloat, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load explicit values, environment variables, then an optional local .env.

    Credentials are optional until a real adapter is selected. The API key is
    excluded from model serialization and repr; callers must never log raw
    environment variables or ``get_secret_value()`` results.
    """

    model_config = SettingsConfigDict(
        env_prefix="REPOPILOT_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        hide_input_in_errors=True,
    )

    llm_base_url: AnyHttpUrl | None = None
    llm_model: str | None = None
    llm_api_key: SecretStr | None = Field(default=None, repr=False, exclude=True)
    max_steps: PositiveInt = 20
    llm_timeout_seconds: PositiveFloat = 60
    llm_max_retries: int = Field(default=2, ge=0, le=5)
    test_timeout_seconds: PositiveFloat = 60
