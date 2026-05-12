from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.core.move import Move, ColumnDestination, FoundationDestination
from solitaire.autoplay.strategies.random_strategy import RandomStrategy


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def make_game(*columns):
    return Game(_RawTableau([list(col) for col in columns]))


def test_random_strategy_returns_a_legal_move_from_the_list():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    move_a = Move(1, 1, ColumnDestination(0))
    move_b = Move(0, 1, FoundationDestination())  # not actually legal but passed anyway as a list element
    visible = [move_a, move_b]
    chosen = RandomStrategy().select(game, visible)
    assert chosen in visible


def test_random_strategy_returns_only_choice_when_one_visible_move():
    game = make_game([face_up("♠", "A")])
    only = Move(0, 1, FoundationDestination())
    chosen = RandomStrategy().select(game, [only])
    assert chosen is only


def test_random_strategy_picks_each_move_at_least_once_over_many_trials():
    # With 1000 trials of choosing from 3 moves, each should be picked at least once.
    game = make_game([face_up("♠", "A")])
    a = Move(0, 1, FoundationDestination())
    b = Move(0, 1, ColumnDestination(1))
    c = Move(0, 1, ColumnDestination(2))
    visible = [a, b, c]
    strat = RandomStrategy()
    seen = set()
    for _ in range(1000):
        seen.add(id(strat.select(game, visible)))
    assert len(seen) == 3, "Expected all three moves to be picked at least once over 1000 trials"
