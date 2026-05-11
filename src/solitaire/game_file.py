# src/solitaire/game_file.py
from pathlib import Path
from solitaire.card import Card


class GameFile:
    @staticmethod
    def save(tableau, path: Path, game_id: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"# Game {game_id}", ""]
        max_rows = max(len(col) for col in tableau.columns)
        header = "| " + " | ".join(f"C{i+1}" for i in range(7)) + " |"
        separator = "| " + " | ".join("---" for _ in range(7)) + " |"
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
        columns = [[] for _ in range(7)]
        for row in data_rows:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            for col_idx, cell in enumerate(cells[:7]):
                if cell:
                    face_up = not cell.startswith("*")
                    raw = cell.lstrip("*")
                    suit = raw[-1]
                    rank = raw[:-1]
                    columns[col_idx].append(Card(suit, rank, face_up=face_up))
        return _RawTableau(columns)
