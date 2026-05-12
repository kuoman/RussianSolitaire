# tests/solitaire/characterization/test_game_char.py
# PROTECTED: do not modify without explicit human permission

import tempfile
from pathlib import Path
from solitaire.core.deck import Deck
from solitaire.core.tableau import Tableau
from solitaire.persistence.game_file import GameFile


def make_tableau():
    deck = Deck()
    deck.shuffle()
    return Tableau(deck)


def round_trip(tableau):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        gf = GameFile(path, game_id="2026-05-11-000001")
        gf.save(tableau)
        return gf.load()


def test_save_then_load_preserves_all_52_cards():
    original = make_tableau()
    loaded = round_trip(original)
    total = sum(len(col) for col in loaded.tableau.columns)
    assert total == 52


def test_save_then_load_preserves_face_up_down_state():
    original = make_tableau()
    loaded = round_trip(original)
    for col_orig, col_loaded in zip(original.columns, loaded.tableau.columns):
        for card_orig, card_loaded in zip(col_orig, col_loaded):
            assert card_orig.face_up == card_loaded.face_up


def test_save_then_load_preserves_column_structure():
    original = make_tableau()
    loaded = round_trip(original)
    assert len(loaded.tableau.columns) == 7
    expected_sizes = [1, 6, 7, 8, 9, 10, 11]
    for i, size in enumerate(expected_sizes):
        assert len(loaded.tableau.columns[i]) == size
