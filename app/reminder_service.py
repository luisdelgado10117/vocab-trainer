"""
Decide a quién recordarle que repase, y le manda la notificación.

Reglas para que un usuario reciba un recordatorio HOY:
    1. Tiene un dispositivo registrado (fcm_token no es None)
    2. Tiene al menos una tarjeta pendiente de repaso hoy
    3. Todavía no se le avisó hoy (evita duplicados si el job corre 2 veces)
"""

from datetime import date

from sqlalchemy.orm import Session

from app.models import Card, User
from app.notifications import send_notification


def send_daily_reminders(db: Session) -> int:
    """Revisa a todos los usuarios y envía recordatorios a quien aplique.

    Devuelve cuántas notificaciones se enviaron exitosamente.
    """
    today = date.today()
    candidates = db.query(User).filter(User.fcm_token.isnot(None)).all()

    sent_count = 0

    for user in candidates:
        if user.last_reminded_on == today:
            continue  # ya se le avisó hoy, no lo satures

        due_count = (
            db.query(Card)
            .filter(Card.user_id == user.id, Card.due_date <= today)
            .count()
        )

        if due_count == 0:
            continue  # no tiene nada pendiente, no hay nada que recordarle

        palabra_o_palabras = "palabra" if due_count == 1 else "palabras"

        try:
            send_notification(
                user.fcm_token,
                title="Es hora de repasar",
                body=f"Tienes {due_count} {palabra_o_palabras} pendiente(s) hoy.",
            )
            user.last_reminded_on = today
            sent_count += 1
        except Exception:
            # Si el envío falla (token inválido, sin internet, etc), no
            # detenemos todo el proceso - seguimos con el resto de usuarios.
            continue

    db.commit()
    return sent_count
