import os
from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base


class Settings(BaseSettings):
    # App settings
    app_name: str = "Library Management System"
    debug: bool = True

    basic_auth_username: ClassVar[str] = os.getenv("BASIC_AUTH_USERNAME", "root")
    basic_auth_password: ClassVar[str] = os.getenv("BASIC_AUTH_PASSWORD", "root")

    # Database settings
    database_url: str = "postgresql://postgres:library@library-db:5432/library"

    # Email settings
    sender_email: str
    sender_password: str
    smtp_server: str
    smtp_port: int

    class Config:
        env_file = ".env"


SQLALCHEMY_DATABASE_URL = Settings().database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


settings = Settings()
