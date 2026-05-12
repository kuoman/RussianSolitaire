# Russian Solitaire Project

Python implementation of Russian Solitaire card game.

## Development Approach

### Test-Driven Development
- **Spec-driven**: All features specified before implementation
- **Test-first**: Write tests before production code
- **Characterization tests**: Used to validate and document functionality
- Both test types written in **fluent style syntax**

### Object-Oriented Design
- **Smalltalk-inspired OOP**: Strong object model with message passing
- **SOLID principles**: 
  - Single Responsibility Principle
  - Open/Closed Principle
  - Liskov Substitution Principle
  - Interface Segregation Principle
  - Dependency Inversion Principle
- **XP (Extreme Programming) principles**:
  - Simple design
  - Refactoring
  - Pair programming mindset (human + AI)
  - Continuous testing

### Architecture
- Text-based prototype interface
- Data persistence in `./data` folder
- Clean separation of concerns
- Message-passing between objects

## Project Structure

```
/
├── docs/                          # Documentation
│   ├── rules.md                   # Game rules
│   ├── gameplay.md                # User-facing guide (CLI, REPL, save format)
│   ├── development-journal.md     # Dev log
│   └── superpowers/               # Historical specs & plans (do not edit)
├── data/                          # Saved games: YYYY-MM-DD-NNNNNN.md
├── src/
│   ├── main.py                    # CLI entry point
│   └── solitaire/
│       ├── __init__.py            # __version__ = "0.0.1"
│       ├── display.py             # Text rendering of tableau + foundations
│       ├── core/                  # Domain model
│       │   ├── card.py            # Card (rank, suit, face_up, save tokens)
│       │   ├── deck.py            # Deck (build, shuffle)
│       │   ├── tableau.py         # 7 columns, 1/6/7/8/9/10/11 deal
│       │   ├── foundation.py      # Single-suit foundation pile
│       │   ├── foundations.py     # Collection of 4 foundations
│       │   ├── game.py            # Apply move, snapshot/restore, move log
│       │   ├── move.py            # Move + ColumnDestination + FoundationDestination
│       │   ├── move_generator.py  # Enumerate all legal moves
│       │   └── move_filter.py     # Hide tableau-moves shadowed by a foundation move
│       ├── persistence/           # Save / load
│       │   ├── game_file.py       # Markdown read/write
│       │   ├── game_registry.py   # Daily-incrementing IDs (YYYY-MM-DD-NNNNNN)
│       │   └── game_analyzer.py   # Deal-state metadata for save header
│       ├── repl/                  # Interactive play loop
│       │   ├── repl.py            # Numbered moves, win/loss, autosave on exit
│       │   └── command_parser.py  # `<card> <source> moved to <dest>` and pick
│       └── autoplay/              # Headless play
│           ├── autoplayer.py      # Drive game until win / stuck / cap
│           └── strategies/        # first_move, non_blocking, nply
└── tests/solitaire/
    ├── unit/                      # AI-editable, fluent style
    ├── characterization/          # PROTECTED — do not modify without permission
    └── assertions.py
```

## Testing Philosophy

- Tests express intent clearly through fluent syntax
- Characterization tests document existing behavior
- Test-first tests drive new functionality
- Tests are first-class citizens - modify with permission only

## Code Style

- Small, focused classes with single responsibilities
- Objects tell, don't ask
- Favor composition over inheritance
- Immutability where appropriate
- Clear, intention-revealing names
- **No `@staticmethod`**: every method is an instance method. If a class has only static methods it isn't really an object — give it a constructor that takes its dependencies and convert the methods. The one allowed exception is `@classmethod` used as a Pythonic alternate constructor (e.g. `Card.from_save_token`).

## Commit Workflow

- **Micro commits**: Commit small, atomic changes frequently
- **Arlo Belshee's commit notation**: Use strict Arlo notation — single character prefix, no colon:
  - `t` — test only, no production code changed
  - `r` — refactor, provably safe (behaviour unchanged, passes before and after)
  - `R` — refactor, higher risk (touching production logic)
  - `F` — new feature (production code, new behaviour)
  - `b` — bug fix
  - `d` — documentation only
  - Uppercase = higher risk; lowercase = safe/mechanical
- **Committer skill**: Always use the committer skill when creating commits (invoked via `c` or `/commit`)
- Commits should be small enough to easily understand and revert if needed

## Branching Strategy

- **Trunk-based development**: `main` is the integration branch — all work lands here
- **Short-lived branches only**: Subagents may create feature branches for isolation during TDD/test-first work, but these must be merged back to `main` before the task is considered done
- **No long-lived branches**: A task is not complete until its code is on `main`
- Single developer — no PRs required, direct merge to main is the norm

## Running the Game

```bash
python3 src/main.py                                    # new deal, save, REPL
python3 src/main.py --no-save                          # play without writing data/
python3 src/main.py --debug                            # show face-down ranks
python3 src/main.py --load <path>                      # resume a saved game
python3 src/main.py --autoplay                         # autoplay (default: first)
python3 src/main.py --autoplay --strategy non-blocking
python3 src/main.py --autoplay --strategy nply --depth 3
```

User-facing details (display layout, command syntax, suit letters) live in
`docs/gameplay.md` — keep that doc in sync if behaviour changes.

## REPL Behaviour

- After every move the display is re-rendered and a numbered list of legal
  moves is printed. Pick by number, or type the long form
  `7h c2 moved to c5`.
- Suits accept either letter (`s h d c`) or unicode (`♠ ♥ ♦ ♣`).
  Destinations are `c1`..`c7` or `f` (foundation).
- `MoveFilter.visible()` hides any tableau move whose `(source_column, count)`
  is also reachable as a foundation move — keeps the menu short and steers
  the player towards foundation-first play.
- On exit the REPL writes the final state (with full move log and outcome)
  back to the same save file, unless `--no-save` was used.

## Autoplay Strategies

- `first` — first legal move from the visible list.
- `non-blocking` — for each candidate, look one move ahead and prefer the
  move that leaves the most legal follow-ups (foundation moves get a small
  bonus).
- `nply --depth N` — minimax-style N-ply search; leaf evaluation is
  `foundation_cards + 0.1 * face_up_cards`.

`Autoplayer` aborts after `max_moves=10000` to prevent runaway loops; the
outcome is one of `"true"` (won), `"false"` (no legal moves), `"aborted"`.

## Save File Format

Saves are Markdown — one file per game in `./data/YYYY-MM-DD-NNNNNN.md`,
numbered per day by `GameRegistry`. Each file contains:

1. `# Game <id>` heading
2. Header lines: `version`, deal-shape metadata from `GameAnalyzer`
   (`c1_special`, `cN_playable`, `kings_on_home_row`), and outcome
   (`won`, `foundation_cards`, `moves`)
3. A pipe-table with columns `C1..C7` — face-down cards are prefixed `*`
4. `## Moves` — numbered list of move descriptions

The same file is overwritten on REPL exit / autoplay finish. `GameFile.load`
re-reads the table and the move log so games can be resumed.

## Domain Rules in Code

- **Tableau-to-tableau**: same suit, one rank lower; whole face-up sub-stack
  moves with the chosen card.
- **Foundation**: single card only, building up by suit from Ace.
- **Empty column**: only Kings (and any cards beneath them) may fill it.
- **Anchored King rule**: if the moving stack starts at the bottom of its
  column (`count == len(source_col)`) and that bottom card is a King, the
  only legal move is `count == 1` to the foundation. In practice: a King
  in column index 0 (the leftmost dealt card of any column) cannot lead a
  same-suit run elsewhere — it can only go up to its foundation alone.

## Testing Protocol

- Run `.venv/bin/pytest` — currently 251 tests, sub-second.
- `tests/solitaire/unit/` is fair game for edits.
- `tests/solitaire/characterization/` is **PROTECTED**: do not modify
  without explicit approval. These tests document existing behaviour and
  catch regressions; if a characterization test is wrong, escalate rather
  than edit.
