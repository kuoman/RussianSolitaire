# src/solitaire/game_file.py
from pathlib import Path
from solitaire.core.tableau import COLUMN_SIZES
from solitaire.core.card import Card
from solitaire import __version__

_OUTCOME_KEYS = {"won", "foundation_cards", "moves", "strategy"}
_VERSION_KEY = "version"


class GameFile:
    def __init__(self, path: Path, game_id: str):
        self._path = path
        self._game_id = game_id

    def save(self, tableau, *, initial_tableau=None, metadata=None, won="unknown",
             foundation_cards=0, move_log=None, strategy="human") -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if metadata is None:
            from solitaire.persistence.game_analyzer import GameAnalyzer
            metadata = GameAnalyzer(tableau).analyse()
        log = list(move_log) if move_log else []
        initial = initial_tableau if initial_tableau is not None else tableau
        has_final = initial_tableau is not None and won != "true"
        header_lines = self._build_header_lines(
            metadata, won, foundation_cards, len(log), strategy
        )
        initial_section = self._build_table_section("Initial Deal", initial)
        final_section = self._build_table_section("Final State", tableau) if has_final else []
        moves_lines = self._build_moves_section(log)
        self._path.write_text(
            "\n".join(header_lines + initial_section + final_section + moves_lines) + "\n"
        )

    def _build_table_section(self, heading, tableau) -> list:
        lines = [f"## {heading}", ""]
        lines.extend(self._build_table_lines(tableau))
        lines.append("")
        return lines

    def _build_header_lines(self, metadata, won, foundation_cards, moves_count, strategy) -> list:
        meta_lines = [f"{k}: {v}" for k, v in metadata.items()]
        outcome_lines = [
            f"won: {won}",
            f"foundation_cards: {foundation_cards}",
            f"moves: {moves_count}",
            f"strategy: {strategy}",
        ]
        return [f"# Game {self._game_id}", "", f"version: {__version__}"] + meta_lines + outcome_lines + [""]

    def _build_moves_section(self, move_log: list) -> list:
        if not move_log:
            return []
        lines = ["## Moves"]
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
        section_lines = self._lines_for_section(lines, "Initial Deal")
        columns = self._parse_columns(section_lines)
        prior_moves = self._parse_moves_section(lines)
        prior_metadata = self._parse_metadata(lines)
        return _RawTableau(
            columns,
            prior_moves=prior_moves,
            prior_metadata=prior_metadata,
        )

    def _lines_for_section(self, lines: list, heading: str) -> list:
        """Return the slice of lines belonging to `## <heading>`. Falls back to
        the entire file (so the first table found is parsed) for legacy format."""
        section_start = None
        for i, line in enumerate(lines):
            if line.strip() == f"## {heading}":
                section_start = i + 1
                break
        if section_start is None:
            return lines
        section_end = len(lines)
        for j in range(section_start, len(lines)):
            if lines[j].startswith("## "):
                section_end = j
                break
        return lines[section_start:section_end]

    def _parse_metadata(self, lines: list) -> dict:
        metadata = {}
        for line in lines:
            if line.startswith("|") or line.startswith("#"):
                continue
            if line.strip() == "## Moves":
                break
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if not key:
                continue
            if key == _VERSION_KEY or key in _OUTCOME_KEYS:
                continue
            if key == "kings_on_home_row":
                try:
                    value = int(value)
                except ValueError:
                    pass
            metadata[key] = value
        return metadata

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
