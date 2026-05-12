from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.autoplay.strategies.non_blocking import NonBlockingStrategy


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
