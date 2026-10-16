import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.card_manager import CardManager
from app.database import Base
from app.models import Card, User
from app.seed_data import PHRASAL_VERBS_PACK, SEED_PACKS


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()


@pytest.fixture
def user_id(db):
    user = User(username="tester", password_hash="x")
    db.add(user)
    db.commit()
    return user.id


def test_phrasal_pack_has_30_unique_entries():
    keys = {(e["word"], e["translation"]) for e in PHRASAL_VERBS_PACK}
    assert len(PHRASAL_VERBS_PACK) == 30
    assert len(keys) == 30


def test_import_all_creates_every_pack(db, user_id):
    manager = CardManager(db)
    created = manager.import_all_seed_packs(user_id, SEED_PACKS)

    total = sum(len(p) for p in SEED_PACKS.values())
    assert len(created) == total


def test_import_all_is_idempotent(db, user_id):
    manager = CardManager(db)
    manager.import_all_seed_packs(user_id, SEED_PACKS)
    second = manager.import_all_seed_packs(user_id, SEED_PACKS)

    assert second == []


def test_existing_user_receives_new_category(db, user_id):
    manager = CardManager(db)
    # Simula a un usuario antiguo: solo tiene irregulares.
    manager.import_seed_pack(user_id, SEED_PACKS["irregular_verbs"], "irregular_verbs")

    created = manager.import_all_seed_packs(user_id, SEED_PACKS)

    assert len(created) == len(PHRASAL_VERBS_PACK)
    assert all(c.category == "phrasal_verbs" for c in created)


def test_cards_are_saved_with_their_category(db, user_id):
    manager = CardManager(db)
    manager.import_all_seed_packs(user_id, SEED_PACKS)

    phrasal = (
        db.query(Card)
        .filter(Card.user_id == user_id, Card.category == "phrasal_verbs")
        .all()
    )
    assert len(phrasal) == 30
    assert all(c.tense is None for c in phrasal)


def test_same_word_in_two_categories_does_not_collide(db, user_id):
    manager = CardManager(db)
    entry = [{"word": "x", "translation": "y", "group": "g", "tense": None}]

    a = manager.import_seed_pack(user_id, entry, "cat_a")
    b = manager.import_seed_pack(user_id, entry, "cat_b")

    assert len(a) == 1
    assert len(b) == 1
