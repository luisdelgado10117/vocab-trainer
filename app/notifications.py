"""
Envío de notificaciones push usando Firebase Cloud Messaging (FCM).

Usa el SDK de administrador de Firebase (firebase-admin), que necesita
una "clave de cuenta de servicio": un archivo JSON secreto que generaste
en la consola de Firebase (Configuración del proyecto -> Cuentas de
servicio -> Generar nueva clave privada).

ESTE ARCHIVO NUNCA SE SUBE A GIT - da acceso administrativo completo a
tu proyecto de Firebase. Por eso su nombre está en .gitignore.
"""

import os

import firebase_admin
from firebase_admin import credentials, messaging

CREDENTIALS_PATH = os.environ.get(
    "FIREBASE_CREDENTIALS_PATH", "firebase-service-account.json"
)

_firebase_app = None


def _get_firebase_app():
    """Inicializa la conexión con Firebase una sola vez (patrón singleton).

    Inicializar esto en cada notificación sería lento e innecesario; lo
    hacemos una vez y reutilizamos la misma conexión después.
    """
    global _firebase_app

    if _firebase_app is None:
        cred = credentials.Certificate(CREDENTIALS_PATH)
        _firebase_app = firebase_admin.initialize_app(cred)

    return _firebase_app


def send_notification(fcm_token: str, title: str, body: str) -> str:
    """Envía una notificación push a un dispositivo específico.

    Devuelve el id del mensaje enviado (útil para logs/depuración).
    """
    _get_firebase_app()

    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=fcm_token,
    )

    return messaging.send(message)