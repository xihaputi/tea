from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# 创建数据库引擎
# Create database engine
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建 SessionLocal 类
# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类
# Create Base class
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    Get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
