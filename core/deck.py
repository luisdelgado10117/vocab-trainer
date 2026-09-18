"""
Deck: la colección completa de tarjetas de vocabulario.

Por ahora guardamos todo en un archivo JSON (no una base de datos todavía,
eso lo dejamos para cuando esto se convierta en API). Un archivo JSON es
perfecto para esta fase: simple, legible, y suficiente para un solo usuario
usando la consola.
"""

import json
from datetime import date
from pathlib import Path

from core.card import Card


class Deck:
    """Maneja el conjunto de tarjetas: agregar, listar, guardar y cargar."""

    def __init__(self):
        self.cards: list[Card] = []

    def add_card(self, word: str, translation: str) -> Card:
        card = Card(word=word, translation=translation)
        self.cards.append(card)
        return card

    def due_cards(self, today: date | None = None) -> list[Card]:
        """Devuelve solo las tarjetas que ya toca repasar hoy."""
        return [card for card in self.cards if card.is_due(today)]

    def save(self, path: str) -> None:
        """Guarda todas las tarjetas en un archivo JSON."""
        data = [card.to_dict() for card in self.cards]
        Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False))

    @classmethod
    def load(cls, path: str) -> "Deck":
        """Carga las tarjetas desde un archivo JSON. Si no existe, empieza vacío."""
        deck = cls()
        file_path = Path(path)

        if file_path.exists():
            data = json.loads(file_path.read_text())
            deck.cards = [Card.from_dict(item) for item in data]

        return deck
