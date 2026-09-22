"""
Capa de lógica de negocio: CardManager.

LO IMPORTANTE de este archivo: NO reescribimos el algoritmo SM-2 aquí.
Lo reutilizamos tal cual está en core/scheduler.py (el mismo que ya
probamos con 7 tests). Esto es una gran ventaja de haber separado el
algoritmo del resto desde el inicio: ahora que necesitamos usarlo desde
una API en vez de la consola, no duplicamos ni una línea de esa lógica.

Como core.scheduler.review_card() trabaja con un core.card.Card (un
dataclass simple, sin base de datos), lo que hacemos aquí es:
  1. Armar un core.card.Card "temporal" con los datos de la fila de BD
  2. Dejar que review_card() haga su magia (ya probada)
  3. Copiar los resultados de vuelta a la fila de la base de datos
"""

from datetime import date

from sqlalchemy.orm import Session

from app.errors import CardNotFoundError, InvalidCardDataError
from app.models import Card
from core.card import Card as CoreCard
from core.scheduler import review_card


class CardManager:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: int) -> list[Card]:
        return self.db.query(Card).filter(Card.user_id == user_id).all()

    def get_due(self, user_id: int) -> list[Card]:
        today = date.today()
        return (
            self.db.query(Card)
            .filter(Card.user_id == user_id, Card.due_date <= today)
            .all()
        )

    def get_by_id(self, card_id: int, user_id: int) -> Card:
        card = (
            self.db.query(Card)
            .filter(Card.id == card_id, Card.user_id == user_id)
            .first()
        )
        if card is None:
            raise CardNotFoundError(f"No existe una tarjeta con id {card_id}")
        return card

    def create(self, word, translation, user_id: int) -> Card:
        self._validate_text(word, "word")
        self._validate_text(translation, "translation")

        card = Card(
            word=word.strip(),
            translation=translation.strip(),
            due_date=date.today(),
            user_id=user_id,
        )
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def submit_review(self, card_id: int, user_id: int, quality) -> Card:
        """Aplica una calificación de repaso a una tarjeta, usando el algoritmo SM-2."""
        db_card = self.get_by_id(card_id, user_id)

        if not isinstance(quality, int):
            raise InvalidCardDataError("El campo 'quality' debe ser un número entero")

        # Reconstruimos un core.card.Card temporal con los datos actuales...
        core_card = CoreCard(
            word=db_card.word,
            translation=db_card.translation,
            repetitions=db_card.repetitions,
            easiness_factor=db_card.easiness_factor,
            interval=db_card.interval,
            due_date=db_card.due_date,
        )

        try:
            review_card(core_card, quality)  # <- el algoritmo probado, sin cambios
        except ValueError as e:
            raise InvalidCardDataError(str(e)) from e

        # ...y copiamos los resultados de vuelta a la fila de la base de datos.
        db_card.repetitions = core_card.repetitions
        db_card.easiness_factor = core_card.easiness_factor
        db_card.interval = core_card.interval
        db_card.due_date = core_card.due_date

        self.db.commit()
        self.db.refresh(db_card)
        return db_card

    @staticmethod
    def _validate_text(value, field_name: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise InvalidCardDataError(f"El campo '{field_name}' es obligatorio")
