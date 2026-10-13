"""
Pruebas de normalize_database_url (esquemas de URL de bases de datos).
"""

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import normalize_database_url


def test_convierte_postgres_a_postgresql_psycopg2():
    url = "postgres://user:pass@host/db"
    assert normalize_database_url(url) == "postgresql+psycopg2://user:pass@host/db"


def test_agrega_driver_a_postgresql():
    url = "postgresql://user:pass@host/db?sslmode=require"
    assert (
        normalize_database_url(url)
        == "postgresql+psycopg2://user:pass@host/db?sslmode=require"
    )


def test_respeta_un_driver_ya_indicado():
    url = "postgresql+psycopg2://user:pass@host/db"
    assert normalize_database_url(url) == url


def test_no_toca_sqlite():
    assert normalize_database_url("sqlite:///vocab.db") == "sqlite:///vocab.db"
