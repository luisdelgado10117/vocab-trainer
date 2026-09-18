"""
Interfaz de consola para el entrenador de vocabulario.

Este archivo es el "punto de entrada": aquí se conecta todo lo que
construimos (Card, Deck, review_card) con algo que tú puedes usar de
verdad, escribiendo en la terminal.
"""

from datetime import date

from core.deck import Deck
from core.scheduler import review_card

DECK_FILE = "data/deck.json"


def menu_principal(deck: Deck) -> None:
    while True:
        print("\n--- Entrenador de vocabulario ---")
        print("1. Agregar palabra nueva")
        print("2. Repasar palabras pendientes")
        print("3. Ver todas las palabras")
        print("4. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            agregar_palabra(deck)
        elif opcion == "2":
            repasar_pendientes(deck)
        elif opcion == "3":
            ver_todas(deck)
        elif opcion == "4":
            deck.save(DECK_FILE)
            print("Progreso guardado. ¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


def agregar_palabra(deck: Deck) -> None:
    word = input("Palabra en inglés: ").strip()
    translation = input("Traducción: ").strip()

    if not word or not translation:
        print("Ambos campos son obligatorios.")
        return

    deck.add_card(word, translation)
    deck.save(DECK_FILE)
    print(f"Se agregó '{word}' -> '{translation}'.")


def repasar_pendientes(deck: Deck) -> None:
    pendientes = deck.due_cards()

    if not pendientes:
        print("No tienes palabras pendientes de repaso por hoy. ¡Buen trabajo!")
        return

    print(f"Tienes {len(pendientes)} palabra(s) para repasar.")

    for card in pendientes:
        print(f"\nPalabra: {card.word}")
        input("Presiona Enter para ver la traducción...")
        print(f"Traducción: {card.translation}")

        quality = pedir_calificacion()
        review_card(card, quality, today=date.today())
        print(f"Próximo repaso en {card.interval} día(s) (el {card.due_date}).")

    deck.save(DECK_FILE)
    print("\nProgreso guardado.")


def pedir_calificacion() -> int:
    """Pide al usuario que se autocalifique, validando que sea un número del 0 al 5."""
    print("¿Qué tan bien la recordaste? (0 = nada, 3 = con esfuerzo, 5 = perfecto)")

    while True:
        respuesta = input("Calificación (0-5): ").strip()
        try:
            quality = int(respuesta)
            if 0 <= quality <= 5:
                return quality
            print("Debe ser un número entre 0 y 5.")
        except ValueError:
            print("Escribe un número válido.")


def ver_todas(deck: Deck) -> None:
    if not deck.cards:
        print("Todavía no tienes palabras agregadas.")
        return

    for card in deck.cards:
        estado = "PENDIENTE" if card.is_due() else f"próximo repaso: {card.due_date}"
        print(f"- {card.word} -> {card.translation} ({estado})")


if __name__ == "__main__":
    deck = Deck.load(DECK_FILE)
    menu_principal(deck)
