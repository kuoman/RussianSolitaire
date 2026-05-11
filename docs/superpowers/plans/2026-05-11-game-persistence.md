# Game Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Save every dealt game to a dated markdown file in `data/` with an auto-incrementing daily game number, and load any saved game back for display.

**Architecture:** Two new stateless classes — `GameRegistry` (determines next game number by scanning `data/`) and `GameFile` (serialises/deserialises a `Tableau` as a markdown table). `main.py` is updated to wire them in with `--no-save` and `--load` flags. All code is TDD with micro-commits (Arlo notation).

**Tech Stack:** Python 3, pytest, `pathlib.Path`, existing fluent assertion helpers in `tests/solitaire/assertions.py`

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `src/solitaire/game_registry.py` | Create | Determine next game number / path for today |
| `src/solitaire/game_file.py` | Create | Save and load a `Tableau` as a markdown table |
| `src/main.py` | Modify | Add `--no-save` and `--load` flags, wire in `GameRegistry` + `GameFile` |
| `tests/solitaire/unit/test_game_registry.py` | Create | Unit tests for `GameRegistry` |
| `tests/solitaire/unit/test_game_file.py` | Create | Unit tests for `GameFile` |
| `tests/solitaire/characterization/test_game_char.py` | Create | PROTECTED round-trip characterization tests |
| `data/.gitkeep` | Create | Ensures empty `data/` directory is tracked by git |

---

## Task 1: Create `data/` directory with `.gitkeep`

**Files:**
- Create: `data/.gitkeep`

- [ ] **Step 1: Create the data directory and gitkeep**

```bash
mkdir -p data
touch data/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
git add data/.gitkeep
git commit -m "chore: add data directory for game save files"
```

---

## Task 2: GameRegistry — next number when no games exist today

**Files:**
- Create: `src/solitaire/game_registry.py`
- Create: `tests/solitaire/unit/test_game_registry.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/solitaire/unit/test_game_registry.py
import tempfile
from pathlib import Path
from datetime import date
from solitaire.game_registry import GameRegistry

def test_next_game_number_is_000001_when_no_games_today():
    with tempfile.TemporaryDirectory() as data_dir:
        result = GameRegistry.next_game_number(date(2026, 5, 11), Path(data_dir))
        assert result == "000001"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_registry.py::test_next_game_number_is_000001_when_no_games_today -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'solitaire.game_registry'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/solitaire/game_registry.py
from pathlib import Path
from datetime import date


class GameRegistry:
    @staticmethod
    def next_game_number(today: date, data_dir: Path) -> str:
        prefix = today.strftime("%Y-%m-%d")
        existing = sorted(data_dir.glob(f"{prefix}-*.md"))
        if not existing:
            return "000001"
        last = existing[-1].stem  # e.g. "2026-05-11-000003"
        last_number = int(last.split("-")[-1])
        return f"{last_number + 1:06d}"

    @staticmethod
    def next_game_path(today: date, data_dir: Path) -> Path:
        number = GameRegistry.next_game_number(today, data_dir)
        return data_dir / f"{today.strftime('%Y-%m-%d')}-{number}.md"
```

- [ ] **Step 4: Run test to verify it passes**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_registry.py::test_next_game_number_is_000001_when_no_games_today -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/game_registry.py tests/solitaire/unit/test_game_registry.py
git commit -m "t: game registry returns 000001 when no games exist today"
```

---

## Task 3: GameRegistry — increments when games exist

**Files:**
- Modify: `tests/solitaire/unit/test_game_registry.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/solitaire/unit/test_game_registry.py`:

```python
def test_next_game_number_increments_from_existing():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        (data_path / "2026-05-11-000001.md").touch()
        (data_path / "2026-05-11-000002.md").touch()
        result = GameRegistry.next_game_number(date(2026, 5, 11), data_path)
        assert result == "000003"

def test_next_game_number_ignores_other_dates():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        (data_path / "2026-05-10-000001.md").touch()  # yesterday
        (data_path / "2026-05-10-000002.md").touch()
        result = GameRegistry.next_game_number(date(2026, 5, 11), data_path)
        assert result == "000001"

def test_next_game_path_returns_correct_path():
    with tempfile.TemporaryDirectory() as data_dir:
        data_path = Path(data_dir)
        result = GameRegistry.next_game_path(date(2026, 5, 11), data_path)
        assert result == data_path / "2026-05-11-000001.md"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_registry.py -v
```
Expected: 3 new tests FAIL

- [ ] **Step 3: Run all registry tests**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_registry.py -v
```
Expected: all 4 PASS (implementation already handles these)

- [ ] **Step 4: Commit**

```bash
git add tests/solitaire/unit/test_game_registry.py
git commit -m "t: game registry increments and ignores other dates"
```

---

## Task 4: GameFile — save produces correct markdown

**Files:**
- Create: `src/solitaire/game_file.py`
- Create: `tests/solitaire/unit/test_game_file.py`

- [ ] **Step 1: Write the failing tests**

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_file.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'solitaire.game_file'`

- [ ] **Step 3: Write minimal implementation**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_file.py -v
```
Expected: all 4 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/game_file.py tests/solitaire/unit/test_game_file.py
git commit -m "t: game file saves markdown table with correct header and face state"
```

---

## Task 5: GameFile — load reconstructs Tableau

**Files:**
- Modify: `src/solitaire/game_file.py`
- Modify: `tests/solitaire/unit/test_game_file.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/solitaire/unit/test_game_file.py`:

```python
def test_load_returns_seven_columns():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        assert len(loaded.columns) == 7

def test_load_preserves_column_card_counts():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        expected_sizes = [1, 6, 7, 8, 9, 10, 11]
        for i, size in enumerate(expected_sizes):
            assert len(loaded.columns[i]) == size

def test_load_preserves_face_up_state():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        for col_orig, col_loaded in zip(original.columns, loaded.columns):
            for card_orig, card_loaded in zip(col_orig, col_loaded):
                assert card_orig.face_up == card_loaded.face_up

def test_load_preserves_suit_and_rank():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        original = make_minimal_tableau()
        GameFile.save(original, path, game_id="2026-05-11-000001")
        loaded = GameFile.load(path)
        for col_orig, col_loaded in zip(original.columns, loaded.columns):
            for card_orig, card_loaded in zip(col_orig, col_loaded):
                assert card_orig.suit == card_loaded.suit
                assert card_orig.rank == card_loaded.rank
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_file.py -v
```
Expected: 4 new tests FAIL — `AttributeError: type object 'GameFile' has no attribute 'load'`

- [ ] **Step 3: Write minimal implementation**

Add to `src/solitaire/game_file.py` (inside `GameFile` class):

```python
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
```

Add `_RawTableau` to `src/solitaire/tableau.py` — a lightweight wrapper that accepts pre-built columns (bypassing the deal logic):

```python
class _RawTableau:
    def __init__(self, columns: list):
        self.columns = columns
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
.venv/bin/pytest tests/solitaire/unit/test_game_file.py -v
```
Expected: all 8 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/game_file.py src/solitaire/tableau.py tests/solitaire/unit/test_game_file.py
git commit -m "t: game file loads markdown table and reconstructs tableau"
```

---

## Task 6: Characterization tests — round-trip (PROTECTED)

**Files:**
- Create: `tests/solitaire/characterization/test_game_char.py`

> ⛔ This file is PROTECTED. Once created, do not modify without explicit human permission.

- [ ] **Step 1: Create the characterization test file**

```python
# tests/solitaire/characterization/test_game_char.py
# PROTECTED: do not modify without explicit human permission

import tempfile
from pathlib import Path
from solitaire.deck import Deck
from solitaire.tableau import Tableau
from solitaire.game_file import GameFile


def make_tableau():
    deck = Deck()
    deck.shuffle()
    return Tableau(deck)


def round_trip(tableau):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "test_game.md"
        GameFile.save(tableau, path, game_id="2026-05-11-000001")
        return GameFile.load(path)


def test_save_then_load_preserves_all_52_cards():
    original = make_tableau()
    loaded = round_trip(original)
    total = sum(len(col) for col in loaded.columns)
    assert total == 52


def test_save_then_load_preserves_face_up_down_state():
    original = make_tableau()
    loaded = round_trip(original)
    for col_orig, col_loaded in zip(original.columns, loaded.columns):
        for card_orig, card_loaded in zip(col_orig, col_loaded):
            assert card_orig.face_up == card_loaded.face_up


def test_save_then_load_preserves_column_structure():
    original = make_tableau()
    loaded = round_trip(original)
    assert len(loaded.columns) == 7
    expected_sizes = [1, 6, 7, 8, 9, 10, 11]
    for i, size in enumerate(expected_sizes):
        assert len(loaded.columns[i]) == size
```

- [ ] **Step 2: Run characterization tests**

```bash
.venv/bin/pytest tests/solitaire/characterization/test_game_char.py -v
```
Expected: all 3 PASS

- [ ] **Step 3: Run full test suite**

```bash
.venv/bin/pytest -v
```
Expected: all tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/solitaire/characterization/test_game_char.py
git commit -m "t: characterization tests for game save/load round-trip"
```

---

## Task 7: Wire `GameRegistry` and `GameFile` into `main.py`

**Files:**
- Modify: `src/main.py`

- [ ] **Step 1: Write the updated main.py**

```python
# src/main.py
import argparse
import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from solitaire.deck import Deck
from solitaire.tableau import Tableau
from solitaire.display import Display
from solitaire.game_registry import GameRegistry
from solitaire.game_file import GameFile

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    parser = argparse.ArgumentParser(description="Yukon Russian Solitaire")
    parser.add_argument("--debug", action="store_true", help="Reveal face-down cards")
    parser.add_argument("--no-save", action="store_true", help="Do not save game to file")
    parser.add_argument("--load", metavar="PATH", help="Load a saved game file")
    args = parser.parse_args()

    if args.load:
        tableau = GameFile.load(Path(args.load))
    else:
        deck = Deck()
        deck.shuffle()
        tableau = Tableau(deck)
        if not args.no_save:
            game_path = GameRegistry.next_game_path(date.today(), DATA_DIR)
            game_id = game_path.stem
            GameFile.save(tableau, game_path, game_id=game_id)
            print(f"Game saved to {game_path}")

    print(Display(tableau, debug=args.debug).render())


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run in normal mode (deal + save)**

```bash
python3 src/main.py
```
Expected: prints `Game saved to data/2026-05-11-000001.md` then the tableau. File exists at `data/2026-05-11-000001.md`.

- [ ] **Step 3: Run again (second game)**

```bash
python3 src/main.py
```
Expected: prints `Game saved to data/2026-05-11-000002.md` — game number increments.

- [ ] **Step 4: Run with `--no-save`**

```bash
python3 src/main.py --no-save
```
Expected: tableau displayed, no save message, no new file created.

- [ ] **Step 5: Run with `--load`**

```bash
python3 src/main.py --load data/2026-05-11-000001.md
```
Expected: same tableau as the original game displayed (no new file created).

- [ ] **Step 6: Run with `--load --debug`**

```bash
python3 src/main.py --load data/2026-05-11-000001.md --debug
```
Expected: same tableau with all face-down cards revealed via `*` prefix.

- [ ] **Step 7: Run full test suite**

```bash
.venv/bin/pytest -v
```
Expected: all tests PASS

- [ ] **Step 8: Commit**

```bash
git add src/main.py
git commit -m "feat: wire game registry and file save/load into main"
```

---

## Final Verification

- [ ] `python3 src/main.py` — saves `data/YYYY-MM-DD-000001.md`, displays tableau
- [ ] `python3 src/main.py` — saves `data/YYYY-MM-DD-000002.md`, increments
- [ ] `python3 src/main.py --no-save` — no file written
- [ ] `python3 src/main.py --load data/<game>.md` — loads and displays correctly
- [ ] `python3 src/main.py --load data/<game>.md --debug` — loads with debug
- [ ] `.venv/bin/pytest -v` — all tests pass
- [ ] `git add data/` and commit any saved game files
