from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.autoplay.strategies.reveal_first import RevealFirstStrategy


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


def make_game(*columns):
    return Game(_RawTableau([list(col) for col in columns]))


def test_returns_a_move_from_visible_list():
    game = make_game([face_up("♠", "A")])
    only = Move(0, 1, FoundationDestination())
    chosen = RevealFirstStrategy().select(game, [only])
    assert chosen is only


def test_prefers_revealing_move_over_non_revealing():
    # Two moves: one reveals a face-down card, the other doesn't.
    #
    # Setup:
    #   C1: [↓5♠, 7♥]   (move 7♥ to C2 reveals 5♠)
    #   C2: [8♥]        (destination for 7♥)
    #   C3: [Q♣]        (move Q♣ to K♣ on C4 reveals nothing — only 1 card in C3)
    #   C4: [K♣]
    game = make_game(
        [face_down("♠", "5"), face_up("♥", "7")],
        [face_up("♥", "8")],
        [face_up("♣", "Q")],
        [face_up("♣", "K")],
        [], [], [],
    )
    reveal_move = Move(source_column=0, count=1, destination=ColumnDestination(1))
    non_reveal_move = Move(source_column=2, count=1, destination=ColumnDestination(3))
    chosen = RevealFirstStrategy().select(game, [non_reveal_move, reveal_move])
    assert chosen is reveal_move


def test_prefers_revealing_move_even_over_foundation():
    # Foundation move (without reveal) vs. reveal-from-tableau move.
    # The 100-point reveal bonus dwarfs the 1.5 foundation bonus, so reveal wins.
    #
    # Setup:
    #   C1: [face_up("♠", "A")]   (A♠ → foundation, no reveal — only 1 card in column)
    #   C2: [↓5♠, face_up("♥", "7")]  (7♥ → 8♥ on C3 reveals 5♠)
    #   C3: [face_up("♥", "8")]
    game = make_game(
        [face_up("♠", "A")],
        [face_down("♠", "5"), face_up("♥", "7")],
        [face_up("♥", "8")],
        [], [], [], [],
    )
    foundation_move = Move(source_column=0, count=1, destination=FoundationDestination())
    reveal_move = Move(source_column=1, count=1, destination=ColumnDestination(2))
    chosen = RevealFirstStrategy().select(game, [foundation_move, reveal_move])
    assert chosen is reveal_move


def test_when_no_reveal_available_picks_foundation_over_column():
    # Two non-reveal options: foundation move + column move.
    # Strategy should still prefer foundation (1.5 bonus vs 0).
    #
    # Setup:
    #   C1: [face_up("♠", "A")]   (A♠ → foundation, no reveal)
    #   C2: [face_up("♥", "7")]   (7♥ → C3 onto 8♥, no reveal — only 1 card)
    #   C3: [face_up("♥", "8")]
    game = make_game(
        [face_up("♠", "A")],
        [face_up("♥", "7")],
        [face_up("♥", "8")],
        [], [], [], [],
    )
    foundation_move = Move(source_column=0, count=1, destination=FoundationDestination())
    column_move = Move(source_column=1, count=1, destination=ColumnDestination(2))
    chosen = RevealFirstStrategy().select(game, [foundation_move, column_move])
    # Foundation wins on the +1.5 bonus + same future-count tiebreak.
    # But future-count after foundation: 7♥ can still move to C3? Yes (still 8♥ there).
    # Future-count after column: 7♥ now on 8♥; A♠ still in C1 ready for foundation.
    # Both leave roughly the same future move count, so the foundation bonus tips it.
    assert chosen is foundation_move


def test_does_not_crash_when_count_equals_column_length():
    # Moving the entire column — no reveal possible (column becomes empty).
    # C1: [Q♣] (single non-king card), moving onto K♣ on C2.
    # count=1=len(C1), exercising the "count >= len(src_col)" branch.
    game = make_game(
        [face_up("♣", "Q")],
        [face_up("♣", "K")],
        [], [], [], [], [],
    )
    only = Move(source_column=0, count=1, destination=ColumnDestination(1))
    chosen = RevealFirstStrategy().select(game, [only])
    assert chosen is only
