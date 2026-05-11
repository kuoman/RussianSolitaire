# Yukon Russian Solitaire — Tableau Display

**Date:** 2026-05-11  
**Scope:** Deal a game and render the tableau as text. Static display only — no moves or interactivity.

---

## Development Mindset

- **TDD first, always:** No production code is written before a failing test exists for it.
- **Micro-commits:** One commit per passing test, using Arlo notation.
- **Smalltalk-inspired OOP:** Objects are responsible for their own behavior. They tell, don't ask. Message passing over procedure calls.
- **SOLID principles:** Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.
- **XP / Code Craftsmanship:** Simple design, continuous refactoring, pair programming mindset (human + AI), no speculative features.
- **Fluent tests:** Tests read like sentences. Custom assertion helpers provide chainable, intention-revealing syntax.

---

## Architecture

```
src/
└── solitaire/
    ├── __init__.py
    ├── card.py        # Card value object
    ├── deck.py        # Deck creation and dealing
    ├── tableau.py     # 7-column game board
    └── display.py     # Text renderer

tests/
└── solitaire/
    ├── __init__.py
    ├── assertions.py          # Fluent assertion helpers (shared)
    ├── unit/                  # AI can freely write and modify
    │   ├── __init__.py
    │   ├── test_card.py
    │   ├── test_deck.py
    │   ├── test_tableau.py
    │   └── test_display.py
    └── characterization/      # PROTECTED — AI cannot modify without explicit human permission
        ├── __init__.py
        └── test_tableau_char.py

src/
└── main.py            # Entry point: deal + render + print
```

**TDD build order:** `Card` → `Deck` → `Tableau` → `Display` → `main.py`

**Test protection rule:** Files under `tests/solitaire/characterization/` are read-only for AI. No edits or deletions without explicit human approval in the conversation.

---

## Data Model

### Card — immutable value object
- `suit`: one of `♠ ♥ ♦ ♣`
- `rank`: one of `A 2 3 4 5 6 7 8 9 10 J Q K`
- `face_up`: boolean (default `False`)
- Rank order: A=1, 2–10, J=11, Q=12, K=13
- Renders as `A♠` when face-up, `░░` when face-down (in normal mode)

### Deck — 52 cards
- Constructs all 52 cards (face-down by default)
- `shuffle()` randomizes order
- `deal(n)` removes and returns n cards from the top

### Tableau — 7-column game board
- Column sizes: 1, 6, 7, 8, 9, 10, 11 cards (28 total... wait — 1+6+7+8+9+10+11 = 52 ✓)
- Face-up rule:
  - Column 1: 1 card, face-up
  - Columns 2–7: bottom cards face-down (1, 2, 3, 4, 5, 6 respectively), top 5 face-up
- Constructed by dealing from a Deck

### Display — stateless renderer
- Takes a `Tableau` and a `debug: bool` flag
- Returns a formatted string (does not print directly)
- `main.py` is responsible for printing

---

## Display Format

Each card slot is fixed-width. Cards render as `A♠`, `10♥` (2–3 chars). Columns are aligned side-by-side, shorter columns padded with blanks.

### Normal mode (`debug=False`)
Face-down cards shown as `░░`:
```
Foundations: ♠--  ♥--  ♦--  ♣--

 C1   C2   C3   C4   C5   C6   C7
 K♠   ░░   ░░   ░░   ░░   ░░   ░░
      5♥   ░░   ░░   ░░   ░░   ░░
      3♦   7♣   ░░   ░░   ░░   ░░
      J♠   Q♥   2♦   ░░   ░░   ░░
      A♣   8♠   9♥   6♦   ░░   ░░
      2♣   4♣   K♦   J♣   3♠   ░░
           9♦   7♥   5♠   10♦  Q♣
                6♣   8♣   8♥   6♠
                     4♠   A♦   4♥
                          K♣   J♦
                               2♠
```

### Debug mode (`debug=True`, via `--debug` flag)
All face-down cards shown with `*` prefix (no `░░` appears in debug mode):
```
Foundations: ♠--  ♥--  ♦--  ♣--

 C1   C2   C3   C4   C5   C6   C7
 K♠  *3♦  *7♣  *2♠  *9♥  *4♦  *J♣
      5♥  *A♣  *8♠  *5♥  *3♣  *K♦
      3♦   7♣  *6♦  *J♠  *Q♣  *8♦
      J♠   Q♥   2♦  *4♣  *A♦  *5♠
      A♣   8♠   9♥   6♦  *6♠  *J♦
      2♣   4♣   K♦   J♣   3♠  *10♦
           9♦   7♥   5♠   10♦  Q♣
                6♣   8♣   8♥   6♠
                     4♠   A♦   4♥
                          K♣   J♦
                               2♠
```

---

## Entry Point

```
python src/main.py          # Normal mode
python src/main.py --debug  # Debug mode (reveals face-down cards)
```

`main.py` responsibilities:
1. Parse `--debug` flag
2. Create and shuffle a `Deck`
3. Deal into a `Tableau`
4. Pass to `Display` with debug flag
5. Print the result

---

## Testing Approach

### Fluent assertion helper (`tests/solitaire/assertions.py`)
Chainable wrappers for intention-revealing tests:
```python
expect(card).to_have_suit("♠").and_rank("A").and_be_face_up()
expect(deck).to_have_card_count(52)
expect(tableau).to_have_column_count(7)
expect(tableau.column(2)).to_have_card_count(6).with_top(5).face_up()
```

### Unit tests (`tests/solitaire/unit/`)
- **Card:** suit, rank, face-up/down state, render output
- **Deck:** 52 cards, all suits/ranks present, deal removes cards
- **Tableau:** correct column sizes, correct face-up/down distribution
- **Display:** correct output format in both normal and debug modes

### Characterization tests (`tests/solitaire/characterization/test_tableau_char.py`)
PROTECTED — document and validate the deal behaviour. Placeholder tests to be implemented:

```python
# PROTECTED: do not modify without explicit human permission

def test_deal_produces_exactly_52_cards(): ...
def test_deal_produces_a_complete_standard_deck(): ...  # all 4 suits × 13 ranks present

def test_c1_has_one_face_up_card(): ...
def test_c1_has_no_face_down_cards(): ...

def test_c2_has_one_face_down_card(): ...
def test_c2_has_five_face_up_cards(): ...

def test_c3_has_two_face_down_cards(): ...
def test_c3_has_five_face_up_cards(): ...

def test_c4_has_three_face_down_cards(): ...
def test_c4_has_five_face_up_cards(): ...

def test_c5_has_four_face_down_cards(): ...
def test_c5_has_five_face_up_cards(): ...

def test_c6_has_five_face_down_cards(): ...
def test_c6_has_five_face_up_cards(): ...

def test_c7_has_six_face_down_cards(): ...
def test_c7_has_five_face_up_cards(): ...
```

---

## Out of Scope (this iteration)
- Moving cards
- Foundation logic
- Win/loss detection
- Saving/loading game state
- Any interactivity beyond `--debug` flag
