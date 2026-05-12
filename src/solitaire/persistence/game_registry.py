from pathlib import Path
from datetime import date


class GameRegistry:
    def __init__(self, data_dir: Path):
        self._data_dir = data_dir

    def next_game_number(self, today: date) -> str:
        prefix = today.strftime("%Y-%m-%d")
        existing = sorted(
            p for p in self._data_dir.glob(f"{prefix}-*.md")
            if p.stem.split("-")[-1].isdigit()
        )
        if not existing:
            return "000001"
        last = existing[-1].stem  # e.g. "2026-05-11-000003"
        last_number = int(last.split("-")[-1])
        return f"{last_number + 1:06d}"

    def next_game_path(self, today: date) -> Path:
        number = self.next_game_number(today)
        return self._data_dir / f"{today.strftime('%Y-%m-%d')}-{number}.md"
