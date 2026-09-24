"""
Pruebas del endpoint /cards/grouped.
"""

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest

from app.database import SessionLocal, init_db
from app.main import app
from app.models import Card, ReviewLog, User


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


def test_agrupa_por_verbo(client, auth_headers):
    client.post("/cards/seed", headers=auth_headers)

    response = client.get("/cards/grouped", headers=auth_headers)
    data = response.get_json()

    assert response.status_code == 200
    assert len(data["groups"]) == 15  # 15 verbos en el paquete

    go_group = next(g for g in data["groups"] if g["group"] == "go")
    assert len(go_group["forms"]) == 3  # infinitivo, pasado, participio


def test_palabra_manual_va_en_ungrouped(client, auth_headers):
    client.post(
        "/cards", json={"word": "keyboard", "translation": "teclado"}, headers=auth_headers
    )

    response = client.get("/cards/grouped", headers=auth_headers)
    data = response.get_json()

    assert len(data["groups"]) == 0
    assert len(data["ungrouped"]) == 1
    assert data["ungrouped"][0]["word"] == "keyboard"


def test_grouped_requiere_auth(client):
    response = client.get("/cards/grouped")
    assert response.status_code == 401