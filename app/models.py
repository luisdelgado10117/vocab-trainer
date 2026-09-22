"""
Modelos de base de datos: User y Card.

Card aquí es distinta a core/card.py: esa es un dataclass en memoria para
el algoritmo puro; esta es la versión que vive en la base de datos, con
un id y conectada a un usuario dueño.
"""

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    cards = relationship("Card", back_populates="owner", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    repetitions = Column(Integer, default=0, nullable=False)
    easiness_factor = Column(Float, default=2.5, nullable=False)
    interval = Column(Integer, default=0, nullable=False)
    due_date = Column(Date, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="cards")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "word": self.word,
            "translation": self.translation,
            "repetitions": self.repetitions,
            "easiness_factor": self.easiness_factor,
            "interval": self.interval,
            "due_date": self.due_date.isoformat(),
        }
