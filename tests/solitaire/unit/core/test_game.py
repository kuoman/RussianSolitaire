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


def test_can_apply_is_true_for_legal_move():
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert game.can_apply(move) is True


def test_can_apply_is_false_for_illegal_move():
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♠", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert game.can_apply(move) is False


def test_apply_moves_card_to_destination_column():
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    game.apply(move)
    assert tableau.columns[0] == []
    assert len(tableau.columns[1]) == 2
    assert tableau.columns[1][0].rank == "8"
    assert tableau.columns[1][0].suit == "♥"
    assert tableau.columns[1][1].rank == "7"
    assert tableau.columns[1][1].suit == "♥"


def test_apply_appends_move_to_history():
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    game.apply(move)
    assert len(game.moves) == 1
    assert game.moves[0] is move
