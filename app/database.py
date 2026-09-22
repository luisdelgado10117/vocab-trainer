"""
Configuración de la base de datos. Mismo patrón que en todo-api-python:
SQLite + SQLAlchemy, con DATABASE_URL configurable por variable de entorno
(para poder usar una base en memoria durante los tests).
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///vocab.db")

connect_args = {"check_same_thread": False}
engine_kwargs = {"connect_args": connect_args}

if DATABASE_URL == "sqlite:///:memory:":
    engine_kwargs["poolclass"] = StaticPool

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
