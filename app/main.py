"""
API de entrenador de vocabulario - Fase 2.

Endpoints:
    POST   /register            -> crea una cuenta
    POST   /login                -> devuelve un token
    GET    /cards                -> lista todas tus tarjetas
    GET    /cards/due            -> lista solo las tarjetas pendientes de repaso hoy
    POST   /cards                -> crea una tarjeta nueva {word, translation}
    POST   /cards/<id>/review    -> aplica una calificación de repaso {quality: 0-5}
"""

from functools import wraps

import jwt
from flask import Flask, g, jsonify, request

from app.auth import decode_token
from app.card_manager import CardManager
from app.database import SessionLocal, init_db
from app.errors import (
    CardNotFoundError,
    InvalidCardDataError,
    InvalidCredentialsError,
    InvalidUserDataError,
    UserAlreadyExistsError,
)
from app.user_manager import UserManager

app = Flask(__name__)

init_db()


def get_card_manager() -> CardManager:
    return CardManager(SessionLocal())


def get_user_manager() -> UserManager:
    return UserManager(SessionLocal())


def require_auth(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return (
                jsonify(
                    {"error": "Falta el token (header Authorization: Bearer <token>)"}
                ),
                401,
            )

        token = auth_header.removeprefix("Bearer ").strip()

        try:
            g.user_id = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token expiró, inicia sesión de nuevo"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        return view_function(*args, **kwargs)

    return wrapper


# --- Autenticación ---


@app.post("/register")
def register():
    manager = get_user_manager()
    data = request.get_json(silent=True) or {}

    try:
        user = manager.register(
            username=data.get("username"), password=data.get("password")
        )
        return jsonify({"id": user.id, "username": user.username}), 201
    except InvalidUserDataError as e:
        return jsonify({"error": str(e)}), 400
    except UserAlreadyExistsError as e:
        return jsonify({"error": str(e)}), 409


@app.post("/login")
def login():
    manager = get_user_manager()
    data = request.get_json(silent=True) or {}

    try:
        token = manager.login(
            username=data.get("username"), password=data.get("password")
        )
        return jsonify({"token": token})
    except InvalidUserDataError as e:
        return jsonify({"error": str(e)}), 400
    except InvalidCredentialsError as e:
        return jsonify({"error": str(e)}), 401


# --- Tarjetas de vocabulario ---


@app.get("/cards")
@require_auth
def get_cards():
    manager = get_card_manager()
    cards = manager.get_all(g.user_id)
    return jsonify([c.to_dict() for c in cards])


@app.get("/cards/due")
@require_auth
def get_due_cards():
    manager = get_card_manager()
    cards = manager.get_due(g.user_id)
    return jsonify([c.to_dict() for c in cards])


@app.post("/cards")
@require_auth
def create_card():
    manager = get_card_manager()
    data = request.get_json(silent=True) or {}

    try:
        card = manager.create(
            word=data.get("word"),
            translation=data.get("translation"),
            user_id=g.user_id,
        )
        return jsonify(card.to_dict()), 201
    except InvalidCardDataError as e:
        return jsonify({"error": str(e)}), 400


@app.post("/cards/<int:card_id>/review")
@require_auth
def review_card_route(card_id: int):
    manager = get_card_manager()
    data = request.get_json(silent=True) or {}

    try:
        card = manager.submit_review(card_id, g.user_id, quality=data.get("quality"))
        return jsonify(card.to_dict())
    except CardNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except InvalidCardDataError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
