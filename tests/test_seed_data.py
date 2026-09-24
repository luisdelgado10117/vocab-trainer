"""
Pruebas del endpoint /cards/seed (paquete de vocabulario inicial).
"""

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest

from app.database import SessionLocal, init_db
from app.models import Card, ReviewLog, User
from app.main import app
from app.seed_data import IRREGULAR_VERBS_PACK


@pytest.fixture
def client():
    init_db()

    db = SessionLocal()
    db.query(ReviewLog).delete()
    db.query(Card).delete()
    db.query(User).delete()
    db.commit()
    db.close()

    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    client.post("/register", json={"username": "ana", "password": "1234"})
    response = client.post("/login", json={"username": "ana", "password": "1234"})
    token = response.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_importar_paquete(client, auth_headers):
    response = client.post("/cards/seed", headers=auth_headers)
    assert response.status_code == 201
    assert response.get_json()["imported"] == len(IRREGULAR_VERBS_PACK)


def test_importar_paquete_dos_veces_no_duplica(client, auth_headers):
    client.post("/cards/seed", headers=auth_headers)
    response = client.post("/cards/seed", headers=auth_headers)

    assert response.get_json()["imported"] == 0

    cards_response = client.get("/cards", headers=auth_headers)
    assert len(cards_response.get_json()) == len(IRREGULAR_VERBS_PACK)


def test_importar_paquete_requiere_auth(client):
    response = client.post("/cards/seed")
    assert response.status_code == 401


def test_paquete_importado_esta_pendiente_hoy(client, auth_headers):
    client.post("/cards/seed", headers=auth_headers)

    response = client.get("/cards/due", headers=auth_headers)
    assert len(response.get_json()) == len(IRREGULAR_VERBS_PACK)
