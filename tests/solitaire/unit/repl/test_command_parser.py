from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.core.game import Game
from solitaire.repl.command_parser import CommandParser


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def make_game(*columns):
    tableau = _RawTableau([list(col) for col in columns])
    return Game(tableau)


def test_empty_input_is_noop():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    assert parser.parse("") == ("noop",)


def test_whitespace_only_is_noop():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    assert parser.parse("   ") == ("noop",)


def test_q_is_quit():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    assert parser.parse("q") == ("quit",)


def test_quit_word_is_quit():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    assert parser.parse("quit") == ("quit",)


def test_question_mark_is_help():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    assert parser.parse("?") == ("help",)


def test_help_word_is_help():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    assert parser.parse("help") == ("help",)


def test_unrecognized_input_returns_error():
    parser = CommandParser(make_game([face_up("♠", "A")]))
    result = parser.parse("foobar")
    assert result[0] == "error"
    assert isinstance(result[1], str)


def test_parse_simple_card_to_column():
    # 7h c2 moved to c5 — single card 7♥ from C2 to C5
    game = make_game(
        [face_up("♥", "8")],          # C1
        [face_up("♥", "7")],          # C2 — has 7♥ at top
        [], [], [],                    # C3, C4, C5
        [], [],
    )
    parser = CommandParser(game)
    kind, move = parser.parse("7h c2 moved to c5")
    assert kind == "move"
    assert move.source_column == 1
    assert move.count == 1
    assert move.destination.is_column() is True
    assert move.destination.column_index() == 4


def test_parse_unicode_suit_symbol_works():
    game = make_game(
        [face_up("♥", "8")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    parser = CommandParser(game)
    kind, move = parser.parse("7♥ c2 moved to c5")
    assert kind == "move"


def test_parse_move_to_foundation():
    game = make_game([face_up("♠", "A")])
    parser = CommandParser(game)
    kind, move = parser.parse("As c1 moved to f")
    assert kind == "move"
    assert move.source_column == 0
    assert move.count == 1
    assert move.destination.is_foundation() is True


def test_parse_stack_move_infers_count():
    game = make_game(
        [],                                # C1
        [face_up("♠", "5"), face_up("♥", "8"), face_up("♣", "7"), face_up("♦", "6")],
        [face_up("♣", "8")],               # C3
        [], [], [], [],
    )
    parser = CommandParser(game)
    kind, move = parser.parse("7c c2 moved to c3")
    assert kind == "move"
    assert move.source_column == 1
    assert move.count == 2  # 7♣ at index 2, len 4, count = 4-2 = 2


def test_parse_card_not_in_source_column_returns_error():
    game = make_game(
        [face_up("♠", "A")],
        [face_up("♥", "7")],
        [], [], [], [], [],
    )
    parser = CommandParser(game)
    kind, msg = parser.parse("7s c2 moved to c5")
    assert kind == "error"


def test_parse_face_down_card_in_source_column_returns_error():
    game = make_game(
        [Card("♥", "7", face_up=False), face_up("♥", "8")],
        [], [], [], [], [], [],
    )
    parser = CommandParser(game)
    kind, msg = parser.parse("7h c1 moved to c2")
    assert kind == "error"


def test_parse_invalid_card_format_returns_error():
    game = make_game([face_up("♠", "A")])
    parser = CommandParser(game)
    kind, msg = parser.parse("XX c1 moved to c2")
    assert kind == "error"


def test_parse_invalid_source_column_returns_error():
    game = make_game([face_up("♠", "A")])
    parser = CommandParser(game)
    kind, msg = parser.parse("As cX moved to f")
    assert kind == "error"


def test_parse_missing_moved_to_phrase_returns_error():
    game = make_game([face_up("♠", "A")])
    parser = CommandParser(game)
    kind, msg = parser.parse("As c1 to f")
    assert kind == "error"
