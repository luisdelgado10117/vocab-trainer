"""
Capa de lógica de negocio: StatsManager.

Junta datos de dos tablas (Card y ReviewLog) y usa la función pura
core.streak.calculate_streak para armar un resumen de progreso.

Definimos "tarjeta dominada" como una tarjeta con un intervalo de 21 días
o más (es la misma convención que usa Anki para considerar una tarjeta
"madura": ya no necesitas repasarla seguido).
"""

from datetime import date

from sqlalchemy.orm import Session

from app.models import Card, ReviewLog
from core.streak import calculate_streak

MASTERED_INTERVAL_THRESHOLD = 21  # días


class StatsManager:
    def __init__(self, db: Session):
        self.db = db

    def get_stats(self, user_id: int) -> dict:
        total_cards = self.db.query(Card).filter(Card.user_id == user_id).count()

        mastered_cards = (
            self.db.query(Card)
            .filter(
                Card.user_id == user_id, Card.interval >= MASTERED_INTERVAL_THRESHOLD
            )
            .count()
        )

        cards_reviewed_today = (
            self.db.query(ReviewLog)
            .filter(ReviewLog.user_id == user_id, ReviewLog.reviewed_on == date.today())
            .count()
        )

        # sacamos las fechas ÚNICAS en las que el usuario repasó algo
        rows = (
            self.db.query(ReviewLog.reviewed_on)
            .filter(ReviewLog.user_id == user_id)
            .distinct()
            .all()
        )
        study_dates = {row[0] for row in rows}

        current_streak, longest_streak = calculate_streak(study_dates)

        return {
            "total_cards": total_cards,
            "mastered_cards": mastered_cards,
            "cards_reviewed_today": cards_reviewed_today,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
        }
