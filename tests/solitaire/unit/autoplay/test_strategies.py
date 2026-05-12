from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.autoplay.strategies.non_blocking import NonBlockingStrategy
from solitaire.autoplay.strategies.nply import NplyStrategy


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


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


def test_non_blocking_does_not_cycle_forever():
    # Setup: A♠ alone on C1, foundations empty. Only legal move: A♠ → foundation.
    # After applying, no legal moves. Outcome should be "false" (lost — game ended,
    # not "aborted" — cap hit).
    from solitaire.autoplay.autoplayer import Autoplayer

    tableau = _RawTableau([
        [Card("♠", "A", face_up=True)],
        [], [], [], [], [], [],
    ])
    game = Game(tableau)
    outcome = Autoplayer(game, strategy=NonBlockingStrategy(), max_moves=100).play()
    assert outcome == "false"
    assert game.foundations.for_suit("♠").size == 1


def test_non_blocking_makes_progress_with_multiple_aces():
    # Aces in C1, C2, C3, C4. All can go to foundation (4 separate moves).
    # Strategy should play all four without cycling.
    from solitaire.autoplay.autoplayer import Autoplayer

    tableau = _RawTableau([
        [Card("♠", "A", face_up=True)],
        [Card("♥", "A", face_up=True)],
        [Card("♦", "A", face_up=True)],
        [Card("♣", "A", face_up=True)],
        [], [], [],
    ])
    game = Game(tableau)
    outcome = Autoplayer(game, strategy=NonBlockingStrategy(), max_moves=100).play()
    assert game.foundations.total_cards == 4
    assert outcome == "false"


def test_non_blocking_prefers_foundation_when_future_counts_tie():
    # Setup: K♥ in C1 sitting on a face-down card (so K♥ is not anchored),
    # A♠ in C2, C3..C7 empty.
    # Visible moves: K♥ to each of C3..C7 (5 column moves), and A♠ → foundation.
    # All six moves yield the same future-move count (6), so without the
    # foundation bonus the first move (a K♥ shuffle) would win the tie.
    # The bonus tips the scales toward the foundation move.
    game = make_game(
        [face_down("♣", "5"), face_up("♥", "K")],
        [face_up("♠", "A")],
        [], [], [], [], [],
    )
    visible = [
        Move(0, 1, ColumnDestination(2)),
        Move(0, 1, ColumnDestination(3)),
        Move(0, 1, ColumnDestination(4)),
        Move(0, 1, ColumnDestination(5)),
        Move(0, 1, ColumnDestination(6)),
        Move(1, 1, FoundationDestination()),
    ]
    chosen = NonBlockingStrategy().select(game, visible)
    assert chosen.destination.is_foundation()
    assert chosen.source_column == 1


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
