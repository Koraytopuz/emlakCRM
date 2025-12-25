from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# psycopg2 kontrolü - yoksa SQLite kullan
try:
    import psycopg2
    DATABASE_URL = settings.DATABASE_URL
except ImportError:
    import warnings
    warnings.warn(
        "psycopg2 bulunamadı! SQLite kullanılıyor. "
        "PostgreSQL için: pip install psycopg2-binary"
    )
    # SQLite fallback
    DATABASE_URL = "sqlite:///./emlakcrm.db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

