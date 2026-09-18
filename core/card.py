"""
Representa una sola tarjeta de vocabulario (una palabra a aprender).

Cada tarjeta guarda no solo la palabra y su traducción, sino también los
datos que el algoritmo de repetición espaciada (SM-2) necesita para
decidir cuándo te conviene volver a verla:

    - repetitions: cuántas veces seguidas la has recordado bien
    - easiness_factor: qué tan "fácil" es esta palabra para ti (empieza en 2.5)
    - interval: cuántos días hay que esperar antes de la próxima repetición
    - due_date: la fecha en la que esta tarjeta "vence" (toca repasarla)
"""

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Card:
    """Una tarjeta de vocabulario con su estado de repetición espaciada."""

    word: str
    translation: str
    repetitions: int = 0
    easiness_factor: float = 2.5
    interval: int = 0
    due_date: date = field(default_factory=date.today)

    def is_due(self, today: date | None = None) -> bool:
        """¿Ya toca repasar esta tarjeta hoy (o antes)?"""
        today = today or date.today()
        return self.due_date <= today

    def to_dict(self) -> dict:
        """Convierte la tarjeta a un diccionario simple, listo para guardar en JSON."""
        return {
            "word": self.word,
            "translation": self.translation,
            "repetitions": self.repetitions,
            "easiness_factor": self.easiness_factor,
            "interval": self.interval,
            "due_date": self.due_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        """Reconstruye una Card a partir de un diccionario (lo opuesto de to_dict)."""
        return cls(
            word=data["word"],
            translation=data["translation"],
            repetitions=data["repetitions"],
            easiness_factor=data["easiness_factor"],
            interval=data["interval"],
            due_date=date.fromisoformat(data["due_date"]),
        )
