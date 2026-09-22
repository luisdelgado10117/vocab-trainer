"""
Pruebas de calculate_streak, con distintos escenarios de fechas de estudio.
"""

from datetime import date

from core.streak import calculate_streak


def test_sin_fechas():
    current, longest = calculate_streak(set())
    assert current == 0
    assert longest == 0


def test_solo_hoy():
    today = date(2026, 1, 10)
    current, longest = calculate_streak({today}, today=today)
    assert current == 1
    assert longest == 1


def test_racha_de_tres_dias_seguidos_hasta_hoy():
    today = date(2026, 1, 10)
    fechas = {date(2026, 1, 8), date(2026, 1, 9), date(2026, 1, 10)}
    current, longest = calculate_streak(fechas, today=today)
    assert current == 3
    assert longest == 3


def test_racha_sigue_viva_si_ayer_estudio_pero_hoy_no():
    """Si estudiaste ayer pero todavía no hoy, tu racha actual no se rompe."""
    today = date(2026, 1, 10)
    fechas = {date(2026, 1, 8), date(2026, 1, 9)}  # nada el día 10 (hoy)
    current, longest = calculate_streak(fechas, today=today)
    assert current == 2


def test_racha_se_rompe_si_paso_mas_de_un_dia():
    today = date(2026, 1, 10)
    fechas = {date(2026, 1, 5), date(2026, 1, 6)}  # hay un hueco grande hasta hoy
    current, longest = calculate_streak(fechas, today=today)
    assert current == 0


def test_racha_mas_larga_puede_ser_mayor_a_la_actual():
    """Tuviste una racha larga en el pasado, pero se rompió; ahora vas empezando otra."""
    today = date(2026, 1, 20)
    fechas = {
        # Racha larga en el pasado: 5 días seguidos
        date(2026, 1, 1),
        date(2026, 1, 2),
        date(2026, 1, 3),
        date(2026, 1, 4),
        date(2026, 1, 5),
        # Racha actual: solo 2 días
        date(2026, 1, 19),
        date(2026, 1, 20),
    }
    current, longest = calculate_streak(fechas, today=today)
    assert current == 2
    assert longest == 5


def test_dias_no_consecutivos_dan_racha_de_uno():
    today = date(2026, 1, 10)
    fechas = {date(2026, 1, 1), date(2026, 1, 5), date(2026, 1, 10)}
    current, longest = calculate_streak(fechas, today=today)
    assert current == 1
    assert longest == 1
