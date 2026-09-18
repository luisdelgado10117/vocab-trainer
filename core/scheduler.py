"""
Algoritmo SM-2 de repetición espaciada (el mismo que usa Anki).

LA IDEA CENTRAL: cada vez que repasas una palabra, te calificas del 0 al 5
qué tan bien la recordaste. Con esa calificación, el algoritmo decide:

    1. ¿Reiniciamos el conteo? (la olvidaste, quality < 3)
    2. ¿Cuántos días esperamos antes de la próxima vez? (el "intervalo")
    3. ¿Qué tan "fácil" es esta palabra para ti? (el "easiness factor")

Mientras mejor la recuerdes, más se espacían las repeticiones (1 día,
luego 6, luego 6 * easiness_factor, luego eso * easiness_factor otra
vez...). Así no pierdes tiempo repasando lo que ya te sabes de memoria.
"""

from datetime import date, timedelta

from core.card import Card

# Calificaciones válidas para qué tan bien recordaste una palabra:
#   0-2 = no la recordaste (o muy mal)   -> se reinicia el progreso
#   3-5 = sí la recordaste (con esfuerzo creciente hacia 5 = perfecto)
QUALITY_MIN = 0
QUALITY_MAX = 5
QUALITY_PASS_THRESHOLD = 3

MIN_EASINESS_FACTOR = 1.3


def review_card(card: Card, quality: int, today: date | None = None) -> Card:
    """Actualiza una tarjeta después de repasarla, según el algoritmo SM-2.

    Args:
        card: la tarjeta que se acaba de repasar.
        quality: qué tan bien la recordaste, del 0 (nada) al 5 (perfecto).
        today: la fecha de hoy (parámetro para poder probarlo en los tests
               sin depender de la fecha real de la computadora).

    Returns:
        La misma tarjeta, con sus valores ya actualizados.
    """
    if not (QUALITY_MIN <= quality <= QUALITY_MAX):
        raise ValueError(f"quality debe estar entre {QUALITY_MIN} y {QUALITY_MAX}")

    today = today or date.today()

    if quality < QUALITY_PASS_THRESHOLD:
        # No la recordaste bien: se reinicia el progreso de esta tarjeta.
        card.repetitions = 0
        card.interval = 1
    else:
        # Sí la recordaste: avanzamos según cuántas veces seguidas ha ido bien.
        if card.repetitions == 0:
            card.interval = 1
        elif card.repetitions == 1:
            card.interval = 6
        else:
            card.interval = round(card.interval * card.easiness_factor)

        card.repetitions += 1

    # Ajustamos qué tan "fácil" es la palabra, según la calificación de hoy.
    # Esta fórmula es la fórmula original del algoritmo SM-2.
    card.easiness_factor += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    card.easiness_factor = max(card.easiness_factor, MIN_EASINESS_FACTOR)

    card.due_date = today + timedelta(days=card.interval)

    return card
