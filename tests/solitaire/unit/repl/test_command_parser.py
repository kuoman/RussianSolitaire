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
