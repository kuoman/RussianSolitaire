from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.core.move_filter import MoveFilter


def test_empty_input_returns_empty():
    assert MoveFilter([]).visible() == []


def test_keeps_lone_column_move():
    moves = [Move(0, 1, ColumnDestination(1))]
    assert MoveFilter(moves).visible() == moves


def test_keeps_lone_foundation_move():
    moves = [Move(0, 1, FoundationDestination())]
    assert MoveFilter(moves).visible() == moves


def test_drops_column_moves_when_foundation_move_exists_for_same_source():
    foundation = Move(0, 1, FoundationDestination())
    column = Move(0, 1, ColumnDestination(1))
    visible = MoveFilter([foundation, column]).visible()
    assert visible == [foundation]


def test_keeps_column_moves_for_different_sources():
    foundation_from_0 = Move(0, 1, FoundationDestination())
    column_from_1 = Move(1, 1, ColumnDestination(2))
    visible = MoveFilter([foundation_from_0, column_from_1]).visible()
    assert foundation_from_0 in visible
    assert column_from_1 in visible


def test_keeps_column_moves_when_count_differs():
    # Foundation requires count=1; a stack move with count=2 from same column should keep
    foundation = Move(0, 1, FoundationDestination())
    stack = Move(0, 2, ColumnDestination(1))
    visible = MoveFilter([foundation, stack]).visible()
    assert foundation in visible
    assert stack in visible
