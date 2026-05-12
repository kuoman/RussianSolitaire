# src/main.py
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from solitaire.core.deck import Deck
from solitaire.core.game import Game
from solitaire.core.tableau import Tableau
from solitaire.display import Display
from solitaire.persistence.game_registry import GameRegistry
from solitaire.persistence.game_file import GameFile
from solitaire.repl.repl import Repl

DATA_DIR = Path(__file__).parent.parent / "data"


def _load_tableau(path_str: str):
    path = Path(path_str)
    try:
        return GameFile(path, game_id=path.stem).load()
    except FileNotFoundError:
        print(f"Error: save file not found: {path_str}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: malformed save file: {e}", file=sys.stderr)
        sys.exit(1)


def _new_tableau(no_save: bool):
    deck = Deck()
    deck.shuffle()
    tableau = Tableau(deck)
    if not no_save:
        game_path = GameRegistry.next_game_path(date.today(), DATA_DIR)
        GameFile(game_path, game_id=game_path.stem).save(tableau)
        print(f"Game saved to {game_path}")
    return tableau


def main():
    parser = argparse.ArgumentParser(description="Yukon Russian Solitaire")
    parser.add_argument("--debug", action="store_true", help="Reveal face-down cards")
    parser.add_argument("--no-save", action="store_true", help="Do not save game to file")
    parser.add_argument("--load", metavar="PATH", help="Load a saved game file")
    args = parser.parse_args()

    tableau = _load_tableau(args.load) if args.load else _new_tableau(args.no_save)
    game = Game(tableau)
    display = Display(tableau, debug=args.debug)
    Repl(game, display).run()


if __name__ == "__main__":
    main()
