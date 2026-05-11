# Tableau Display Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deal a shuffled Yukon Russian Solitaire game and render the 7-column tableau as text, with a `--debug` flag to reveal face-down cards.

**Architecture:** Smalltalk-inspired OOP with four focused classes: `Card` (immutable value object), `Deck` (52-card factory), `Tableau` (deal logic + column state), `Display` (stateless renderer). TDD throughout — every line of production code is preceded by a failing test. Micro-commit after each green test using Arlo notation.

**Tech Stack:** Python 3, pytest, custom fluent assertion helpers in `tests/solitaire/assertions.py`

---

## File Map

| File | Responsibility |
|------|---------------|
| `src/solitaire/__init__.py` | Package marker |
| `src/solitaire/card.py` | `Card` immutable value object |
| `src/solitaire/deck.py` | `Deck` — builds and shuffles 52 cards, deals n cards |
| `src/solitaire/tableau.py` | `Tableau` — 7 columns, deal logic, face-up/down rules |
| `src/solitaire/display.py` | `Display` — stateless text renderer, normal + debug mode |
| `src/main.py` | Entry point — parse `--debug`, wire up and print |
| `tests/solitaire/__init__.py` | Package marker |
| `tests/solitaire/assertions.py` | Fluent chainable assertion helpers |
| `tests/solitaire/unit/__init__.py` | Package marker |
| `tests/solitaire/unit/test_card.py` | Unit tests for `Card` |
| `tests/solitaire/unit/test_deck.py` | Unit tests for `Deck` |
| `tests/solitaire/unit/test_tableau.py` | Unit tests for `Tableau` |
| `tests/solitaire/unit/test_display.py` | Unit tests for `Display` |
| `tests/solitaire/characterization/__init__.py` | Package marker |
| `tests/solitaire/characterization/test_tableau_char.py` | **PROTECTED** characterization tests — do not edit without human permission |

---

## Task 1: Project scaffolding + pytest setup

**Files:**
- Create: `src/solitaire/__init__.py`
- Create: `tests/solitaire/__init__.py`
- Create: `tests/solitaire/unit/__init__.py`
- Create: `tests/solitaire/characterization/__init__.py`
- Create: `pytest.ini`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p src/solitaire
mkdir -p tests/solitaire/unit
mkdir -p tests/solitaire/characterization
```

- [ ] **Step 2: Create package markers**

Create `src/solitaire/__init__.py` — empty file.
Create `tests/solitaire/__init__.py` — empty file.
Create `tests/solitaire/unit/__init__.py` — empty file.
Create `tests/solitaire/characterization/__init__.py` — empty file.

- [ ] **Step 3: Create pytest.ini**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

- [ ] **Step 4: Verify pytest is installed and discovers tests**

```bash
pytest --collect-only
```
Expected: `no tests ran` with 0 errors (directories discovered, no test files yet).

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/__init__.py tests/solitaire/__init__.py tests/solitaire/unit/__init__.py tests/solitaire/characterization/__init__.py pytest.ini
git commit -m "chore: scaffold project structure and pytest config"
```

---

## Task 2: Fluent assertion helpers

**Files:**
- Create: `tests/solitaire/assertions.py`

- [ ] **Step 1: Create the fluent assertion helper**

```python
class CardAssertion:
    def __init__(self, card):
        self._card = card

    def to_have_suit(self, suit):
        assert self._card.suit == suit, f"Expected suit {suit!r}, got {self._card.suit!r}"
        return self

    def and_rank(self, rank):
        assert self._card.rank == rank, f"Expected rank {rank!r}, got {self._card.rank!r}"
        return self

    def and_be_face_up(self):
        assert self._card.face_up, "Expected card to be face-up"
        return self

    def and_be_face_down(self):
        assert not self._card.face_up, "Expected card to be face-down"
        return self

    def and_render_as(self, text):
        assert self._card.render() == text, f"Expected render {text!r}, got {self._card.render()!r}"
        return self


class DeckAssertion:
    def __init__(self, deck):
        self._deck = deck

    def to_have_card_count(self, count):
        actual = len(self._deck.cards)
        assert actual == count, f"Expected {count} cards, got {actual}"
        return self

    def to_contain_all_suits_and_ranks(self):
        suits = {"♠", "♥", "♦", "♣"}
        ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
        found_suits = {c.suit for c in self._deck.cards}
        found_ranks = {c.rank for c in self._deck.cards}
        assert found_suits == suits, f"Missing suits: {suits - found_suits}"
        assert found_ranks == ranks, f"Missing ranks: {ranks - found_ranks}"
        return self


class ColumnAssertion:
    def __init__(self, column):
        self._column = column

    def to_have_card_count(self, count):
        actual = len(self._column)
        assert actual == count, f"Expected {count} cards in column, got {actual}"
        return self

    def to_have_face_up_count(self, count):
        actual = sum(1 for c in self._column if c.face_up)
        assert actual == count, f"Expected {count} face-up cards, got {actual}"
        return self

    def to_have_face_down_count(self, count):
        actual = sum(1 for c in self._column if not c.face_up)
        assert actual == count, f"Expected {count} face-down cards, got {actual}"
        return self


class TableauAssertion:
    def __init__(self, tableau):
        self._tableau = tableau

    def to_have_column_count(self, count):
        actual = len(self._tableau.columns)
        assert actual == count, f"Expected {count} columns, got {actual}"
        return self

    def column(self, number):
        return ColumnAssertion(self._tableau.columns[number - 1])


def expect_card(card):
    return CardAssertion(card)

def expect_deck(deck):
    return DeckAssertion(deck)

def expect_tableau(tableau):
    return TableauAssertion(tableau)
```

- [ ] **Step 2: Commit**

```bash
git add tests/solitaire/assertions.py
git commit -m "chore: add fluent assertion helpers"
```

---

## Task 3: Card — suit and rank

**Files:**
- Create: `src/solitaire/card.py`
- Create: `tests/solitaire/unit/test_card.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/solitaire/unit/test_card.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from solitaire.card import Card
from tests.solitaire.assertions import expect_card

def test_card_has_suit_and_rank():
    card = Card("♠", "A")
    expect_card(card).to_have_suit("♠").and_rank("A")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/solitaire/unit/test_card.py::test_card_has_suit_and_rank -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'solitaire.card'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/solitaire/card.py

class Card:
    def __init__(self, suit: str, rank: str, face_up: bool = False):
        self._suit = suit
        self._rank = rank
        self._face_up = face_up

    @property
    def suit(self) -> str:
        return self._suit

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def face_up(self) -> bool:
        return self._face_up
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/solitaire/unit/test_card.py::test_card_has_suit_and_rank -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/card.py tests/solitaire/unit/test_card.py
git commit -m "t: card has suit and rank"
```

---

## Task 4: Card — face-up and face-down state

**Files:**
- Modify: `tests/solitaire/unit/test_card.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/solitaire/unit/test_card.py`:

```python
def test_card_is_face_down_by_default():
    card = Card("♥", "K")
    expect_card(card).and_be_face_down()

def test_card_can_be_face_up():
    card = Card("♦", "5", face_up=True)
    expect_card(card).and_be_face_up()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_card.py -v
```
Expected: the two new tests FAIL (face_up property not yet tested — but Card already has it, so these should pass after Task 3's implementation). If they pass, that's fine — move to Step 5.

- [ ] **Step 3: Run all card tests**

```bash
pytest tests/solitaire/unit/test_card.py -v
```
Expected: all 3 PASS

- [ ] **Step 4: Commit**

```bash
git add tests/solitaire/unit/test_card.py
git commit -m "t: card face-up and face-down state"
```

---

## Task 5: Card — render output

**Files:**
- Modify: `src/solitaire/card.py`
- Modify: `tests/solitaire/unit/test_card.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/solitaire/unit/test_card.py`:

```python
def test_face_up_card_renders_as_rank_and_suit():
    card = Card("♠", "A", face_up=True)
    expect_card(card).and_render_as("A♠")

def test_face_up_ten_renders_as_three_chars():
    card = Card("♥", "10", face_up=True)
    expect_card(card).and_render_as("10♥")

def test_face_down_card_renders_as_block():
    card = Card("♣", "Q", face_up=False)
    expect_card(card).and_render_as("░░")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_card.py -v
```
Expected: 3 new tests FAIL — `AttributeError: 'Card' object has no attribute 'render'`

- [ ] **Step 3: Write minimal implementation**

Add to `src/solitaire/card.py`:

```python
    def render(self) -> str:
        if self._face_up:
            return f"{self._rank}{self._suit}"
        return "░░"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/solitaire/unit/test_card.py -v
```
Expected: all 6 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/card.py tests/solitaire/unit/test_card.py
git commit -m "t: card renders rank+suit when face-up, ░░ when face-down"
```

---

## Task 6: Card — debug render (face-down with * prefix)

**Files:**
- Modify: `src/solitaire/card.py`
- Modify: `tests/solitaire/unit/test_card.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/solitaire/unit/test_card.py`:

```python
def test_face_down_card_renders_with_star_prefix_in_debug_mode():
    card = Card("♣", "Q", face_up=False)
    expect_card(card).and_render_as("*Q♣", debug=True)
```

Update `CardAssertion.and_render_as` in `tests/solitaire/assertions.py` to accept optional `debug`:

```python
def and_render_as(self, text, debug=False):
    actual = self._card.render(debug=debug)
    assert actual == text, f"Expected render {text!r}, got {actual!r}"
    return self
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/solitaire/unit/test_card.py::test_face_down_card_renders_with_star_prefix_in_debug_mode -v
```
Expected: FAIL — `TypeError: render() got an unexpected keyword argument 'debug'`

- [ ] **Step 3: Write minimal implementation**

Update `render` in `src/solitaire/card.py`:

```python
    def render(self, debug: bool = False) -> str:
        if self._face_up:
            return f"{self._rank}{self._suit}"
        if debug:
            return f"*{self._rank}{self._suit}"
        return "░░"
```

- [ ] **Step 4: Run all card tests**

```bash
pytest tests/solitaire/unit/test_card.py -v
```
Expected: all 7 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/card.py tests/solitaire/unit/test_card.py tests/solitaire/assertions.py
git commit -m "t: face-down card renders with * prefix in debug mode"
```

---

## Task 7: Deck — 52 cards with all suits and ranks

**Files:**
- Create: `src/solitaire/deck.py`
- Create: `tests/solitaire/unit/test_deck.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/solitaire/unit/test_deck.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from solitaire.deck import Deck
from tests.solitaire.assertions import expect_deck

def test_deck_has_52_cards():
    deck = Deck()
    expect_deck(deck).to_have_card_count(52)

def test_deck_contains_all_suits_and_ranks():
    deck = Deck()
    expect_deck(deck).to_contain_all_suits_and_ranks()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_deck.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'solitaire.deck'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/solitaire/deck.py
import random
from solitaire.card import Card

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n: int) -> list:
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/solitaire/unit/test_deck.py -v
```
Expected: all 2 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/deck.py tests/solitaire/unit/test_deck.py
git commit -m "t: deck has 52 cards covering all suits and ranks"
```

---

## Task 8: Deck — deal removes cards from top

**Files:**
- Modify: `tests/solitaire/unit/test_deck.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/solitaire/unit/test_deck.py`:

```python
def test_deal_removes_cards_from_deck():
    deck = Deck()
    dealt = deck.deal(5)
    assert len(dealt) == 5
    expect_deck(deck).to_have_card_count(47)

def test_deal_returns_cards_from_top():
    deck = Deck()
    top_card = deck.cards[0]
    dealt = deck.deal(1)
    assert dealt[0] is top_card
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_deck.py -v
```
Expected: both new tests FAIL (deal not fully implemented yet — but our implementation already handles this, so they may pass).

- [ ] **Step 3: Run all deck tests**

```bash
pytest tests/solitaire/unit/test_deck.py -v
```
Expected: all 4 PASS

- [ ] **Step 4: Commit**

```bash
git add tests/solitaire/unit/test_deck.py
git commit -m "t: deal removes n cards from top of deck"
```

---

## Task 9: Tableau — 7 columns with correct card counts

**Files:**
- Create: `src/solitaire/tableau.py`
- Create: `tests/solitaire/unit/test_tableau.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/solitaire/unit/test_tableau.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from solitaire.deck import Deck
from solitaire.tableau import Tableau
from tests.solitaire.assertions import expect_tableau

def test_tableau_has_seven_columns():
    deck = Deck()
    tableau = Tableau(deck)
    expect_tableau(tableau).to_have_column_count(7)

def test_tableau_column_sizes():
    deck = Deck()
    tableau = Tableau(deck)
    expected_sizes = [1, 6, 7, 8, 9, 10, 11]
    for i, size in enumerate(expected_sizes, start=1):
        expect_tableau(tableau).column(i).to_have_card_count(size)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_tableau.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'solitaire.tableau'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/solitaire/tableau.py
from solitaire.deck import Deck

COLUMN_SIZES = [1, 6, 7, 8, 9, 10, 11]

class Tableau:
    def __init__(self, deck: Deck):
        self.columns = []
        for size in COLUMN_SIZES:
            self.columns.append(deck.deal(size))
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/solitaire/unit/test_tableau.py -v
```
Expected: all 2 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/tableau.py tests/solitaire/unit/test_tableau.py
git commit -m "t: tableau deals 7 columns with correct card counts"
```

---

## Task 10: Tableau — face-up and face-down distribution

**Files:**
- Modify: `src/solitaire/tableau.py`
- Modify: `tests/solitaire/unit/test_tableau.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/solitaire/unit/test_tableau.py`:

```python
def test_column_1_has_one_face_up_card():
    deck = Deck()
    tableau = Tableau(deck)
    expect_tableau(tableau).column(1).to_have_face_up_count(1)

def test_column_1_has_no_face_down_cards():
    deck = Deck()
    tableau = Tableau(deck)
    expect_tableau(tableau).column(1).to_have_face_down_count(0)

def test_columns_2_to_7_have_five_face_up_cards():
    deck = Deck()
    tableau = Tableau(deck)
    for col in range(2, 8):
        expect_tableau(tableau).column(col).to_have_face_up_count(5)

def test_columns_2_to_7_face_down_counts():
    deck = Deck()
    tableau = Tableau(deck)
    expected_face_down = [1, 2, 3, 4, 5, 6]
    for col, expected in zip(range(2, 8), expected_face_down):
        expect_tableau(tableau).column(col).to_have_face_down_count(expected)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_tableau.py -v
```
Expected: 4 new tests FAIL — all cards are face-down (default), so face-up counts are 0.

- [ ] **Step 3: Write minimal implementation**

Update `src/solitaire/tableau.py`:

```python
# src/solitaire/tableau.py
from solitaire.card import Card
from solitaire.deck import Deck

COLUMN_SIZES = [1, 6, 7, 8, 9, 10, 11]

class Tableau:
    def __init__(self, deck: Deck):
        self.columns = []
        for i, size in enumerate(COLUMN_SIZES):
            cards = deck.deal(size)
            face_down_count = 0 if i == 0 else size - 5
            column = [
                Card(card.suit, card.rank, face_up=(j >= face_down_count))
                for j, card in enumerate(cards)
            ]
            self.columns.append(column)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/solitaire/unit/test_tableau.py -v
```
Expected: all 6 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/tableau.py tests/solitaire/unit/test_tableau.py
git commit -m "t: tableau sets correct face-up/down distribution per column"
```

---

## Task 11: Characterization tests — deal validation (PROTECTED)

**Files:**
- Create: `tests/solitaire/characterization/test_tableau_char.py`

> ⛔ This file is PROTECTED. Once created, it must not be modified without explicit human permission.

- [ ] **Step 1: Create the characterization test file**

```python
# tests/solitaire/characterization/test_tableau_char.py
# PROTECTED: do not modify without explicit human permission

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from solitaire.deck import Deck
from solitaire.tableau import Tableau
from tests.solitaire.assertions import expect_tableau

def make_tableau():
    deck = Deck()
    deck.shuffle()
    return Tableau(deck)

def test_deal_produces_exactly_52_cards():
    tableau = make_tableau()
    total = sum(len(col) for col in tableau.columns)
    assert total == 52

def test_deal_produces_a_complete_standard_deck():
    deck = Deck()
    tableau = Tableau(deck)
    all_cards = [card for col in tableau.columns for card in col]
    suits = {c.suit for c in all_cards}
    ranks = {c.rank for c in all_cards}
    assert suits == {"♠", "♥", "♦", "♣"}
    assert ranks == {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}

def test_c1_has_one_face_up_card():
    expect_tableau(make_tableau()).column(1).to_have_face_up_count(1)

def test_c1_has_no_face_down_cards():
    expect_tableau(make_tableau()).column(1).to_have_face_down_count(0)

def test_c2_has_one_face_down_card():
    expect_tableau(make_tableau()).column(2).to_have_face_down_count(1)

def test_c2_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(2).to_have_face_up_count(5)

def test_c3_has_two_face_down_cards():
    expect_tableau(make_tableau()).column(3).to_have_face_down_count(2)

def test_c3_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(3).to_have_face_up_count(5)

def test_c4_has_three_face_down_cards():
    expect_tableau(make_tableau()).column(4).to_have_face_down_count(3)

def test_c4_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(4).to_have_face_up_count(5)

def test_c5_has_four_face_down_cards():
    expect_tableau(make_tableau()).column(5).to_have_face_down_count(4)

def test_c5_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(5).to_have_face_up_count(5)

def test_c6_has_five_face_down_cards():
    expect_tableau(make_tableau()).column(6).to_have_face_down_count(5)

def test_c6_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(6).to_have_face_up_count(5)

def test_c7_has_six_face_down_cards():
    expect_tableau(make_tableau()).column(7).to_have_face_down_count(6)

def test_c7_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(7).to_have_face_up_count(5)
```

- [ ] **Step 2: Run characterization tests**

```bash
pytest tests/solitaire/characterization/ -v
```
Expected: all 16 PASS

- [ ] **Step 3: Run full test suite**

```bash
pytest -v
```
Expected: all tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/solitaire/characterization/test_tableau_char.py
git commit -m "t: characterization tests for deal validation"
```

---

## Task 12: Display — normal mode rendering

**Files:**
- Create: `src/solitaire/display.py`
- Create: `tests/solitaire/unit/test_display.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/solitaire/unit/test_display.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from solitaire.card import Card
from solitaire.deck import Deck
from solitaire.tableau import Tableau
from solitaire.display import Display

def make_fixed_tableau():
    deck = Deck()  # unshuffled, deterministic order
    return Tableau(deck)

def test_display_includes_foundation_header():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    assert "Foundations: ♠--  ♥--  ♦--  ♣--" in output

def test_display_includes_column_headers():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    assert "C1" in output
    assert "C7" in output

def test_display_shows_face_down_as_blocks_in_normal_mode():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    assert "░░" in output
    assert "*" not in output

def test_display_has_eleven_card_rows():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    lines = output.strip().split("\n")
    card_lines = [l for l in lines if any(s in l for s in ["♠", "♥", "♦", "♣", "░░"])]
    assert len(card_lines) == 11
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_display.py -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'solitaire.display'`

- [ ] **Step 3: Write minimal implementation**

```python
# src/solitaire/display.py

SLOT_WIDTH = 5  # " A♠  " — 4 chars + 1 space, wide enough for "10♥ "

class Display:
    def __init__(self, tableau, debug: bool = False):
        self._tableau = tableau
        self._debug = debug

    def render(self) -> str:
        lines = []
        lines.append("Foundations: ♠--  ♥--  ♦--  ♣--")
        lines.append("")
        lines.append(self._header_row())
        max_rows = max(len(col) for col in self._tableau.columns)
        for row in range(max_rows):
            lines.append(self._card_row(row))
        return "\n".join(lines)

    def _header_row(self) -> str:
        headers = [f" C{i+1} " for i in range(7)]
        return " ".join(headers)

    def _card_row(self, row: int) -> str:
        slots = []
        for col in self._tableau.columns:
            if row < len(col):
                card = col[row]
                text = card.render(debug=self._debug)
                slots.append(f"{text:<4}")
            else:
                slots.append("    ")
        return " ".join(slots)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/solitaire/unit/test_display.py -v
```
Expected: all 4 PASS

- [ ] **Step 5: Commit**

```bash
git add src/solitaire/display.py tests/solitaire/unit/test_display.py
git commit -m "t: display renders foundation header, column headers, and card rows"
```

---

## Task 13: Display — debug mode rendering

**Files:**
- Modify: `tests/solitaire/unit/test_display.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/solitaire/unit/test_display.py`:

```python
def test_display_shows_star_prefix_for_face_down_in_debug_mode():
    tableau = make_fixed_tableau()
    output = Display(tableau, debug=True).render()
    assert "*" in output
    assert "░░" not in output

def test_display_normal_mode_has_no_star_prefix():
    tableau = make_fixed_tableau()
    output = Display(tableau, debug=False).render()
    assert "*" not in output
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/solitaire/unit/test_display.py -v
```
Expected: both new tests FAIL

- [ ] **Step 3: Verify implementation already supports debug**

`Display.__init__` already accepts `debug` and passes it to `card.render(debug=...)`. Run:

```bash
pytest tests/solitaire/unit/test_display.py -v
```
Expected: all 6 PASS (the debug wiring was done in Task 12)

- [ ] **Step 4: Commit**

```bash
git add tests/solitaire/unit/test_display.py
git commit -m "t: display debug mode shows * prefix for face-down cards"
```

---

## Task 14: Entry point — main.py

**Files:**
- Create: `src/main.py`

- [ ] **Step 1: Create main.py**

```python
# src/main.py
import argparse
from solitaire.deck import Deck
from solitaire.tableau import Tableau
from solitaire.display import Display

def main():
    parser = argparse.ArgumentParser(description="Yukon Russian Solitaire")
    parser.add_argument("--debug", action="store_true", help="Reveal face-down cards")
    args = parser.parse_args()

    deck = Deck()
    deck.shuffle()
    tableau = Tableau(deck)
    print(Display(tableau, debug=args.debug).render())

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run in normal mode**

```bash
python src/main.py
```
Expected: tableau printed with `░░` for face-down cards, `Foundations: ♠--  ♥--  ♦--  ♣--` header.

- [ ] **Step 3: Run in debug mode**

```bash
python src/main.py --debug
```
Expected: same tableau but face-down cards show as `*A♠` style, no `░░`.

- [ ] **Step 4: Run full test suite**

```bash
pytest -v
```
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add src/main.py
git commit -m "feat: add main entry point with --debug flag"
```

---

## Final verification

- [ ] Run full suite: `pytest -v` — all tests pass
- [ ] Run `python src/main.py` — normal display looks correct
- [ ] Run `python src/main.py --debug` — debug display reveals face-down cards with `*`
- [ ] Confirm characterization tests still pass: `pytest tests/solitaire/characterization/ -v`
