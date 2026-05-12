# src/solitaire/game_file.py
from pathlib import Path
from solitaire.core.tableau import COLUMN_SIZES
from solitaire.core.card import Card
from solitaire import __version__


class GameFile:
    def __init__(self, path: Path, game_id: str):
        self._path = path
        self._game_id = game_id

    def save(self, tableau, *, won="unknown", foundation_cards=0, moves=0) -> None:
        from solitaire.persistence.game_analyzer import GameAnalyzer
        self._path.parent.mkdir(parents=True, exist_ok=True)
        metadata = GameAnalyzer.analyse(tableau)
        meta_lines = [f"{k}: {v}" for k, v in metadata.items()]
        outcome_lines = [
            f"won: {won}",
            f"foundation_cards: {foundation_cards}",
            f"moves: {moves}",
        ]
        lines = [f"# Game {self._game_id}", "", f"version: {__version__}"] + meta_lines + outcome_lines + [""]
        max_rows = max(len(col) for col in tableau.columns)
        header = "| " + " | ".join(f"C{i+1}" for i in range(len(COLUMN_SIZES))) + " |"
        separator = "| " + " | ".join("---" for _ in range(len(COLUMN_SIZES))) + " |"
        lines.append(header)
        lines.append(separator)
        for row in range(max_rows):
            cells = []
            for col in tableau.columns:
                if row < len(col):
                    cells.append(col[row].to_save_token())
                else:
                    cells.append("")
            lines.append("| " + " | ".join(cells) + " |")
        self._path.write_text("\n".join(lines) + "\n")

    def load(self):
        from solitaire.core.tableau import _RawTableau
        lines = self._path.read_text().splitlines()
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
                    columns[col_idx].append(Card.from_save_token(cell))
        return _RawTableau(columns)
