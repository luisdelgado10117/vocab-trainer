"""
Programa el job diario que revisa y envía recordatorios de repaso.

Usa APScheduler, que corre un hilo en segundo plano DENTRO del mismo
proceso de tu API Flask. Para que esto funcione, tu servidor tiene que
seguir corriendo (si apagas 'python -m app.main', el job deja de correr
hasta que lo vuelvas a prender).

En producción con varios workers (ej. gunicorn con -w 4), esto correría
una vez POR WORKER, duplicando notificaciones - por ahora, con un solo
proceso de desarrollo, no es un problema. Es un detalle a resolver si
algún día escalas la API (quedaría como mejora futura en el README).
"""

import os

from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.reminder_service import send_daily_reminders

REMINDER_HOUR = int(os.environ.get("REMINDER_HOUR", "9"))
REMINDER_MINUTE = int(os.environ.get("REMINDER_MINUTE", "0"))

_scheduler = None


def _run_reminder_job():
    db = SessionLocal()
    try:
        sent = send_daily_reminders(db)
        print(f"[recordatorios] Se enviaron {sent} notificacion(es).")
    finally:
        db.close()


def start_scheduler():
    """Arranca el programador. Seguro de llamar más de una vez: si ya
    está corriendo, no crea un segundo (evitaría recordatorios duplicados).
    """
    global _scheduler

    if _scheduler is not None:
        return

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        _run_reminder_job,
        trigger="cron",
        hour=REMINDER_HOUR,
        minute=REMINDER_MINUTE,
    )
    _scheduler.start()
