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


def make_tableau(*columns):
    return _RawTableau([list(col) for col in columns])


def test_move_with_count_zero_is_illegal():
    tableau = make_tableau([face_up("♠", "A")])
    foundations = Foundations()
    move = Move(source_column=0, count=0, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_with_negative_count_is_illegal():
    tableau = make_tableau([face_up("♠", "A")])
    foundations = Foundations()
    move = Move(source_column=0, count=-1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_with_source_column_out_of_range_is_illegal():
    tableau = make_tableau([face_up("♠", "A")])
    foundations = Foundations()
    move = Move(source_column=99, count=1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_with_count_larger_than_column_is_illegal():
    tableau = make_tableau([face_up("♠", "A")])
    foundations = Foundations()
    move = Move(source_column=0, count=2, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_with_face_down_source_card_is_illegal():
    tableau = make_tableau(
        [face_down("♣", "5"), face_up("♥", "8"), face_up("♠", "9")],
        [face_up("♥", "10")],
    )
    # count=3 would include the face-down 5♣ as the topmost — illegal
    foundations = Foundations()
    move = Move(source_column=0, count=3, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_to_column_with_matching_suit_one_rank_lower_is_legal():
    # Move 7♥ onto 8♥
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is True


def test_move_to_column_with_wrong_suit_is_illegal():
    # 7♥ cannot go on 8♠
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♠", "8")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_to_column_with_wrong_rank_is_illegal():
    # 7♥ cannot go on 9♥
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "9")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_stack_to_column_uses_topmost_card_for_validation():
    # Source column has 7♥ then 6♠ then 5♥ as last three face-up
    # Destination has 8♥ on top
    # count=3 means moving [7♥, 6♠, 5♥], topmost is 7♥, lands on 8♥ → legal
    tableau = make_tableau(
        [face_up("♥", "7"), face_up("♠", "6"), face_up("♥", "5")],
        [face_up("♥", "8")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=3, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is True


def test_king_to_empty_column_is_legal():
    tableau = make_tableau(
        [face_up("♠", "K")],
        [],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is True


def test_non_king_to_empty_column_is_illegal():
    tableau = make_tableau(
        [face_up("♠", "5")],
        [],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is False


def test_king_led_stack_to_empty_column_is_legal():
    # Stack [K♠, Q♥, J♠] → empty column. Topmost is K♠ → legal.
    tableau = make_tableau(
        [face_up("♠", "K"), face_up("♥", "Q"), face_up("♠", "J")],
        [],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=3, destination=ColumnDestination(1))
    assert move.is_legal_on(tableau, foundations) is True


def test_move_to_same_column_is_illegal():
    # source_column == destination column doesn't make sense
    tableau = make_tableau(
        [face_up("♥", "7"), face_up("♥", "8")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(0))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_to_column_out_of_range_is_illegal():
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=ColumnDestination(99))
    assert move.is_legal_on(tableau, foundations) is False


def test_move_ace_to_empty_foundation_is_legal():
    tableau = make_tableau([face_up("♠", "A")])
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    assert move.is_legal_on(tableau, foundations) is True


def test_move_non_ace_to_empty_foundation_is_illegal():
    tableau = make_tableau([face_up("♠", "5")])
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    assert move.is_legal_on(tableau, foundations) is False


def test_move_two_to_foundation_with_ace_is_legal():
    tableau = make_tableau([face_up("♠", "2")])
    foundations = Foundations()
    foundations.add(face_up("♠", "A"))
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    assert move.is_legal_on(tableau, foundations) is True


def test_move_to_foundation_with_count_greater_than_one_is_illegal():
    # Only single cards go to foundation
    tableau = make_tableau(
        [face_up("♠", "A"), face_up("♠", "2")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=2, destination=FoundationDestination())
    assert move.is_legal_on(tableau, foundations) is False


def test_move_to_foundation_must_use_deepest_card():
    # Source column ends in ...8♥, A♠. Move count=1 takes the A♠ — that's legal.
    # But if we tried count=1 from a non-bottom card it shouldn't be possible to address
    # since source card is always determined by count from the bottom.
    # This test confirms: count=1 always picks the deepest card.
    tableau = make_tableau(
        [face_up("♥", "8"), face_up("♠", "A")],
    )
    foundations = Foundations()
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    assert move.is_legal_on(tableau, foundations) is True


def test_describe_single_card_move_to_column():
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    move = Move(source_column=1, count=1, destination=ColumnDestination(0))
    assert move.describe(tableau) == "7♥ from C2 moved to C1"


def test_describe_stack_move():
    tableau = make_tableau(
        [face_up("♣", "8")],
        [face_up("♣", "7"), face_up("♦", "6")],
    )
    move = Move(source_column=1, count=2, destination=ColumnDestination(0))
    assert move.describe(tableau) == "7♣ from C2 moved to C1"


def test_describe_foundation_move():
    tableau = make_tableau([face_up("♠", "A")])
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    assert move.describe(tableau) == "A♠ from C1 moved to foundation"
