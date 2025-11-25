from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

settings = get_settings()

# Prefer explicit DB_URL (e.g., mysql+pymysql://user:pass@host:3306/tea), fallback to SQLite file.
DATABASE_URL = settings.db_url or f"sqlite:///{settings.sqlite_path}"
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Provide a SQLAlchemy session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
