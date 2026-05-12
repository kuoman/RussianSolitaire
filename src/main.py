# src/main.py
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from solitaire.autoplay.autoplayer import Autoplayer
from solitaire.autoplay.batch_runner import BatchRunner
from solitaire.autoplay.strategies.first_move import FirstMoveStrategy
from solitaire.autoplay.strategies.non_blocking import NonBlockingStrategy
from solitaire.autoplay.strategies.nply import NplyStrategy
from solitaire.core.deck import Deck
from solitaire.core.game import Game
from solitaire.core.tableau import Tableau
from solitaire.display import Display
from solitaire.persistence.game_analyzer import GameAnalyzer
from solitaire.persistence.game_registry import GameRegistry
from solitaire.persistence.game_file import GameFile
from solitaire.repl.repl import Repl

DATA_DIR = Path(__file__).parent.parent / "data"

OUTCOME_WORD = {"true": "won", "false": "lost", "aborted": "aborted (cap hit)"}


def _load_tableau(path_str: str):
    path = Path(path_str)
    try:
        tableau = GameFile(path, game_id=path.stem).load()
    except FileNotFoundError:
        print(f"Error: save file not found: {path_str}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: malformed save file: {e}", file=sys.stderr)
        sys.exit(1)
    save_target = GameFile(path, game_id=path.stem)
    metadata = getattr(tableau, "prior_metadata", {})
    return tableau, save_target, metadata


def _new_tableau(no_save: bool, strategy_label: str = "human"):
    deck = Deck()
    deck.shuffle()
    tableau = Tableau(deck)
    metadata = GameAnalyzer(tableau).analyse()
    if no_save:
        return tableau, None, metadata
    game_path = GameRegistry(DATA_DIR).next_game_path(date.today())
    save_target = GameFile(game_path, game_id=game_path.stem)
    save_target.save(tableau, metadata=metadata, strategy=strategy_label)
    print(f"Game saved to {game_path}")
    return tableau, save_target, metadata


def _build_strategy(strategy_name, depth):
    if strategy_name == "first":
        return FirstMoveStrategy()
    if strategy_name == "non-blocking":
        return NonBlockingStrategy()
    if strategy_name == "nply":
        return NplyStrategy(depth=depth)
    raise ValueError(f"unknown strategy: {strategy_name}")


def _strategy_label(args):
    if not args.autoplay and args.runs is None:
        return "human"
    if args.strategy == "nply":
        return f"nply-{args.depth}"
    return args.strategy


def _run_autoplay(game, save_target, strategy, strategy_label):
    outcome = Autoplayer(game, strategy=strategy).play()
    if save_target is not None:
        save_target.save(
            game.tableau,
            initial_tableau=game.initial_tableau,
            metadata=game.metadata,
            won=outcome,
            foundation_cards=game.foundations.total_cards,
            move_log=game.move_descriptions,
            strategy=strategy_label,
        )
    print(
        f"Result: {OUTCOME_WORD[outcome]} after {game.total_moves} moves "
        f"({game.foundations.total_cards} cards on foundations)"
    )


def _run_batch(args):
    if args.load:
        print("Error: --runs cannot be combined with --load", file=sys.stderr)
        sys.exit(1)

    strategy_label = _strategy_label(args)

    def run_one():
        deck = Deck()
        deck.shuffle()
        tableau = Tableau(deck)
        metadata = GameAnalyzer(tableau).analyse()
        game = Game(tableau, metadata=metadata)
        save_target = None
        if not args.no_save:
            game_path = GameRegistry(DATA_DIR).next_game_path(date.today())
            save_target = GameFile(game_path, game_id=game_path.stem)
            save_target.save(tableau, metadata=metadata, strategy=strategy_label)
        strategy = _build_strategy(args.strategy, args.depth)
        outcome = Autoplayer(game, strategy=strategy).play()
        if save_target is not None:
            save_target.save(
                game.tableau,
                initial_tableau=game.initial_tableau,
                metadata=metadata,
                won=outcome,
                foundation_cards=game.foundations.total_cards,
                move_log=game.move_descriptions,
                strategy=strategy_label,
            )
        return {
            "outcome": outcome,
            "moves": game.total_moves,
            "foundation_cards": game.foundations.total_cards,
        }

    runner = BatchRunner(args.runs, run_one)
    stats = runner.run()
    _print_summary(stats, args)


def _print_summary(stats, args):
    strategy_label = args.strategy
    if args.strategy == "nply":
        strategy_label = f"nply --depth {args.depth}"
    runs = stats["runs"]
    won = stats["won"]
    lost = stats["lost"]
    aborted = stats["aborted"]
    print(f"Strategy: {strategy_label}, runs: {runs}")
    if runs > 0:
        print(f"  Won:     {won:>3} ({won/runs*100:>4.1f}%)")
        print(f"  Lost:    {lost:>3} ({lost/runs*100:>4.1f}%)")
        print(f"  Aborted: {aborted:>3} ({aborted/runs*100:>4.1f}%)")
        print(f"  Avg moves: {stats['avg_moves']:.1f}")
        print(f"  Avg foundation cards: {stats['avg_foundation_cards']:.1f}")


def main():
    parser = argparse.ArgumentParser(description="Yukon Russian Solitaire")
    parser.add_argument("--debug", action="store_true", help="Reveal face-down cards")
    parser.add_argument("--no-save", action="store_true", help="Do not save game to file")
    parser.add_argument("--load", metavar="PATH", help="Load a saved game file")
    parser.add_argument("--autoplay", action="store_true", help="Autoplay until win or stuck")
    parser.add_argument(
        "--strategy",
        choices=["first", "non-blocking", "nply"],
        default="first",
        help="Autoplay strategy",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=1,
        help="Lookahead depth (nply only)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=None,
        help="Run autoplay N times and print summary",
    )
    args = parser.parse_args()

    if args.runs is not None and args.runs > 0:
        _run_batch(args)
        return

    strategy_label = _strategy_label(args)
    tableau, save_target, metadata = (
        _load_tableau(args.load) if args.load else _new_tableau(args.no_save, strategy_label)
    )
    prior_moves = getattr(tableau, "prior_moves", None)
    game = Game(tableau, prior_moves=prior_moves, metadata=metadata)

    if args.autoplay:
        strategy = _build_strategy(args.strategy, args.depth)
        _run_autoplay(game, save_target, strategy, strategy_label)
        return

    display = Display(tableau, debug=args.debug, foundations=game.foundations)
    Repl(game, display, save_target=save_target).run()


if __name__ == "__main__":
    main()
