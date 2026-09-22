"""
Pruebas de la API del entrenador de vocabulario.

Corre con:
    python -m pytest
"""

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest

from app.database import SessionLocal, init_db
from app.main import app
from app.models import Card, User


@pytest.fixture
def client():
    init_db()

    db = SessionLocal()
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


def test_crear_tarjeta(client, auth_headers):
    response = client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    assert response.status_code == 201

    data = response.get_json()
    assert data["word"] == "hello"
    assert data["repetitions"] == 0


def test_crear_tarjeta_sin_datos(client, auth_headers):
    response = client.post("/cards", json={"word": "hello"}, headers=auth_headers)
    assert response.status_code == 400


def test_tarjeta_nueva_esta_pendiente_hoy(client, auth_headers):
    client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )

    response = client.get("/cards/due", headers=auth_headers)
    assert len(response.get_json()) == 1


def test_review_actualiza_intervalo(client, auth_headers):
    create_response = client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    card_id = create_response.get_json()["id"]

    review_response = client.post(
        f"/cards/{card_id}/review", json={"quality": 5}, headers=auth_headers
    )
    assert review_response.status_code == 200

    data = review_response.get_json()
    assert data["repetitions"] == 1
    assert data["interval"] == 1


def test_review_quality_invalida(client, auth_headers):
    create_response = client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    card_id = create_response.get_json()["id"]

    response = client.post(
        f"/cards/{card_id}/review", json={"quality": 10}, headers=auth_headers
    )
    assert response.status_code == 400


def test_review_tarjeta_de_otro_usuario(client, auth_headers):
    create_response = client.post(
        "/cards", json={"word": "hello", "translation": "hola"}, headers=auth_headers
    )
    card_id = create_response.get_json()["id"]

    client.post("/register", json={"username": "otro", "password": "1234"})
    login_otro = client.post("/login", json={"username": "otro", "password": "1234"})
    headers_otro = {"Authorization": f"Bearer {login_otro.get_json()['token']}"}

    response = client.post(
        f"/cards/{card_id}/review", json={"quality": 5}, headers=headers_otro
    )
    assert response.status_code == 404


def test_cards_requiere_auth(client):
    response = client.get("/cards")
    assert response.status_code == 401
