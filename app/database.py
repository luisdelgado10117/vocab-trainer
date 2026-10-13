"""
Configuración de la base de datos.

- En desarrollo y tests: SQLite (archivo local o en memoria).
- En producción: PostgreSQL (por ejemplo Neon), indicado con la variable
  de entorno DATABASE_URL. Así el mismo código corre en ambos sitios.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool


def normalize_database_url(url: str) -> str:
    """Deja la URL de Postgres en la forma 'postgresql+psycopg2://...'.

    - Algunos proveedores entregan 'postgres://' (esquema antiguo) que
      SQLAlchemy 2.x ya no acepta.
    - Indicar el driver explícitamente (+psycopg2) evita que distintas
      versiones de SQLAlchemy elijan un driver por defecto diferente.
    """
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg2://" + url[len(prefix) :]
    return url


DATABASE_URL = normalize_database_url(
    os.environ.get("DATABASE_URL", "sqlite:///vocab.db")
)

engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    # check_same_thread solo existe en SQLite; con Postgres daría error.
    engine_kwargs["connect_args"] = {"check_same_thread": False}

    # Una base ":memory:" se borra al cerrar la conexión: usamos siempre
    # la misma conexión para que todas las sesiones vean los mismos datos.
    if DATABASE_URL == "sqlite:///:memory:":
        engine_kwargs["poolclass"] = StaticPool
else:
    # Bases en la nube (Neon, etc.) que se "duermen" cuando no se usan:
    # pool_pre_ping prueba la conexión antes de usarla y la reabre si
    # quedó cerrada; pool_recycle renueva conexiones viejas.
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_recycle"] = 300

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
