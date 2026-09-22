class CardNotFoundError(Exception):
    """Se lanza cuando se busca una tarjeta que no existe (o no es tuya)."""


class InvalidCardDataError(Exception):
    """Se lanza cuando los datos de una tarjeta son inválidos."""


class UserAlreadyExistsError(Exception):
    """Se lanza al intentar registrar un username que ya está en uso."""


class InvalidUserDataError(Exception):
    """Se lanza cuando el username o password no cumplen las reglas mínimas."""


class InvalidCredentialsError(Exception):
    """Se lanza cuando el username o password no coinciden con ningún usuario."""
