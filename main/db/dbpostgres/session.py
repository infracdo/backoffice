from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main.core.config import settings

options = {
    "echo": True,
    "pool_pre_ping": True,
    "pool_recycle": 120,
    "pool_size": 10,
    "max_overflow": 20,
}

engine = create_engine(url=str(settings.SQLALCHEMY_DATABASE_URI), **options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)