"""
Cálculo de rachas de estudio (días consecutivos).

Es una función PURA a propósito (como review_card en scheduler.py): solo
depende de sus parámetros, no de la base de datos ni de la fecha real del
sistema (salvo cuando no se la pasan explícitamente). Esto la hace fácil
de probar con muchos escenarios distintos.
"""

from datetime import date, timedelta


def calculate_streak(
    study_dates: set[date], today: date | None = None
) -> tuple[int, int]:
    """Calcula la racha actual y la racha más larga a partir de un conjunto
    de fechas en las que el usuario estudió (sin importar cuántas tarjetas
    repasó ese día, solo si estudió o no).

    Returns:
        (racha_actual, racha_mas_larga)
    """
    if not study_dates:
        return 0, 0

    today = today or date.today()

    # --- Racha actual: días consecutivos terminando HOY o AYER ---
    # (si no has estudiado hoy pero sí ayer, tu racha sigue "viva" hasta medianoche)
    sorted_desc = sorted(study_dates, reverse=True)
    current_streak = 0

    if sorted_desc[0] in (today, today - timedelta(days=1)):
        current_streak = 1
        for i in range(1, len(sorted_desc)):
            gap = sorted_desc[i - 1] - sorted_desc[i]
            if gap == timedelta(days=1):
                current_streak += 1
            else:
                break

    # --- Racha más larga: la secuencia consecutiva más larga en todo el historial ---
    sorted_asc = sorted(study_dates)
    longest_streak = 1
    run = 1

    for i in range(1, len(sorted_asc)):
        gap = sorted_asc[i] - sorted_asc[i - 1]
        if gap == timedelta(days=1):
            run += 1
            longest_streak = max(longest_streak, run)
        else:
            run = 1

    longest_streak = max(longest_streak, current_streak)

    return current_streak, longest_streak
