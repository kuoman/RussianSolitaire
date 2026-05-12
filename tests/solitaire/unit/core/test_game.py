from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.foundations import Foundations
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.core.game import Game


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


def make_tableau(*columns):
    return _RawTableau([list(col) for col in columns])


def test_new_game_has_empty_move_history():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    assert game.moves == []


def test_new_game_exposes_tableau():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    assert game.tableau is tableau


def test_new_game_creates_empty_foundations_by_default():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    assert game.foundations.total_cards == 0


def test_new_game_accepts_foundations_argument():
    tableau = make_tableau([face_up("♠", "A")])
    foundations = Foundations()
    game = Game(tableau, foundations)
    assert game.foundations is foundations


def test_new_game_is_not_won():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    assert game.is_won is False
