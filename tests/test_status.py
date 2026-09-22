"""
Pruebas del endpoint /stats.
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


def test_stats_sin_actividad(client, auth_headers):
    response = client.get("/stats", headers=auth_headers)
    assert response.status_code == 200

    data = response.get_json()
    assert data["total_cards"] == 0
    assert data["current_streak"] == 0
    assert data["longest_streak"] == 0


def test_stats_total_cards(client, auth_headers):
    client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    client.post(
        "/cards", json={"word": "bye", "translation": "adios"}, headers=auth_headers
    )

    response = client.get("/stats", headers=auth_headers)
    assert response.get_json()["total_cards"] == 2


def test_stats_despues_de_un_repaso(client, auth_headers):
    create_response = client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    card_id = create_response.get_json()["id"]

    client.post(f"/cards/{card_id}/review", json={"quality": 5}, headers=auth_headers)

    response = client.get("/stats", headers=auth_headers)
    data = response.get_json()

    assert data["cards_reviewed_today"] == 1
    assert data["current_streak"] == 1
    assert data["longest_streak"] == 1


def test_stats_requiere_auth(client):
    response = client.get("/stats")
    assert response.status_code == 401


def test_stats_no_mezcla_usuarios(client, auth_headers):
    """Las estadísticas de un usuario no deben incluir actividad de otro."""
    create_response = client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    card_id = create_response.get_json()["id"]
    client.post(f"/cards/{card_id}/review", json={"quality": 5}, headers=auth_headers)

    client.post("/register", json={"username": "otro", "password": "1234"})
    login_otro = client.post("/login", json={"username": "otro", "password": "1234"})
    headers_otro = {"Authorization": f"Bearer {login_otro.get_json()['token']}"}

    response = client.get("/stats", headers=headers_otro)
    data = response.get_json()

    assert data["total_cards"] == 0
    assert data["current_streak"] == 0
