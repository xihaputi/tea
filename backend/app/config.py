from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Ó¦ÓÃÅäÖÃ
    Application Settings
    """
    DATABASE_URL: str = "sqlite:///./tea_garden.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
