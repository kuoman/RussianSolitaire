from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.foundations import Foundations
from solitaire.core.move import Move, ColumnDestination, FoundationDestination


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


def test_column_destination_is_column():
    dest = ColumnDestination(3)
    assert dest.is_column() is True
    assert dest.is_foundation() is False


def test_column_destination_remembers_index():
    dest = ColumnDestination(5)
    assert dest.column_index() == 5


def test_column_destinations_equal_when_indexes_match():
    assert ColumnDestination(3) == ColumnDestination(3)
    assert ColumnDestination(3) != ColumnDestination(4)


def test_foundation_destination_is_foundation():
    dest = FoundationDestination()
    assert dest.is_foundation() is True
    assert dest.is_column() is False


def test_foundation_destinations_are_equal():
    assert FoundationDestination() == FoundationDestination()


def test_destinations_of_different_types_are_not_equal():
    assert ColumnDestination(3) != FoundationDestination()


def test_move_remembers_source_column():
    move = Move(source_column=2, count=3, destination=ColumnDestination(5))
    assert move.source_column == 2


def test_move_remembers_count():
    move = Move(source_column=2, count=3, destination=ColumnDestination(5))
    assert move.count == 3


def test_move_remembers_destination():
    dest = ColumnDestination(5)
    move = Move(source_column=2, count=3, destination=dest)
    assert move.destination == dest
