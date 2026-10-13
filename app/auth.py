"""
Utilidades de autenticación: hash de contraseñas y tokens JWT.
Mismo enfoque que en todo-api-python (ya validado ahí).
"""

import datetime
import os

import jwt
from werkzeug.security import check_password_hash, generate_password_hash

DEFAULT_DEV_SECRET = "clave-secreta-de-desarrollo-cambiame"
SECRET_KEY = os.environ.get("SECRET_KEY", DEFAULT_DEV_SECRET)

# "Fallar rápido": si olvidas configurar SECRET_KEY en producción, es mejor
# que la app NO arranque a que arranque con una clave pública que permitiría
# a cualquiera fabricar tokens de sesión válidos.
if os.environ.get("APP_ENV") == "production" and SECRET_KEY == DEFAULT_DEV_SECRET:
    raise RuntimeError("En produccion debes definir la variable de entorno SECRET_KEY")
TOKEN_EXP_HOURS = 24


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def generate_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=TOKEN_EXP_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["user_id"]
