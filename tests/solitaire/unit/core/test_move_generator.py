from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.foundations import Foundations
from solitaire.core.game import Game
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.core.move_generator import MoveGenerator


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


def make_game(*columns):
    tableau = _RawTableau([list(col) for col in columns])
    return Game(tableau)


def test_no_legal_moves_returns_empty_list():
    game = make_game(
        [face_up("♠", "5")],
        [face_up("♥", "9")],
        [], [], [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    assert moves == []


def test_finds_single_card_to_column_move():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    assert len(moves) == 1
    assert moves[0].source_column == 1
    assert moves[0].count == 1
    assert moves[0].destination == ColumnDestination(0)


def test_finds_ace_to_empty_foundation_move():
    game = make_game(
        [face_up("♠", "A")],
        [], [], [], [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    foundation_moves = [m for m in moves if m.destination.is_foundation()]
    assert len(foundation_moves) == 1
    assert foundation_moves[0].source_column == 0


def test_finds_king_to_empty_column_move():
    game = make_game(
        [face_up("♠", "K")],
        [],
        [], [], [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    column_moves = [m for m in moves if m.destination.is_column()]
    assert len(column_moves) == 6


def test_finds_stack_moves():
    game = make_game(
        [face_up("♣", "8")],
        [face_up("♣", "7"), face_up("♦", "6")],
        [], [], [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    stack_moves = [m for m in moves if m.count == 2]
    assert any(m.source_column == 1 and m.destination == ColumnDestination(0) for m in stack_moves)


def test_does_not_include_face_down_cards_as_source():
    game = make_game(
        [face_down("♠", "5"), face_up("♥", "8")],
        [], [], [], [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    assert moves == []


def test_finds_multiple_destinations_for_same_card():
    game = make_game(
        [face_up("♠", "K")],
        [],
        [],
        [face_up("♥", "5")],
        [], [], [],
    )
    moves = MoveGenerator(game).legal_moves()
    column_moves = [m for m in moves if m.destination.is_column()]
    assert len(column_moves) == 5
