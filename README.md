# Russian Solitaire

A Python 3 implementation of **Yukon Russian Solitaire** — the variant of Yukon
in which tableau columns build down by **same suit** (not alternate colour).
Single-player, fully playable from the terminal.

## Quick Start

```bash
# create / activate the virtualenv (one time)
python3 -m venv .venv
source .venv/bin/activate

# play a fresh deal (auto-saves to ./data/YYYY-MM-DD-NNNNNN.md)
python3 src/main.py

# play without saving
python3 src/main.py --no-save

# show face-down ranks for debugging
python3 src/main.py --debug

# resume a previously-saved game
python3 src/main.py --load data/2026-05-12-000003.md

# autoplay (default strategy: first legal move)
python3 src/main.py --autoplay
python3 src/main.py --autoplay --strategy non-blocking
python3 src/main.py --autoplay --strategy nply --depth 3
```

## What Works Today

- Full Yukon Russian Solitaire deal (7 columns, 1/6/7/8/9/10/11, top 5 face-up)
- Domain model: `Card`, `Deck`, `Tableau`, `Foundation`, `Foundations`, `Game`,
  `Move`, `MoveGenerator`, `MoveFilter`
- REPL with numbered list of legal moves, foundation-preferred filtering,
  win/loss detection, free-form move syntax (`7h c2 moved to c5`)
- Save / load as Markdown files in `./data/` — version, deal metadata, outcome,
  full move log
- Autoplay with three pluggable strategies:
  - `first` — first legal move
  - `non-blocking` — picks the move that leaves the most legal follow-ups
  - `nply --depth N` — N-ply lookahead, scored on foundation cards + face-up cards
- Anchored-King rule: a King at the bottom of a column (column index `[0]`,
  the deal's leftmost card in each column) is anchored — it can only leave
  by going to the foundation as a single card

## Documentation

- [`docs/rules.md`](docs/rules.md) — game rules
- [`docs/gameplay.md`](docs/gameplay.md) — how to play, CLI usage, REPL syntax,
  save-file format, autoplay
- [`docs/development-journal.md`](docs/development-journal.md) — dev log
- [`CLAUDE.md`](CLAUDE.md) — development conventions (TDD, OOP, SOLID,
  Arlo commit notation, branching), required reading for AI collaborators
- `docs/superpowers/specs/` and `docs/superpowers/plans/` — historical design
  artefacts (snapshots, do not edit)

## Tests

```bash
.venv/bin/pytest          # run the full suite (currently 251 tests, ~0.1s)
.venv/bin/pytest -q       # quieter output
```

Tests live in `tests/solitaire/`:

- `unit/` — AI-editable unit tests, fluent style
- `characterization/` — **PROTECTED**, do not modify without explicit approval

## Development Approach

TDD-first, micro-commits in [Arlo Belshee notation](https://www.arlobelshee.com/post/the-simplest-thing-that-could-possibly-work),
trunk-based development on `main`. See [`CLAUDE.md`](CLAUDE.md) for the full
conventions.
