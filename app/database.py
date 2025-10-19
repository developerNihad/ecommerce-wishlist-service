from sqlmodel import SQLModel, create_engine, Session
from app.config import DATABASE_URL
import os

# Database Engine - Use psycopg2 for migrations, asyncpg for runtime
if DATABASE_URL and "asyncpg" in DATABASE_URL:
    # Convert asyncpg URL to psycopg2 for migrations
    migration_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
else:
    migration_url = DATABASE_URL

# Use psycopg2 for migrations and general database operations
engine = create_engine(migration_url, echo=False, pool_pre_ping=True, pool_recycle=300)

def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI"""
    with Session(engine) as session:
        yield session