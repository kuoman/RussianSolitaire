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


def test_apply_moves_stack_to_destination_column():
    tableau = make_tableau(
        [face_up("♥", "7"), face_up("♠", "6"), face_up("♥", "5")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=3, destination=ColumnDestination(1))
    game.apply(move)
    assert tableau.columns[0] == []
    assert len(tableau.columns[1]) == 4
    # Stack preserved in order: 8♥, 7♥, 6♠, 5♥
    ranks = [c.rank for c in tableau.columns[1]]
    assert ranks == ["8", "7", "6", "5"]


def test_apply_flips_newly_exposed_face_down_card():
    # Source column: [↓5♠, 7♥]. Move 7♥ to column with 8♥.
    # After move, source column should be [5♠ face-up].
    tableau = make_tableau(
        [face_down("♠", "5"), face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    game.apply(move)
    assert len(tableau.columns[0]) == 1
    assert tableau.columns[0][0].rank == "5"
    assert tableau.columns[0][0].suit == "♠"
    assert tableau.columns[0][0].face_up is True


def test_apply_does_not_flip_when_exposed_card_already_face_up():
    tableau = make_tableau(
        [face_up("♠", "5"), face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    game.apply(move)
    assert tableau.columns[0][0].face_up is True
    assert tableau.columns[0][0].rank == "5"


def test_apply_leaves_empty_source_column_empty():
    tableau = make_tableau(
        [face_up("♥", "7")],
        [face_up("♥", "8")],
    )
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    game.apply(move)
    assert tableau.columns[0] == []


def test_apply_moves_card_to_foundation():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    game.apply(move)
    assert tableau.columns[0] == []
    assert game.foundations.total_cards == 1
    assert game.foundations.for_suit("♠").size == 1


def test_apply_to_foundation_appends_to_history():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    game.apply(move)
    assert len(game.moves) == 1
    assert game.moves[0] is move


def test_apply_to_foundation_auto_flips_exposed_card():
    tableau = make_tableau([face_down("♣", "5"), face_up("♠", "A")])
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    game.apply(move)
    assert len(tableau.columns[0]) == 1
    assert tableau.columns[0][0].face_up is True
    assert tableau.columns[0][0].rank == "5"


def test_is_won_when_all_52_cards_on_foundations():
    # Build a game where the foundations are already complete
    tableau = make_tableau([])
    game = Game(tableau)
    for suit in ("♠", "♥", "♦", "♣"):
        for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            game.foundations.add(face_up(suit, rank))
    assert game.is_won is True


def test_apply_captures_move_description():
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    game = Game(tableau)
    move = Move(source_column=1, count=1, destination=ColumnDestination(0))
    game.apply(move)
    assert game.move_descriptions == ["7♥ from C2 moved to C1"]


def test_apply_captures_description_before_mutation():
    # If we captured AFTER mutation, the source column would be empty and
    # describe() would fail. This test confirms pre-mutation timing.
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    game = Game(tableau)
    move = Move(source_column=1, count=1, destination=ColumnDestination(0))
    game.apply(move)
    # Source column is now empty; description must already be captured.
    assert tableau.columns[1] == []
    assert game.move_descriptions[0] == "7♥ from C2 moved to C1"


def test_total_moves_starts_at_zero():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    assert game.total_moves == 0


def test_total_moves_increments_on_apply():
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    game = Game(tableau)
    move = Move(source_column=1, count=1, destination=ColumnDestination(0))
    game.apply(move)
    assert game.total_moves == 1


def test_prior_moves_seed_descriptions_and_total():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau, prior_moves=["X", "Y", "Z"])
    assert game.move_descriptions == ["X", "Y", "Z"]
    assert game.total_moves == 3


def test_prior_moves_combined_with_session_moves():
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    game = Game(tableau, prior_moves=["X", "Y"])
    move = Move(source_column=1, count=1, destination=ColumnDestination(0))
    game.apply(move)
    assert game.move_descriptions == ["X", "Y", "7♥ from C2 moved to C1"]
    assert game.total_moves == 3


def test_snapshot_then_restore_returns_to_original_state():
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    game = Game(tableau)
    move = Move(source_column=1, count=1, destination=ColumnDestination(0))
    snapshot = game.snapshot()
    game.apply(move)
    assert game.total_moves == 1
    game.restore(snapshot)
    assert game.total_moves == 0
    assert tableau.columns[0] == [face_up("♥", "8")]
    assert tableau.columns[1] == [face_up("♥", "7")]


def test_snapshot_captures_foundations_state():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    move = Move(source_column=0, count=1, destination=FoundationDestination())
    snapshot = game.snapshot()
    game.apply(move)
    assert game.foundations.total_cards == 1
    game.restore(snapshot)
    assert game.foundations.total_cards == 0


def test_game_stores_metadata():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau, metadata={"c1_special": "A"})
    assert game.metadata == {"c1_special": "A"}


def test_game_metadata_defaults_empty():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau)
    assert game.metadata == {}


def test_game_metadata_is_defensive_copy_on_input():
    tableau = make_tableau([face_up("♠", "A")])
    original = {"c1_special": "A"}
    game = Game(tableau, metadata=original)
    original["c1_special"] = "K"  # mutating input must not affect the game
    assert game.metadata == {"c1_special": "A"}


def test_game_metadata_is_defensive_copy_on_output():
    tableau = make_tableau([face_up("♠", "A")])
    game = Game(tableau, metadata={"c1_special": "A"})
    game.metadata["c1_special"] = "K"  # mutating output must not affect the game
    assert game.metadata == {"c1_special": "A"}


def test_snapshot_captures_move_descriptions():
    tableau = make_tableau(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
    )
    game = Game(tableau)
    snapshot = game.snapshot()
    game.apply(Move(1, 1, ColumnDestination(0)))
    assert game.move_descriptions == ["7♥ from C2 moved to C1"]
    game.restore(snapshot)
    assert game.move_descriptions == []
