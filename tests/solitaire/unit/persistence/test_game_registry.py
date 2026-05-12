import tempfile
from pathlib import Path
from datetime import date
from solitaire.persistence.game_registry import GameRegistry


def test_next_game_number_is_000001_when_no_games_today():
    with tempfile.TemporaryDirectory() as data_dir:
        result = GameRegistry(Path(data_dir)).next_game_number(date(2026, 5, 11))
        assert result == "000001"


def test_next_game_number_is_000002_when_one_game_exists_today():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        (data_path / "2026-05-11-000001.md").touch()
        result = GameRegistry(data_path).next_game_number(date(2026, 5, 11))
        assert result == "000002"


def test_next_game_number_increments_from_existing():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        (data_path / "2026-05-11-000001.md").touch()
        (data_path / "2026-05-11-000002.md").touch()
        result = GameRegistry(data_path).next_game_number(date(2026, 5, 11))
        assert result == "000003"


def test_next_game_number_ignores_other_dates():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        (data_path / "2026-05-10-000001.md").touch()
        (data_path / "2026-05-10-000002.md").touch()
        result = GameRegistry(data_path).next_game_number(date(2026, 5, 11))
        assert result == "000001"


def test_next_game_path_returns_correct_path():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        result = GameRegistry(data_path).next_game_path(date(2026, 5, 11))
        assert result == data_path / "2026-05-11-000001.md"


def test_next_game_path_increments_when_game_exists():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        (data_path / "2026-05-11-000001.md").touch()
        result = GameRegistry(data_path).next_game_path(date(2026, 5, 11))
        assert result == data_path / "2026-05-11-000002.md"
