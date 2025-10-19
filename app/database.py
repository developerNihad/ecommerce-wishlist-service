from sqlmodel import SQLModel, create_engine, Session
from app.config import DATABASE_URL
import os

# Database Engine - Always use psycopg2 for SQLModel/SQLAlchemy
# Convert asyncpg URL to psycopg2 if needed
if DATABASE_URL and "asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True, pool_recycle=300)

def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI"""
    with Session(engine) as session:
        yield session