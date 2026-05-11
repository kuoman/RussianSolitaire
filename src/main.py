# src/main.py
import argparse
import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from solitaire.deck import Deck
from solitaire.tableau import Tableau
from solitaire.display import Display
from solitaire.game_registry import GameRegistry
from solitaire.game_file import GameFile

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    parser = argparse.ArgumentParser(description="Yukon Russian Solitaire")
    parser.add_argument("--debug", action="store_true", help="Reveal face-down cards")
    parser.add_argument("--no-save", action="store_true", help="Do not save game to file")
    parser.add_argument("--load", metavar="PATH", help="Load a saved game file")
    args = parser.parse_args()

    if args.load:
        tableau = GameFile.load(Path(args.load))
    else:
        deck = Deck()
        deck.shuffle()
        tableau = Tableau(deck)
        if not args.no_save:
            game_path = GameRegistry.next_game_path(date.today(), DATA_DIR)
            game_id = game_path.stem
            GameFile.save(tableau, game_path, game_id=game_id)
            print(f"Game saved to {game_path}")

    print(Display(tableau, debug=args.debug).render())


if __name__ == "__main__":
    main()
