from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.display import Display
from solitaire.repl.repl import Repl


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def make_game(*columns):
    tableau = _RawTableau([list(col) for col in columns])
    return Game(tableau)


def make_repl(game, inputs):
    """inputs is a list of strings to feed; output_fn captures output."""
    iterator = iter(inputs)
    captured = []

    def fake_input(prompt=""):
        return next(iterator)

    def fake_output(s):
        captured.append(s)

    repl = Repl(game, Display(game.tableau), input_fn=fake_input, output_fn=fake_output)
    return repl, captured


def test_repl_renders_tableau_then_quits_on_q():
    game = make_game([face_up("♠", "A")])
    repl, captured = make_repl(game, ["q"])
    repl.run()
    rendered = "\n".join(captured)
    assert "C1" in rendered  # tableau header was printed


def test_repl_applies_legal_move():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["7h c2 moved to c1", "q"])
    repl.run()
    assert len(game.moves) == 1
    assert game.tableau.columns[0][-1].rank == "7"
    assert game.tableau.columns[1] == []


def test_repl_rejects_illegal_move_with_message():
    game = make_game(
        [face_up("♥", "9")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["7h c2 moved to c1", "q"])
    repl.run()
    assert len(game.moves) == 0
    rendered = "\n".join(captured)
    assert (
        "illegal" in rendered.lower()
        or "cannot" in rendered.lower()
        or "not legal" in rendered.lower()
    )


def test_repl_help_command_prints_help():
    game = make_game([face_up("♠", "A")])
    repl, captured = make_repl(game, ["?", "q"])
    repl.run()
    rendered = "\n".join(captured)
    assert "moved to" in rendered or "MOVE" in rendered.upper()


def test_repl_handles_empty_input():
    game = make_game([face_up("♠", "A")])
    repl, captured = make_repl(game, ["", "q"])
    # Should not crash on empty input
    repl.run()


def test_repl_announces_win_after_winning_move():
    game = make_game([face_up("♠", "K")])
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q"]:
        game.foundations.add(Card("♠", rank, face_up=True))
    for suit in ("♥", "♦", "♣"):
        for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            game.foundations.add(Card(suit, rank, face_up=True))
    repl, captured = make_repl(game, ["Ks c1 moved to f", "q"])
    repl.run()
    assert game.is_won is True
    rendered = "\n".join(captured)
    assert (
        "won" in rendered.lower()
        or "win" in rendered.lower()
        or "congrat" in rendered.lower()
    )
