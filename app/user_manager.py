from sqlalchemy.orm import Session

from app.auth import generate_token, hash_password, verify_password
from app.errors import (
    InvalidCredentialsError,
    InvalidUserDataError,
    UserAlreadyExistsError,
)
from app.models import User


class UserManager:
    def __init__(self, db: Session):
        self.db = db

    def register(self, username, password) -> User:
        self._validate_credentials(username, password)

        existing = self.db.query(User).filter(User.username == username).first()
        if existing is not None:
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe")

        user = User(username=username.strip(), password_hash=hash_password(password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login(self, username, password) -> str:
        self._validate_credentials(username, password)

        user = self.db.query(User).filter(User.username == username).first()

        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Usuario o contraseña incorrectos")

        return generate_token(user.id)

    @staticmethod
    def _validate_credentials(username, password) -> None:
        if not isinstance(username, str) or not username.strip():
            raise InvalidUserDataError("El campo 'username' es obligatorio")
        if not isinstance(password, str) or len(password) < 4:
            raise InvalidUserDataError("La contraseña debe tener al menos 4 caracteres")
