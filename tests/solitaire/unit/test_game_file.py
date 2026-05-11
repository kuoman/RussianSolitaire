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
        assert "| C1 |" in content
        assert "| C7 |" in content

def test_face_down_cards_saved_with_star_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        content = path.read_text()
        assert "*" in content

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
