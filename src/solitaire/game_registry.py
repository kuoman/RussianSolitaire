from pathlib import Path
from datetime import date


class GameRegistry:
    @staticmethod
    def next_game_number(today: date, data_dir: Path) -> str:
        prefix = today.strftime("%Y-%m-%d")
        existing = sorted(
            p for p in data_dir.glob(f"{prefix}-*.md")
            if p.stem.split("-")[-1].isdigit()
        )
        if not existing:
            return "000001"
        last = existing[-1].stem  # e.g. "2026-05-11-000003"
        last_number = int(last.split("-")[-1])
        return f"{last_number + 1:06d}"

    @staticmethod
    def next_game_path(today: date, data_dir: Path) -> Path:
        number = GameRegistry.next_game_number(today, data_dir)
        return data_dir / f"{today.strftime('%Y-%m-%d')}-{number}.md"
