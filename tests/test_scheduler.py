"""
Pruebas del algoritmo SM-2.

Como este algoritmo tiene reglas matemáticas precisas, las pruebas son
especialmente importantes: nos dejan verificar que el comportamiento es
el esperado en distintos escenarios (recordar bien varias veces seguidas,
olvidar, mejorar después de olvidar, etc).
"""

from datetime import date

import pytest

from core.card import Card
from core.scheduler import review_card


def test_quality_invalida_lanza_error():
    card = Card(word="hello", translation="hola")
    with pytest.raises(ValueError):
        review_card(card, quality=6)
    with pytest.raises(ValueError):
        review_card(card, quality=-1)


def test_primera_repeticion_correcta():
    """La primera vez que recuerdas bien una palabra, el intervalo es de 1 día."""
    card = Card(word="hello", translation="hola")
    today = date(2026, 1, 1)

    review_card(card, quality=4, today=today)

    assert card.repetitions == 1
    assert card.interval == 1
    assert card.due_date == date(2026, 1, 2)


def test_segunda_repeticion_correcta():
    """La segunda vez seguida que la recuerdas bien, el intervalo salta a 6 días."""
    card = Card(word="hello", translation="hola")
    today = date(2026, 1, 1)

    review_card(card, quality=4, today=today)
    review_card(card, quality=4, today=date(2026, 1, 2))

    assert card.repetitions == 2
    assert card.interval == 6


def test_tercera_repeticion_usa_easiness_factor():
    """De la tercera vez en adelante, el intervalo crece multiplicando por el easiness_factor."""
    card = Card(word="hello", translation="hola")
    today = date(2026, 1, 1)

    review_card(card, quality=4, today=today)  # repetitions=1, interval=1
    review_card(card, quality=4, today=date(2026, 1, 2))  # repetitions=2, interval=6
    review_card(card, quality=4, today=date(2026, 1, 8))  # repetitions=3, interval=6*EF

    assert card.repetitions == 3
    assert card.interval == round(6 * card.easiness_factor)


def test_olvidar_reinicia_el_progreso():
    """Si la calificación es menor a 3, se reinician las repeticiones."""
    card = Card(word="hello", translation="hola")
    today = date(2026, 1, 1)

    review_card(card, quality=4, today=today)
    review_card(card, quality=4, today=date(2026, 1, 2))
    assert card.repetitions == 2

    # Ahora la olvida:
    review_card(card, quality=1, today=date(2026, 1, 8))

    assert card.repetitions == 0
    assert card.interval == 1


def test_easiness_factor_nunca_baja_del_minimo():
    """Calificar muy bajo repetidamente no debe bajar el easiness_factor de 1.3."""
    card = Card(word="dificil", translation="difficult")
    today = date(2026, 1, 1)

    for _ in range(10):
        review_card(card, quality=0, today=today)

    assert card.easiness_factor >= 1.3


def test_calificacion_perfecta_aumenta_easiness_factor():
    """Recordar perfecto (quality=5) debe aumentar el easiness_factor."""
    card = Card(word="hello", translation="hola")
    ef_inicial = card.easiness_factor

    review_card(card, quality=5, today=date(2026, 1, 1))

    assert card.easiness_factor > ef_inicial
