# src/solitaire/game_file.py
from pathlib import Path
from solitaire.core.tableau import COLUMN_SIZES
from solitaire.core.card import Card
from solitaire import __version__


class GameFile:
    def __init__(self, path: Path, game_id: str):
        self._path = path
        self._game_id = game_id

    def save(self, tableau, *, metadata=None, won="unknown", foundation_cards=0, move_log=None) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if metadata is None:
            from solitaire.persistence.game_analyzer import GameAnalyzer
            metadata = GameAnalyzer(tableau).analyse()
        log = list(move_log) if move_log else []
        header_lines = self._build_header_lines(metadata, won, foundation_cards, len(log))
        table_lines = self._build_table_lines(tableau)
        moves_lines = self._build_moves_section(log)
        self._path.write_text("\n".join(header_lines + table_lines + moves_lines) + "\n")

    def _build_header_lines(self, metadata, won, foundation_cards, moves_count) -> list:
        meta_lines = [f"{k}: {v}" for k, v in metadata.items()]
        outcome_lines = [
            f"won: {won}",
            f"foundation_cards: {foundation_cards}",
            f"moves: {moves_count}",
        ]
        return [f"# Game {self._game_id}", "", f"version: {__version__}"] + meta_lines + outcome_lines + [""]

    def _build_moves_section(self, move_log: list) -> list:
        if not move_log:
            return []
        lines = ["", "## Moves"]
        for i, description in enumerate(move_log, start=1):
            lines.append(f"{i}. {description}")
        return lines

    def _build_table_lines(self, tableau) -> list:
        max_rows = max(len(col) for col in tableau.columns)
        header = "| " + " | ".join(f"C{i+1}" for i in range(len(COLUMN_SIZES))) + " |"
        separator = "| " + " | ".join("---" for _ in range(len(COLUMN_SIZES))) + " |"
        lines = [header, separator]
        for row in range(max_rows):
            cells = []
            for col in tableau.columns:
                cells.append(col[row].to_save_token() if row < len(col) else "")
            lines.append("| " + " | ".join(cells) + " |")
        return lines

    def load(self):
        from solitaire.core.tableau import _RawTableau
        lines = self._path.read_text().splitlines()
        columns = self._parse_columns(lines)
        prior_moves = self._parse_moves_section(lines)
        return _RawTableau(columns, prior_moves=prior_moves)

    def _parse_columns(self, lines: list) -> list:
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
        return columns

    def _parse_moves_section(self, lines: list) -> list:
        moves = []
        in_section = False
        for line in lines:
            if line.strip() == "## Moves":
                in_section = True
                continue
            if not in_section:
                continue
            stripped = line.strip()
            if not stripped:
                continue
            # Strip "N. " prefix
            dot_idx = stripped.find(". ")
            if dot_idx > 0 and stripped[:dot_idx].isdigit():
                moves.append(stripped[dot_idx + 2:])
            else:
                moves.append(stripped)
        return moves
