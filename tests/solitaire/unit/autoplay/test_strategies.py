from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.autoplay.strategies.non_blocking import NonBlockingStrategy
from solitaire.autoplay.strategies.nply import NplyStrategy


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def make_game(*columns):
    return Game(_RawTableau([list(col) for col in columns]))


def test_non_blocking_returns_a_move_when_multiple_available():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    visible = [Move(1, 1, ColumnDestination(0))]
    strat = NonBlockingStrategy()
    chosen = strat.select(game, visible)
    assert chosen in visible


def test_non_blocking_returns_first_when_only_one_legal_move():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    only_move = Move(1, 1, ColumnDestination(0))
    strat = NonBlockingStrategy()
    chosen = strat.select(game, [only_move])
    assert chosen is only_move


def test_nply_returns_a_move():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    only_move = Move(1, 1, ColumnDestination(0))
    chosen = NplyStrategy(depth=1).select(game, [only_move])
    assert chosen is only_move


def test_nply_rejects_zero_depth():
    import pytest
    with pytest.raises(ValueError):
        NplyStrategy(depth=0)


def test_nply_picks_winning_move_at_depth_1():
    # Setup: K♠ in C1, all other 51 cards on foundations. Picking the foundation
    # move wins. Even at depth=1 the strategy should pick it.
    game = make_game([face_up("♠", "K")], [], [], [], [], [], [])
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q"]:
        game.foundations.add(Card("♠", rank, face_up=True))
    for suit in ("♥", "♦", "♣"):
        for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            game.foundations.add(Card(suit, rank, face_up=True))
    visible = [Move(0, 1, FoundationDestination())]
    chosen = NplyStrategy(depth=1).select(game, visible)
    assert chosen is visible[0]
