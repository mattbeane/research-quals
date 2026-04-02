"""Configuration via environment variables / .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="PIPELINE_")

    db_path: str = "pipeline.db"
    host: str = "0.0.0.0"
    port: int = 8100
    auth_token: str = ""  # empty = no auth (local-only mode)

    @property
    def db_abs_path(self) -> Path:
        p = Path(self.db_path)
        if not p.is_absolute():
            p = Path(__file__).resolve().parent.parent.parent / p
        return p
