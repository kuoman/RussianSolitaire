# tests/solitaire/unit/test_game_file.py
import tempfile
from pathlib import Path
from solitaire.card import Card
from solitaire.game_file import GameFile

def make_minimal_tableau():
    from solitaire.deck import Deck
    from solitaire.tableau import Tableau
    deck = Deck()
    return Tableau(deck)

def test_saved_file_contains_game_header():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        content = path.read_text()
        assert "# Game 2026-05-11-000001" in content

def test_saved_file_contains_column_headers():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        content = path.read_text()
        assert "| C1 | C2 | C3 | C4 | C5 | C6 | C7 |" in content

def test_face_down_cards_saved_with_star_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        lines = path.read_text().splitlines()
        data_rows = [l for l in lines if l.startswith("|") and "C1" not in l and "---" not in l]
        # C2 has 1 face-down card (first card in column 2)
        first_data_row = data_rows[0]
        c2_cell = first_data_row.split("|")[2].strip()
        assert c2_cell.startswith("*")

def test_face_up_card_in_c1_saved_without_star():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        lines = path.read_text().splitlines()
        first_data_row = [l for l in lines if l.startswith("|") and "C1" not in l and "---" not in l][0]
        c1_cell = first_data_row.split("|")[1].strip()
        assert not c1_cell.startswith("*")
        assert len(c1_cell) > 0

def test_empty_cells_written_for_shorter_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        lines = path.read_text().splitlines()
        data_rows = [l for l in lines if l.startswith("|") and "C1" not in l and "---" not in l]
        # C1 has only 1 card; second data row should have an empty C1 cell
        second_data_row = data_rows[1]
        c1_cell = second_data_row.split("|")[1].strip()
        assert c1_cell == ""

def test_saved_file_contains_version():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        content = path.read_text()
        assert "version: 0.0.1" in content

def test_saved_file_contains_c1_special_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        content = path.read_text()
        assert "c1_special:" in content

def test_saved_file_contains_playability_metadata_for_all_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        content = path.read_text()
        for col_num in range(2, 8):
            assert f"c{col_num}_playable:" in content

def test_load_returns_seven_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        assert len(loaded.columns) == 7

def test_load_preserves_column_card_counts():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        expected_sizes = [1, 6, 7, 8, 9, 10, 11]
        for i, size in enumerate(expected_sizes):
            assert len(loaded.columns[i]) == size

def test_load_preserves_face_up_state():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        for col_orig, col_loaded in zip(original.columns, loaded.columns):
            for card_orig, card_loaded in zip(col_orig, col_loaded):
                assert card_orig.face_up == card_loaded.face_up

def test_load_preserves_suit_and_rank():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        for col_orig, col_loaded in zip(original.columns, loaded.columns):
            for card_orig, card_loaded in zip(col_orig, col_loaded):
                assert card_orig.suit == card_loaded.suit
                assert card_orig.rank == card_loaded.rank
