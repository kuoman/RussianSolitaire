# src/solitaire/game_file.py
from pathlib import Path
from solitaire.card import Card
from solitaire.tableau import COLUMN_SIZES
from solitaire import __version__


class GameFile:
    @staticmethod
    def save(tableau, path: Path, game_id: str) -> None:
        from solitaire.game_analyzer import GameAnalyzer
        path.parent.mkdir(parents=True, exist_ok=True)
        metadata = GameAnalyzer.analyse(tableau)
        meta_lines = [f"{k}: {v}" for k, v in metadata.items()]
        lines = [f"# Game {game_id}", "", f"version: {__version__}"] + meta_lines + [""]
        max_rows = max(len(col) for col in tableau.columns)
        header = "| " + " | ".join(f"C{i+1}" for i in range(len(COLUMN_SIZES))) + " |"
        separator = "| " + " | ".join("---" for _ in range(len(COLUMN_SIZES))) + " |"
        lines.append(header)
        lines.append(separator)
        for row in range(max_rows):
            cells = []
            for col in tableau.columns:
                if row < len(col):
                    card = col[row]
                    prefix = "" if card.face_up else "*"
                    cells.append(f"{prefix}{card.rank}{card.suit}")
                else:
                    cells.append("")
            lines.append("| " + " | ".join(cells) + " |")
        path.write_text("\n".join(lines) + "\n")

    @staticmethod
    def load(path: Path):
        from solitaire.tableau import _RawTableau
        lines = path.read_text().splitlines()
        data_rows = [l for l in lines if l.startswith("|") and "C1" not in l and "---" not in l]
        columns = [[] for _ in range(len(COLUMN_SIZES))]
        for row in data_rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cells) != len(COLUMN_SIZES):
                raise ValueError(
                    f"Expected {len(COLUMN_SIZES)} columns, got {len(cells)} in: {row!r}"
                )
            for col_idx, cell in enumerate(cells):
                if cell:
                    face_up = not cell.startswith("*")
                    raw = cell.lstrip("*")
                    suit = raw[-1]
                    rank = raw[:-1]
                    columns[col_idx].append(Card(suit, rank, face_up=face_up))
        return _RawTableau(columns)
