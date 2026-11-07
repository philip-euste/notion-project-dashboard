
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Notion Project Dashboard"
    debug: bool = True

    database_url: str

    notion_api_key: str | None = None
    notion_database_id: str | None = None
    notion_webhook_secret: str | None = None

    sync_secret: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]
