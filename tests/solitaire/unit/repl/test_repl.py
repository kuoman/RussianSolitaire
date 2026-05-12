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


def make_repl(game, inputs, save_target=None):
    """inputs is a list of strings to feed; output_fn captures output."""
    iterator = iter(inputs)
    captured = []

    def fake_input(prompt=""):
        return next(iterator)

    def fake_output(s):
        captured.append(s)

    repl = Repl(
        game,
        Display(game.tableau),
        input_fn=fake_input,
        output_fn=fake_output,
        save_target=save_target,
    )
    return repl, captured


class FakeSaveTarget:
    def __init__(self):
        self.calls = []

    _UNSET = object()

    def save(self, tableau, *, initial_tableau=None, metadata=None, won="unknown",
             foundation_cards=0, move_log=None, strategy=_UNSET):
        self.calls.append(
            {
                "tableau": tableau,
                "initial_tableau": initial_tableau,
                "metadata": metadata,
                "won": won,
                "foundation_cards": foundation_cards,
                "move_log": list(move_log) if move_log else [],
                "strategy": strategy if strategy is not FakeSaveTarget._UNSET else None,
            }
        )


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
    # Includes an Ace in C3 so MoveGenerator finds at least one legal move
    # (A♠ -> foundation), which prevents auto-exit-on-no-legal-moves and lets
    # the test verify the illegal-move rejection path.
    game = make_game(
        [face_up("♥", "9")],
        [face_up("♥", "7")],
        [face_up("♠", "A")],
        [], [], [], [],
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


def test_repl_lists_available_moves():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["q"])
    repl.run()
    rendered = "\n".join(captured)
    assert "Available moves" in rendered
    assert "7♥ from C2 moved to C1" in rendered


def test_repl_dispatches_pick():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["1", "q"])
    repl.run()
    assert len(game.moves) == 1
    assert game.tableau.columns[1] == []
    assert game.tableau.columns[0][-1].rank == "7"


def test_repl_pick_out_of_range_is_error():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["99", "q"])
    repl.run()
    assert len(game.moves) == 0
    rendered = "\n".join(captured)
    assert "out of range" in rendered.lower() or "choose" in rendered.lower()


def test_repl_no_legal_moves_message():
    game = make_game(
        [face_up("♠", "5")],
        [face_up("♥", "9")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["q"])
    repl.run()
    rendered = "\n".join(captured)
    assert "no legal moves" in rendered.lower() or "no available" in rendered.lower()


def test_repl_exits_loop_when_no_legal_moves():
    # Stranded cards. The Repl should print loss message and exit
    # WITHOUT needing input from the player.
    game = make_game(
        [face_up("♠", "5")],
        [face_up("♥", "9")],
        [], [], [], [], [],
    )
    # No inputs queued — if the repl tries to read input, the test will raise
    # StopIteration (because make_repl uses an iter() over the inputs list).
    repl, captured = make_repl(game, [])
    repl.run()  # Should NOT raise — should detect loss and return
    rendered = "\n".join(captured)
    assert "game over" in rendered.lower() or "no legal moves" in rendered.lower()


def test_repl_filters_out_column_move_when_foundation_move_available():
    # K♠ in C1 with ♠ A-Q already on foundation. K♠ can go to foundation
    # OR into any of the empty columns C2-C7. Expect only the foundation
    # move to be displayed.
    game = make_game([face_up("♠", "K")], [], [], [], [], [], [])
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q"]:
        game.foundations.add(Card("♠", rank, face_up=True))
    repl, captured = make_repl(game, ["q"])
    repl.run()
    rendered = "\n".join(captured)
    assert "K♠ from C1 moved to foundation" in rendered
    assert "K♠ from C1 moved to C2" not in rendered
    assert "K♠ from C1 moved to C3" not in rendered


def test_repl_keeps_column_moves_when_no_foundation_alternative():
    # 7♥ to 8♥ — column move only; foundation is empty so 7♥ cannot go there.
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    repl, captured = make_repl(game, ["q"])
    repl.run()
    rendered = "\n".join(captured)
    assert "7♥ from C2 moved to C1" in rendered


def test_repl_pick_uses_filtered_list():
    # K♠ to foundation (with ♠ A-Q already there). Without filter, foundation
    # would be one of many; with filter, picking 1 must apply the foundation move.
    game = make_game([face_up("♠", "K")], [], [], [], [], [], [])
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q"]:
        game.foundations.add(Card("♠", rank, face_up=True))
    repl, captured = make_repl(game, ["1", "q"])
    repl.run()
    assert game.foundations.for_suit("♠").size == 13


def test_repl_saves_on_quit_with_won_unknown():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, ["q"], save_target=save_target)
    repl.run()
    assert len(save_target.calls) == 1
    call = save_target.calls[0]
    assert call["won"] == "unknown"
    assert call["foundation_cards"] == 0
    assert call["move_log"] == []
    assert call["tableau"] is game.tableau


def test_repl_saves_on_win_with_won_true():
    game = make_game([face_up("♠", "K")])
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q"]:
        game.foundations.add(Card("♠", rank, face_up=True))
    for suit in ("♥", "♦", "♣"):
        for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            game.foundations.add(Card(suit, rank, face_up=True))
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, ["Ks c1 moved to f"], save_target=save_target)
    repl.run()
    assert game.is_won is True
    assert len(save_target.calls) == 1
    call = save_target.calls[0]
    assert call["won"] == "true"
    assert call["foundation_cards"] == 52
    assert call["move_log"] == ["K♠ from C1 moved to foundation"]


def test_repl_saves_on_loss_with_won_false():
    # Stranded cards. No legal moves exist — auto-exit triggers loss save.
    game = make_game(
        [face_up("♠", "5")],
        [face_up("♥", "9")],
        [], [], [], [], [],
    )
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, [], save_target=save_target)
    repl.run()
    assert len(save_target.calls) == 1
    call = save_target.calls[0]
    assert call["won"] == "false"
    assert call["foundation_cards"] == 0
    assert call["move_log"] == []


def test_repl_save_includes_prior_moves_in_log():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    # Seed prior moves (as if loaded from disk)
    game._prior_descriptions = ["X", "Y"]
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, ["1", "q"], save_target=save_target)
    repl.run()
    call = save_target.calls[0]
    assert call["move_log"] == ["X", "Y", "7♥ from C2 moved to C1"]


def test_repl_skips_save_when_save_target_is_none():
    game = make_game([face_up("♠", "A")])
    repl, _ = make_repl(game, ["q"], save_target=None)
    # Just verify run() doesn't blow up when save_target is None
    repl.run()


def test_repl_passes_game_metadata_to_save_on_end():
    tableau = _RawTableau([[face_up("♠", "A")], [], [], [], [], [], []])
    deal_metadata = {"c1_special": "A", "kings_on_home_row": 0}
    game = Game(tableau, metadata=deal_metadata)
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, ["q"], save_target=save_target)
    repl.run()
    assert len(save_target.calls) == 1
    assert save_target.calls[0]["metadata"] == deal_metadata


def test_repl_passes_human_strategy_to_save():
    game = make_game([face_up("♠", "A")])
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, ["q"], save_target=save_target)
    repl.run()
    assert save_target.calls[0]["strategy"] == "human"


def test_repl_passes_initial_tableau_to_save():
    game = make_game([face_up("♠", "A")])
    save_target = FakeSaveTarget()
    repl, _ = make_repl(game, ["q"], save_target=save_target)
    repl.run()
    assert save_target.calls[0]["initial_tableau"] is not None
