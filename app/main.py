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

import os
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
from app.reminder_service import send_daily_reminders
from app.scheduler import start_scheduler
from app.stats_manager import StatsManager
from app.seed_data import IRREGULAR_VERBS_PACK
from app.user_manager import UserManager
from app.models import User
from app.notifications import send_notification

# Secreto compartido para poder disparar el job de recordatorios "a mano"
# (desde curl, o mas adelante desde un servicio externo de cron una vez
# que la API este desplegada). NO requiere login de usuario, pero SI
# requiere conocer este secreto.
CRON_SECRET = os.environ.get("CRON_SECRET", "cambia-este-secreto-en-produccion")

app = Flask(__name__)

init_db()
start_scheduler()


@app.get("/")
def health_check():
    """Ruta simple para probar que la API es alcanzable desde tu celular."""
    return jsonify({"status": "ok", "message": "La API esta funcionando"})


def get_card_manager() -> CardManager:
    return CardManager(SessionLocal())


def get_user_manager() -> UserManager:
    return UserManager(SessionLocal())


def get_stats_manager() -> StatsManager:
    return StatsManager(SessionLocal())


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


@app.post("/device-token")
@require_auth
def register_device_token():
    """Guarda el token de FCM del celular del usuario, para poder
    enviarle notificaciones push mas adelante."""
    data = request.get_json(silent=True) or {}
    token = data.get("token")

    if not isinstance(token, str) or not token.strip():
        return jsonify({"error": "El campo 'token' es obligatorio"}), 400

    db = SessionLocal()
    user = db.query(User).filter(User.id == g.user_id).first()
    user.fcm_token = token.strip()
    db.commit()

    return jsonify({"message": "Token guardado correctamente"}), 200


@app.post("/notifications/test")
@require_auth
def send_test_notification():
    """Envia una notificacion de prueba al dispositivo del usuario actual.
    Sirve para confirmar que todo el flujo (Firebase + token + backend)
    funciona de punta a punta antes de automatizar recordatorios reales."""
    db = SessionLocal()
    user = db.query(User).filter(User.id == g.user_id).first()

    if not user.fcm_token:
        return (
            jsonify(
                {"error": "Este usuario no tiene un dispositivo registrado todavia"}
            ),
            400,
        )

    try:
        message_id = send_notification(
            user.fcm_token,
            title="Entrenador de vocabulario",
            body="Esta es una notificacion de prueba. Si la ves, todo funciona!",
        )
        return (
            jsonify({"message": "Notificacion enviada", "message_id": message_id}),
            200,
        )
    except Exception as e:
        return jsonify({"error": f"Error al enviar la notificacion: {e}"}), 500


@app.post("/notifications/run-daily-check")
def run_daily_check():
    """Dispara manualmente la revision de recordatorios diarios.

    Protegido con un secreto compartido (header X-Cron-Secret), NO con
    login de un usuario especifico - revisa a TODOS los usuarios. Util
    para probar sin esperar a la hora programada, y mas adelante para
    conectarlo a un servicio externo de cron cuando la API este desplegada.
    """
    secret = request.headers.get("X-Cron-Secret")
    if secret != CRON_SECRET:
        return jsonify({"error": "No autorizado"}), 403

    db = SessionLocal()
    sent = send_daily_reminders(db)
    db.close()

    return jsonify({"message": f"Se enviaron {sent} notificacion(es)"}), 200


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


@app.get("/cards/grouped")
@require_auth
def get_grouped_cards():
    """Devuelve las tarjetas agrupadas por verbo (para la pantalla de
    'Mi vocabulario' en la app, en vez de una lista plana)."""
    manager = get_card_manager()
    return jsonify(manager.get_grouped(g.user_id))


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


@app.post("/cards/seed")
@require_auth
def import_seed_pack():
    """Importa (o sincroniza) todos los paquetes de vocabulario predefinidos.

    Es seguro llamarlo varias veces: nunca duplica. Por eso el cliente
    (la app) lo puede llamar en cada login sin preguntar - si en el
    futuro agregamos una categoría nueva (ej. sustantivos), los usuarios
    que ya tenían cuenta la reciben automáticamente en su siguiente login.
    """
    manager = get_card_manager()
    created = manager.import_seed_pack(g.user_id, IRREGULAR_VERBS_PACK)
    return (
        jsonify(
            {
                "imported": len(created),
                "cards": [c.to_dict() for c in created],
            }
        ),
        201,
    )


# --- Estadísticas de progreso ---


@app.get("/stats")
@require_auth
def get_stats():
    manager = get_stats_manager()
    return jsonify(manager.get_stats(g.user_id))


if __name__ == "__main__":
    # host="0.0.0.0" hace que la API escuche en TODAS las interfaces de red
    # de tu computadora (no solo en 127.0.0.1), para que tu celular pueda
    # alcanzarla estando en la misma red WiFi.
    app.run(host="0.0.0.0", port=5000, debug=True)
