from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.autoplay.autoplayer import Autoplayer


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


def make_game(*columns):
    tableau = _RawTableau([list(col) for col in columns])
    return Game(tableau)


def test_autoplay_returns_true_on_win():
    # K♠ in C1, all other 51 cards on foundations.
    game = make_game([face_up("♠", "K")], [], [], [], [], [], [])
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q"]:
        game.foundations.add(Card("♠", rank, face_up=True))
    for suit in ("♥", "♦", "♣"):
        for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            game.foundations.add(Card(suit, rank, face_up=True))
    outcome = Autoplayer(game).play()
    assert outcome == "true"
    assert game.is_won


def test_autoplay_returns_false_when_stranded():
    # Two stranded cards, no legal moves.
    game = make_game(
        [face_up("♠", "5")],
        [face_up("♥", "9")],
        [], [], [], [], [],
    )
    outcome = Autoplayer(game).play()
    assert outcome == "false"
    assert not game.is_won
    assert game.total_moves == 0


def test_autoplay_plays_through_simple_sequence():
    # Aces face-up in two columns, foundations empty.
    # Autoplay should put both aces on foundations.
    game = make_game(
        [face_up("♠", "A")],
        [face_up("♥", "A")],
        [], [], [], [], [],
    )
    outcome = Autoplayer(game).play()
    # After both aces moved, no more legal moves (other columns empty), so "false".
    assert outcome == "false"
    assert game.foundations.for_suit("♠").size == 1
    assert game.foundations.for_suit("♥").size == 1
    assert game.total_moves == 2


def test_autoplay_aborts_on_max_moves_cap():
    # Setup: a game that allows multiple moves. Cap=1 means after one move autoplay aborts.
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [],
        [face_up("♠", "A")],
        [], [], [],
    )
    outcome = Autoplayer(game, max_moves=1).play()
    assert outcome == "aborted"
    assert game.total_moves == 1


def test_autoplayer_uses_provided_strategy():
    class StubStrategy:
        def __init__(self):
            self.calls = 0

        def select(self, game, visible_moves):
            self.calls += 1
            return visible_moves[0]

    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    stub = StubStrategy()
    Autoplayer(game, strategy=stub).play()
    assert stub.calls >= 1
