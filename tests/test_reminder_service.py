"""
Pruebas de send_daily_reminders.

Usamos @patch para "simular" send_notification: no queremos que las
pruebas de verdad intenten contactar a Firebase (eso fallaría sin
credenciales reales, y además no deberíamos depender de internet para
que nuestros tests pasen).
"""

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from datetime import date, timedelta
from unittest.mock import patch

import pytest

from app.auth import hash_password
from app.database import SessionLocal, init_db
from app.models import Card, ReviewLog, User
from app.reminder_service import send_daily_reminders


@pytest.fixture
def db_session():
    init_db()

    db = SessionLocal()
    db.query(ReviewLog).delete()
    db.query(Card).delete()
    db.query(User).delete()
    db.commit()

    yield db

    db.close()


def _create_user_with_card(db, username, fcm_token=None, due_in_days=0):
    user = User(
        username=username, password_hash=hash_password("1234"), fcm_token=fcm_token
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    card = Card(
        word="test",
        translation="prueba",
        due_date=date.today() + timedelta(days=due_in_days),
        user_id=user.id,
    )
    db.add(card)
    db.commit()

    return user


@patch("app.reminder_service.send_notification")
def test_envia_a_usuario_con_pendientes_y_token(mock_send, db_session):
    user = _create_user_with_card(db_session, "ana", fcm_token="tok123", due_in_days=0)

    sent = send_daily_reminders(db_session)

    assert sent == 1
    mock_send.assert_called_once()

    db_session.refresh(user)
    assert user.last_reminded_on == date.today()


@patch("app.reminder_service.send_notification")
def test_no_envia_sin_token_registrado(mock_send, db_session):
    _create_user_with_card(db_session, "ana", fcm_token=None, due_in_days=0)

    sent = send_daily_reminders(db_session)

    assert sent == 0
    mock_send.assert_not_called()


@patch("app.reminder_service.send_notification")
def test_no_envia_si_no_tiene_pendientes(mock_send, db_session):
    _create_user_with_card(db_session, "ana", fcm_token="tok123", due_in_days=5)

    sent = send_daily_reminders(db_session)

    assert sent == 0
    mock_send.assert_not_called()


@patch("app.reminder_service.send_notification")
def test_no_envia_dos_veces_el_mismo_dia(mock_send, db_session):
    _create_user_with_card(db_session, "ana", fcm_token="tok123", due_in_days=0)

    primera_vez = send_daily_reminders(db_session)
    segunda_vez = send_daily_reminders(db_session)

    assert primera_vez == 1
    assert segunda_vez == 0
    mock_send.assert_called_once()


@patch("app.reminder_service.send_notification")
def test_varios_usuarios_independientes(mock_send, db_session):
    _create_user_with_card(
        db_session, "con_pendientes", fcm_token="tok1", due_in_days=0
    )
    _create_user_with_card(
        db_session, "sin_pendientes", fcm_token="tok2", due_in_days=10
    )
    _create_user_with_card(db_session, "sin_token", fcm_token=None, due_in_days=0)

    sent = send_daily_reminders(db_session)

    assert sent == 1  # solo el primero califica
