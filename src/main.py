# src/main.py
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

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
        try:
            tableau = GameFile(Path(args.load), game_id=Path(args.load).stem).load()
        except FileNotFoundError:
            print(f"Error: save file not found: {args.load}", file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: malformed save file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        deck = Deck()
        deck.shuffle()
        tableau = Tableau(deck)
        if not args.no_save:
            game_path = GameRegistry.next_game_path(date.today(), DATA_DIR)
            game_id = game_path.stem
            GameFile(game_path, game_id=game_id).save(tableau)
            print(f"Game saved to {game_path}")

    print(Display(tableau, debug=args.debug).render())


if __name__ == "__main__":
    main()
