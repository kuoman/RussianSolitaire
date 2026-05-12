# tests/solitaire/unit/test_game_file.py
import tempfile
from pathlib import Path
from solitaire.core.card import Card
from solitaire.core.tableau import _RawTableau
from solitaire.persistence.game_file import GameFile

def make_minimal_tableau():
    from solitaire.core.deck import Deck
    from solitaire.core.tableau import Tableau
    deck = Deck()
    return Tableau(deck)


def test_save_with_empty_c1_does_not_crash_when_metadata_provided():
    # Reproduces the --runs crash: post-play tableau has empty C1, but we have
    # the original deal metadata to use.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = _RawTableau([
            [],  # C1 empty (post-play state)
            [Card("♥", "8", face_up=True)],
            [Card("♥", "7", face_up=True)],
            [], [], [], [],
        ])
        deal_metadata = {
            "c1_special": "A",
            "c2_playable": "false",
            "c3_playable": "true",
            "c4_playable": "false",
            "c5_playable": "false",
            "c6_playable": "false",
            "c7_playable": "false",
            "kings_on_home_row": 0,
        }
        gf = GameFile(path, game_id="test")
        # Should NOT crash
        gf.save(
            tableau,
            metadata=deal_metadata,
            won="false",
            foundation_cards=1,
            move_log=["A♠ from C1 moved to foundation"],
        )
        content = path.read_text()
        assert "c1_special: A" in content
        assert "won: false" in content
        assert "foundation_cards: 1" in content


def test_save_without_metadata_runs_analyzer_for_initial_deal():
    # When metadata is not provided, GameFile runs the analyzer (existing behaviour).
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)  # no metadata
        content = path.read_text()
        assert "c1_special" in content

def test_saved_file_contains_game_header():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "# Game 2026-05-11-000001" in content

def test_saved_file_contains_column_headers():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "| C1 | C2 | C3 | C4 | C5 | C6 | C7 |" in content

def test_face_down_cards_saved_with_star_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
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
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        lines = path.read_text().splitlines()
        first_data_row = [l for l in lines if l.startswith("|") and "C1" not in l and "---" not in l][0]
        c1_cell = first_data_row.split("|")[1].strip()
        assert not c1_cell.startswith("*")
        assert len(c1_cell) > 0

def test_empty_cells_written_for_shorter_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
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
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "version: 0.0.1" in content

def test_saved_file_contains_c1_special_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "c1_special:" in content

def test_saved_file_contains_kings_on_home_row_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "kings_on_home_row:" in content

def test_saved_file_contains_playability_metadata_for_all_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        for col_num in range(2, 8):
            assert f"c{col_num}_playable:" in content

def test_saved_file_contains_won_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "won: unknown" in content

def test_saved_file_contains_foundation_cards_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "foundation_cards: 0" in content

def test_saved_file_contains_moves_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(tableau)
        content = path.read_text()
        assert "moves: 0" in content

def test_save_accepts_custom_outcome_values():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="2026-05-11-000001").save(
            tableau,
            won="true",
            foundation_cards=52,
            move_log=["m"] * 37,
        )
        content = path.read_text()
        assert "won: true" in content
        assert "foundation_cards: 52" in content
        assert "moves: 37" in content


def test_save_writes_no_moves_section_when_log_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="test").save(tableau, move_log=[])
        content = path.read_text()
        assert "## Moves" not in content


def test_save_writes_moves_section_when_log_has_entries():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="test").save(
            tableau,
            move_log=["7♥ from C2 moved to C1", "A♠ from C3 moved to foundation"],
        )
        content = path.read_text()
        assert "## Moves" in content
        assert "1. 7♥ from C2 moved to C1" in content
        assert "2. A♠ from C3 moved to foundation" in content


def test_save_moves_section_appears_after_table():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="test").save(tableau, move_log=["X"])
        content = path.read_text()
        moves_idx = content.index("## Moves")
        last_pipe_idx = content.rindex("|")
        assert last_pipe_idx < moves_idx


def test_save_moves_count_metadata_matches_log_length():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        GameFile(path, game_id="test").save(
            tableau, move_log=["X", "Y", "Z"]
        )
        content = path.read_text()
        assert "moves: 3" in content

def test_load_returns_seven_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        gf = GameFile(path, game_id="2026-05-11-000001")
        gf.save(original)
        loaded = gf.load()
        assert len(loaded.tableau.columns) == 7

def test_load_preserves_column_card_counts():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        gf = GameFile(path, game_id="2026-05-11-000001")
        gf.save(original)
        loaded = gf.load()
        expected_sizes = [1, 6, 7, 8, 9, 10, 11]
        for i, size in enumerate(expected_sizes):
            assert len(loaded.tableau.columns[i]) == size

def test_load_preserves_face_up_state():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        gf = GameFile(path, game_id="2026-05-11-000001")
        gf.save(original)
        loaded = gf.load()
        for col_orig, col_loaded in zip(original.columns, loaded.tableau.columns):
            for card_orig, card_loaded in zip(col_orig, col_loaded):
                assert card_orig.face_up == card_loaded.face_up

def test_load_preserves_suit_and_rank():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        gf = GameFile(path, game_id="2026-05-11-000001")
        gf.save(original)
        loaded = gf.load()
        for col_orig, col_loaded in zip(original.columns, loaded.tableau.columns):
            for card_orig, card_loaded in zip(col_orig, col_loaded):
                assert card_orig.suit == card_loaded.suit
                assert card_orig.rank == card_loaded.rank


def test_load_returns_empty_prior_moves_when_no_section():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)
        loaded = gf.load()
        assert loaded.prior_moves == []


def test_load_parses_prior_moves_from_section():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(
            tableau,
            move_log=[
                "7♥ from C2 moved to C1",
                "A♠ from C3 moved to foundation",
            ],
        )
        loaded = gf.load()
        assert loaded.prior_moves == [
            "7♥ from C2 moved to C1",
            "A♠ from C3 moved to foundation",
        ]


def test_load_round_trips_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)  # initial save with analyzer-derived metadata
        loaded = gf.load()
        assert "c1_special" in loaded.prior_metadata
        assert "kings_on_home_row" in loaded.prior_metadata
        for col_num in range(2, 8):
            assert f"c{col_num}_playable" in loaded.prior_metadata


def test_load_metadata_excludes_outcome_keys():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, won="true", foundation_cards=52)
        loaded = gf.load()
        assert "won" not in loaded.prior_metadata
        assert "foundation_cards" not in loaded.prior_metadata
        assert "moves" not in loaded.prior_metadata
        assert "version" not in loaded.prior_metadata


def test_load_metadata_converts_kings_on_home_row_to_int():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)
        loaded = gf.load()
        # kings_on_home_row is numeric; round-trip should yield an int
        assert isinstance(loaded.prior_metadata["kings_on_home_row"], int)


def test_save_writes_initial_deal_section():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)
        content = path.read_text()
        assert "## Initial Deal" in content


def test_initial_save_omits_final_state_section():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)  # initial save, no initial_tableau passed
        content = path.read_text()
        assert "## Final State" not in content


def test_save_writes_final_state_when_initial_tableau_provided():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        initial = _RawTableau([
            [Card("♠", "A", face_up=True)],
            [], [], [], [], [], [],
        ])
        final = _RawTableau([
            [],  # A♠ moved to foundation
            [], [], [], [], [], [],
        ])
        gf = GameFile(path, game_id="test")
        gf.save(
            final,
            initial_tableau=initial,
            metadata={"c1_special": "A"},
            won="false",
            foundation_cards=1,
        )
        content = path.read_text()
        assert "## Initial Deal" in content
        assert "## Final State" in content


def test_save_omits_final_state_on_win():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        initial = _RawTableau([
            [Card("♠", "A", face_up=True)],
            [], [], [], [], [], [],
        ])
        final = _RawTableau([
            [], [], [], [], [], [], [],
        ])
        gf = GameFile(path, game_id="test")
        gf.save(
            final,
            initial_tableau=initial,
            metadata={"c1_special": "A"},
            won="true",
            foundation_cards=52,
        )
        content = path.read_text()
        assert "## Initial Deal" in content
        assert "## Final State" not in content


def test_load_reads_from_initial_deal_section_not_final_state():
    # When both Initial Deal and Final State exist, load must return the
    # Initial Deal — that's the canonical starting position.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        initial = _RawTableau([
            [Card("♠", "A", face_up=True)],
            [Card("♥", "K", face_up=True)],
            [], [], [], [], [],
        ])
        final = _RawTableau([
            [], [],
            [], [], [], [], [],
        ])
        gf = GameFile(path, game_id="test")
        gf.save(
            final,
            initial_tableau=initial,
            metadata={"c1_special": "A"},
            won="false",
            foundation_cards=2,
        )
        loaded = gf.load()
        # Initial Deal had A♠ in C1 and K♥ in C2; final state was empty.
        # Load should return Initial Deal.
        assert len(loaded.tableau.columns[0]) == 1
        assert loaded.tableau.columns[0][0].rank == "A"
        assert len(loaded.tableau.columns[1]) == 1
        assert loaded.tableau.columns[1][0].rank == "K"


def test_save_writes_strategy_field():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, strategy="nply-3")
        content = path.read_text()
        assert "strategy: nply-3" in content


def test_save_default_strategy_is_human():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)
        content = path.read_text()
        assert "strategy: human" in content


def test_load_does_not_preserve_strategy_in_prior_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, strategy="nply-3")
        loaded = gf.load()
        assert "strategy" not in loaded.prior_metadata


def test_save_writes_face_down_at_end():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        # Tableau with 3 face-down cards, 1 face-up
        tableau = _RawTableau([
            [Card("♠", "A", face_up=False), Card("♥", "5", face_up=True)],
            [Card("♣", "K", face_up=False), Card("♦", "7", face_up=False)],
            [], [], [], [], [],
        ])
        gf = GameFile(path, game_id="test")
        gf.save(tableau, metadata={"c1_special": "none"})
        content = path.read_text()
        assert "face_down_at_end: 3" in content


def test_save_writes_time_to_first_foundation():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, move_log=[
            "7♥ from C2 moved to C1",
            "A♠ from C3 moved to foundation",
            "8♣ from C4 moved to C5",
        ])
        content = path.read_text()
        assert "time_to_first_foundation: 2" in content


def test_save_writes_none_when_no_foundation_move():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, move_log=[
            "7♥ from C2 moved to C1",
            "8♣ from C4 moved to C5",
        ])
        content = path.read_text()
        assert "time_to_first_foundation: none" in content


def test_save_writes_legal_moves_per_turn():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, legal_moves_per_turn=[12, 9, 7, 5, 3, 2, 1])
        content = path.read_text()
        assert "legal_moves_per_turn: 12,9,7,5,3,2,1" in content


def test_save_writes_stuck_threshold_move():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        # Counts go [12, 9, 7, 5, 3, 2, 1, 2, 1] — first sustained ≤2 starts at index 5 (move 6)
        gf.save(tableau, legal_moves_per_turn=[12, 9, 7, 5, 3, 2, 1, 2, 1])
        content = path.read_text()
        assert "stuck_threshold_move: 6" in content


def test_save_writes_stuck_none_when_never_stuck():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, legal_moves_per_turn=[12, 9, 7, 5, 3, 5, 4])
        content = path.read_text()
        assert "stuck_threshold_move: none" in content


def test_load_does_not_preserve_outcome_stats_in_prior_metadata():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau, legal_moves_per_turn=[5, 3, 1])
        loaded = gf.load()
        assert "time_to_first_foundation" not in loaded.prior_metadata
        assert "face_down_at_end" not in loaded.prior_metadata
        assert "stuck_threshold_move" not in loaded.prior_metadata
        assert "legal_moves_per_turn" not in loaded.prior_metadata


def test_save_legal_moves_per_turn_handles_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        tableau = make_minimal_tableau()
        gf = GameFile(path, game_id="test")
        gf.save(tableau)  # no legal_moves_per_turn arg
        content = path.read_text()
        assert "legal_moves_per_turn:" in content
        assert "stuck_threshold_move: none" in content


def test_load_falls_back_to_first_table_for_legacy_format():
    # Legacy format: no `## Initial Deal` heading, just the table.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "legacy.md"
        path.write_text(
            "# Game legacy\n"
            "\n"
            "version: 0.0.1\n"
            "c1_special: A\n"
            "won: unknown\n"
            "foundation_cards: 0\n"
            "moves: 0\n"
            "\n"
            "| C1 | C2 | C3 | C4 | C5 | C6 | C7 |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            "| A♠ |  |  |  |  |  |  |\n"
        )
        gf = GameFile(path, game_id="legacy")
        loaded = gf.load()
        assert len(loaded.tableau.columns) == 7
        assert loaded.tableau.columns[0][0].rank == "A"
