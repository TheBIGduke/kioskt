# Made by Kaléin Tamaríz
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Fix for sqlite path if it's just a file path in .env
    if DATABASE_URL.startswith("sqlite:///") == False and DATABASE_URL.endswith(".db"):
        DATABASE_URL = f"sqlite:///{DATABASE_URL}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Dependency that creates a new SQLAlchemy database session for each request."""
    if not SessionLocal:
        raise RuntimeError("Database not configured. Set DATABASE_URL environment variable.")
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
