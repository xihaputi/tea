from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    env: str = "development"
    sqlite_path: Path = Path(__file__).resolve().parents[2] / "data" / "tea.db"
    db_url: str | None = None  # e.g. mysql+pymysql://user:pass@host:3306/tea
    upload_dir: Path = Path(__file__).resolve().parents[2] / "uploads"
    api_prefix: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
