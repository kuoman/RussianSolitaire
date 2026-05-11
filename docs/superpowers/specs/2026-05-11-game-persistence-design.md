# Game Persistence — Save & Load

**Date:** 2026-05-11
**Scope:** Save a dealt Tableau to a markdown file with an auto-incrementing daily game number. Load a saved game back into display. No game-play state beyond the initial deal.

---

## Development Mindset

Same as all features in this project:
- **TDD first:** No production code before a failing test
- **Micro-commits:** One commit per green test, Arlo notation
- **Smalltalk-inspired OOP:** Each class has one clear responsibility
- **SOLID principles**
- **XP / Code Craftsmanship**
- **Fluent tests** via `tests/solitaire/assertions.py`

---

## Architecture

Two new classes added to `src/solitaire/`:

```
src/solitaire/
├── card.py           # existing
├── deck.py           # existing
├── tableau.py        # existing
├── display.py        # existing
├── game_registry.py  # NEW — determine next game number for today
└── game_file.py      # NEW — save/load Tableau to/from .md file

data/                 # NEW directory — game save files (gitignored)
    2026-05-11-000001.md
    2026-05-11-000002.md

tests/solitaire/unit/
├── test_game_registry.py   # NEW — unit tests
└── test_game_file.py       # NEW — unit tests

tests/solitaire/characterization/
└── test_game_char.py       # NEW — PROTECTED round-trip tests
```

**TDD build order:** `GameRegistry` → `GameFile` → wire into `main.py`

---

## Data Model

### GameRegistry
- Scans `./data/` for files matching `YYYY-MM-DD-XXXXXX.md` for today's date
- Returns next available 6-digit zero-padded game number as a string (e.g. `"000001"`)
- If no games exist for today, returns `"000001"`
- `next_game_number(date, data_dir)` — stateless, takes date and directory as arguments
- `next_game_path(date, data_dir)` — returns full `Path` for the next game file

### GameFile
- Stateless — no constructor state
- `save(tableau, path)` — writes markdown table to `path`, creates `data/` directory if needed
- `load(path)` — reads markdown table, returns a reconstructed `Tableau`

---

## File Format

Markdown table where:
- Columns = C1 through C7 (tableau columns)
- Rows = card positions (depth in each column), top to bottom
- Face-down cards prefixed with `*`
- Face-up cards have no prefix
- Empty cells where a column has no card at that row depth

### Example: `data/2026-05-11-000001.md`

```markdown
# Game 2026-05-11-000001

| C1 | C2  | C3  | C4  | C5   | C6   | C7   |
|----|-----|-----|-----|------|------|------|
| A♠ | *3♦ | *7♣ | *2♠ | *9♥  | *4♦  | *J♣  |
|    | 5♥  | *A♣ | *8♠ | *5♥  | *3♣  | *K♦  |
|    | 3♦  | 5♥  | *6♦ | *J♠  | *Q♣  | *8♦  |
|    | J♠  | Q♥  | 2♦  | *4♣  | *A♦  | *5♠  |
|    | A♣  | 8♠  | 9♥  | 6♦   | *6♠  | *J♦  |
|    | 2♣  | 4♣  | K♦  | J♣   | 3♠   | *10♦ |
|    |     | 9♦  | 7♥  | 5♠   | 10♦  | Q♣   |
|    |     |     | 6♣  | 8♣   | 8♥   | 6♠   |
|    |     |     |     | 4♠   | A♦   | 4♥   |
|    |     |     |     |      | K♣   | J♦   |
|    |     |     |     |      |      | 2♠   |
```

### Parsing rules for load
- Strip whitespace from each cell
- Empty cell → no card at that position (column ends)
- Cell starting with `*` → face-down card, strip `*` to get `rank+suit`
- Other cell → face-up card
- Rank = all chars except last unicode char; suit = last unicode char

---

## CLI

```bash
python3 src/main.py                                      # deal, save, display
python3 src/main.py --no-save                            # deal, display (no file)
python3 src/main.py --debug                              # deal, save, display with debug
python3 src/main.py --load data/2026-05-11-000001.md     # load existing game, display
python3 src/main.py --load data/2026-05-11-000001.md --debug  # load + debug
```

- `--no-save` skips file creation (deal mode only)
- `--load <path>` loads saved game instead of dealing — no save written
- `--debug` works with both modes

---

## Testing

### Unit tests (`tests/solitaire/unit/`)

**`test_game_registry.py`:**
- When `data/` is empty for today, next number is `"000001"`
- When one game exists for today, next number is `"000002"`
- Files from other dates are ignored
- `next_game_path` returns correct full path

**`test_game_file.py`:**
- Saved file contains correct markdown header
- Saved file contains column headers C1–C7
- Face-down cards written with `*` prefix
- Face-up cards written without prefix
- Empty cells written for shorter columns
- Load reconstructs correct number of columns (7)
- Load reconstructs correct card counts per column
- Load reconstructs correct face-up/down state per card
- Load reconstructs correct suit and rank per card

### Characterization tests (`tests/solitaire/characterization/test_game_char.py`)
PROTECTED — do not modify without explicit human permission.

```python
def test_save_then_load_preserves_all_52_cards(): ...
def test_save_then_load_preserves_face_up_down_state(): ...
def test_save_then_load_preserves_column_structure(): ...
```

---

## Implementation Notes

- Add `data/` to `.gitignore` — game files are runtime data, not source
- `data/` directory should be created by `GameFile.save()` if it doesn't exist

---

## Out of Scope (this iteration)
- Game moves or play history
- Win/loss recording
- Multiple save formats
- Loading from `--load` flag producing a different display than a fresh deal
