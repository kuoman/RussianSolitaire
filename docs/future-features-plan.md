# Future Features Plan

A scratchpad for ideas not yet implemented. Each section gives enough context for a future Claude/AI session to pick up the thread without re-reading the entire codebase. See the **Project state at write time** section at the bottom for the snapshot this plan was written against.

---

## 1. Hint mode in the REPL

**What:** Add a `?move` or `hint` command to the REPL that suggests a next move using one of the autoplay strategies, without actually applying it.

**Why:** Players stuck on what to do next would benefit from a "show me what `nply-3` would do here" peek. The numbered move list already shows legal moves, but doesn't rank them.

**Where it'd go:**
- Extend `src/solitaire/repl/command_parser.py` to recognize `hint` / `?move` as a new return kind, e.g. `("hint",)`.
- In `src/solitaire/repl/repl.py`, dispatch the hint kind to a new method that:
  1. Builds a strategy (default: `nply-3` for quality, or maybe `non-blocking` for speed)
  2. Calls `strategy.select(self._game, self._current_moves)`
  3. Renders the chosen move's `describe(tableau)` plus its index in the numbered list
  4. Re-displays the prompt without changing game state
- Could also accept `hint <strategy>` to choose which strategy gives the suggestion.

**Tests:** Add to `tests/solitaire/unit/repl/test_repl.py`. Use a stub strategy that returns a known move; verify the REPL prints the suggestion and doesn't apply it.

**Estimate:** 1–2 hours.

---

## 2. Undo / redo

**What:** Let the player undo their last move (and redo it). Keyboard shortcut: `u` for undo, `r` for redo (or `redo`).

**Why:** Mistakes happen. A simple undo dramatically improves UX without changing strategy.

**Where it'd go:**
- `Game.snapshot()` and `Game.restore()` already exist — built for the look-ahead strategies. Reuse them.
- Maintain a stack of snapshots in `Repl` (or in `Game` itself). On `apply()`, push pre-state. On undo, pop and restore.
- The REPL would maintain a separate redo stack if you want both directions.
- New parser kinds: `("undo",)` and `("redo",)`.
- Update `Game.apply()` semantics: it should probably NOT auto-snapshot (snapshots cost memory; let callers decide). The REPL pushes before each apply.

**Risks:** the snapshot/restore was designed for AI search — not for long-term retention. Make sure restoring to a snapshot N moves back doesn't have stale references. Probably fine since `Card` is immutable, but verify.

**Tests:** Multiple apply/undo cycles, undo back to start, redo forward, undo past start (should no-op or message), interaction with auto-flip.

**Estimate:** 2–4 hours including testing edge cases.

---

## 3. Better display

**What:** Visual polish in the terminal:
- Highlight cards that have a legal move target (e.g., bold them or show a subtle marker)
- Color suit pairs (red for hearts/diamonds, black/white for spades/clubs) using ANSI escape codes
- Show foundation pile *next-needed-card* hint (e.g., `♠ 5  next: 6`)
- Mark anchored Kings visually so the player remembers they can't move

**Where it'd go:** `src/solitaire/display.py`. Currently produces plain text — would gain optional ANSI color via a `--color` or `NO_COLOR=1` env-var convention. Keep monochrome path for tests / non-TTY output.

**Why this is non-trivial:** color affects test snapshots and pipe-redirect output. The cleanest approach is a `Display(tableau, foundations, *, color=False)` flag that defaults to off, with `main.py` enabling it when `sys.stdout.isatty()`.

**Tests:** Existing display tests assert on plain-text output. Add a small set of color-mode tests that snapshot the ANSI-laden output.

**Estimate:** 4–6 hours including color mode testing across terminals.

---

## 4. "Is this deal winnable?" classifier

**What:** A small ML or rule-based classifier trained on the 20,000+ saved games that, given a fresh deal's metadata, predicts probability of winning.

**Why:** Players (and autoplay) could decide whether to invest time in a deal before starting. The current `--analyze`-style scripts are descriptive; this would be predictive.

**Approach:**
1. **Features** are already captured in `GameAnalyzer`: `c1_special`, `cN_playable` (six bools), `kings_on_home_row`. Could add features computed from the initial deal: rank distribution per column, number of face-down cards under each face-up card, etc.
2. **Label**: `won == "true"`. We have ~20K labeled examples in `data/`, ~95% loss / ~5% win — class-imbalanced but workable.
3. **Models worth trying** (in order of complexity):
   - Logistic regression on existing features. Probably 60–65% accuracy and well-calibrated probability.
   - Gradient-boosted trees (sklearn's `GradientBoostingClassifier` or `xgboost`). Probably 65–70%.
   - A neural net is overkill for this dataset size.
4. **Train/test split:** 80/20 with stratification on `won`.

**Where it'd go:**
- `src/solitaire/analysis/winnability_classifier.py` — model class with `train(games)` and `predict(metadata)` methods.
- A CLI flag `--predict-win` that, after dealing, prints "estimated win probability: 4.2%" before entering the REPL.
- Or as a standalone tool: `python3 src/predict.py --load data/<file>.md`.

**Caveats:**
- The dataset is autoplay-only. A model trained on it predicts "would `non-blocking` win this deal," not "is this deal theoretically winnable." Still useful, but be honest about that.
- With ~5% positive class, AUC is a better metric than raw accuracy.

**Estimate:** 4–8 hours including data loading, model training, evaluation, and integration. Adds `scikit-learn` (or similar) as a dependency — first non-stdlib runtime dep in the project.

---

## 5. LLM-as-strategy

**What:** Wire an LLM (Claude or otherwise) to play the game as a real strategist — prompted with the current tableau, foundations, and legal moves; returning the chosen move. Compare its win rate against the algorithmic strategies.

**Why:** Validates whether reasoning beats heuristic play on this game. Also a useful demo for using LLMs in game-playing contexts.

**Where it'd go:**
- New strategy class `src/solitaire/autoplay/strategies/llm_strategy.py` implementing `select(game, visible_moves)`.
- Constructor takes a model identifier and prompt template.
- Each turn:
  1. Render the current state as a compact prompt (tableau as text, foundations, legal moves with indices).
  2. Call the LLM with a prompt like "Pick the index (1..N) of the best move. Respond with just the number."
  3. Parse the response back to a move index.
- Cache: an LLM call costs tokens. Don't run 10,000 games of this — maybe 50–100 to start.
- New CLI: `--strategy llm --model <name>`.

**Risks:**
- Cost. 100 games × 30 moves × ~$0.02/call = ~$60 per batch.
- Latency. ~30 minutes of API time for 100 games. Use background flag.
- Determinism. LLMs are stochastic; results aren't directly reproducible.

**What it'd reveal:**
- Whether prompting + reasoning beats `nply-3` lookahead on a small game.
- Whether the LLM's chosen moves track the data-driven advice in `gameplay-hints.md`.

**Estimate:** 4–6 hours including prompt iteration. Adds an SDK dependency (e.g. `anthropic`).

---

## 6. Hybrid strategies (data-driven follow-up)

**What:** The `non-blocking`, `nply-3`, and `reveal-first` strategies all win ~4% of deals but in different sub-regions of deal space. Build a meta-strategy that picks the right base strategy based on deal-time metadata.

**Idea:**
- If `playable_count <= 2` → use `nply-3` (better at low-playable deals — finds wins from "bad" positions)
- If `playable_count >= 5` → use `non-blocking` (better at rich deals — exploits options aggressively)
- Else → use `reveal-first` or `non-blocking`

**Where it'd go:**
- A new `MetaStrategy` class that wraps multiple base strategies and dispatches based on the deal-time analysis.
- Could also be turn-by-turn (call `_evaluate_state` each turn and switch strategies dynamically).

**Why it's interesting:** The 10K-each comparison showed the strategies have different strengths on different deal shapes. Routing should outperform any single strategy. Predicted win rate: 4.5–5%.

**Estimate:** 2–3 hours plus another 10K-runs benchmark to verify.

---

## 7. Replay viewer

**What:** A command that takes a saved game file with a populated `## Moves` section and replays the game move-by-move on the terminal — showing the tableau evolution, with timing controls (`space` to step, `→` to fast-forward, `q` to quit).

**Why:** Makes it possible to study autoplay games or your own past plays. Also useful for debugging strategies.

**Where it'd go:**
- `src/solitaire/replay/replay.py` — class `Replayer(game_file)` with `step()`, `back()`, `play_to_end()`.
- New CLI: `--replay <path>`.
- Reuses `Game.apply()` for state evolution and `Display.render()` for output. The move log is parsed back into `Move` objects (parser already exists in `playground/king_face_down_analysis.py:parse_move_descriptor` — promote it to `src/`).

**Tests:** Replay a known-winning game; assert state matches expected at key checkpoints.

**Estimate:** 3–5 hours.

---

## Empirical findings — what 20K+ games taught us

Carry these forward; they shape what's worth trying next.

- **Strategy choice barely matters at this scale.** `non-blocking`, `nply-3`, and `reveal-first` all win ~4.0–4.2% on random deals (10K each). 95% CI half-width is ~0.4pp, so the differences are within noise. `first` and `random` also land near 4% — even pure random play wins about as often as the smart strategies.
- **Real signal lives in the deal, not the strategy.** Deal-quality features (`playable_count`, `c1_special`, anchored Kings) reliably stratify wins. See `docs/analysis/winnability-signals.md` for the full breakdown.
- **Lookahead doesn't pay off at depth 3.** `nply-3` slightly under-performs `non-blocking` on rich deals (6 playable: 5.5% vs 8.9%). Either we need a much deeper search or a better leaf evaluator. The current evaluator is `foundation_cards + 0.1×face_up`.
- **Sample-size noise is bigger than expected.** First 1K vs next 9K of `reveal-first` differed by 0.46pp on the same strategy. 100-run smoke tests are basically a coin toss — don't draw conclusions from anything under 1K.
- **The anchored-King rule is critical to terminate games.** Without it, autoplay used to ping-pong Kings between empty columns forever and hit the 10K-move cap. With the rule, 0 aborts in 30K+ games.
- **Foundation moves dominate strategically.** Both `non-blocking` and `reveal-first` add a +1.5 bonus to foundation moves to prevent cycling and to nudge progress.
- **King-in-C1 is a real curse.** ~2.7% win rate vs 4.0% baseline — a King at column[0] is anchored and locks C1 until ♠ Q reaches foundation.
- **Ace-in-C1 is a real boon.** ~6.1% win rate. Ace goes to foundation immediately and clears C1 for a King.
- **Per-column playability matters more for deeper columns.** C7 playable boosts win rate ~70%; C2 playable barely moves the needle.

## Gotchas & lessons learned

Hard-won wisdom for future Claude sessions:

- **The protected-test rule is real.** `tests/solitaire/characterization/` cannot be modified without explicit permission. The user has granted permission case-by-case (e.g., for the `LoadedGame` extraction). Always stop and ask; never silently edit.
- **Watch out for uncommitted working-tree changes during analysis.** A buggy change to `src/solitaire/core/move_filter.py` once silently inflated `reveal-first` win rates. Always run `git status` and `git diff` before trusting performance numbers.
- **Use `git add` selectively, not `git add -A`.** Subagents have repeatedly swept untracked save files (`data/*.md`) into commits, polluting the diff. Specify exact paths.
- **Strict Arlo notation has no colon.** `t Game tracks legal moves` — not `t: Game tracks legal moves`. The colon style was used early on; it's been corrected. Future commits should match.
- **No `@staticmethod` anywhere in `src/`.** Only `@classmethod` for alternate constructors (e.g., `Card.from_save_token`). This is a hard rule documented in CLAUDE.md.
- **Use `.venv/bin/pytest`, not bare `pytest`.** The venv has the project's pinned versions.
- **Run the full test suite after every change.** It's sub-second (~300 tests in 0.13s). No reason to skip.
- **`Card` is immutable.** Every modification (e.g., flipping face-up) constructs a new `Card`. Don't try to mutate.
- **Game.apply() has a perf cost now.** It captures `len(MoveFilter(MoveGenerator(self).legal_moves()).visible())` per call to track `legal_moves_per_turn`. Fine for autoplay; might bite future deep-lookahead work. If `nply --depth 5+` becomes slow, make the capture optional.
- **Session continuity:** start a new session by reading `CLAUDE.md` (auto-loaded) then this file's "Project state" + "Empirical findings" sections.

## Tooling reference (`playground/`)

These scripts aren't part of the production code but are useful for analysis:

| Script | Purpose |
|---|---|
| `playground/analyze_strategy.py <strategy-label>` | Win-rate slices by `c1_special`, `kings_on_home_row`, per-column playability, count of playable. Quick view. |
| `playground/winnability_signals.py <strategy-label>` | Deeper analysis with 95% CI significance markers, combined feature buckets, and a composite deal-quality score. The richer tool. |
| `playground/king_face_down_analysis.py` | Per-game analysis of "how many face-down cards remained under a King when it was first moved" — replays each save file's move log. |
| `playground/analyze_non_blocking.py` | Older non-blocking-specific analyzer. Largely subsumed by `analyze_strategy.py`. |
| `playground/md_to_html.py <md-files...>` | Render markdown analysis docs to standalone HTML for browser print-to-PDF. |

**HTML → PDF workflow:** `python3 playground/md_to_html.py docs/analysis/<file>.md` then `open docs/analysis/<file>.html`, then Cmd+P → "Save as PDF" in the browser. The HTML uses a print-friendly stylesheet.

**Generating fresh datasets:** see `docs/batch-commands.md` for the full reference. Quick recipe: `python3 src/main.py --runs 10000 --strategy non-blocking` (with saves) or add `--no-save` for pure-stats runs.

---

## Project state at write time (2026-05-13)

**Tests:** 299 passing. Run with `.venv/bin/pytest`.

**Source structure:**
```
src/solitaire/
├── __init__.py        (__version__ = "0.0.1")
├── display.py         (Display.render() returns string; takes optional foundations)
├── core/
│   ├── card.py        (Card with __eq__/__hash__, RANKS constant, save-token methods)
│   ├── deck.py
│   ├── tableau.py     (Tableau, _RawTableau)
│   ├── foundation.py  (per-suit pile)
│   ├── foundations.py (4-suit container)
│   ├── game.py        (apply, can_apply, snapshot/restore, move log, initial_tableau,
│   │                   metadata, legal_moves_per_turn)
│   ├── move.py        (Move + ColumnDestination + FoundationDestination + anchored-King rule)
│   ├── move_generator.py
│   └── move_filter.py (foundation-preferred filter)
├── persistence/
│   ├── game_file.py   (Markdown save format with deal/final tables, move log, metadata,
│   │                   outcome stats; LoadedGame value object on load)
│   ├── game_registry.py (daily-incrementing IDs)
│   ├── game_analyzer.py (deal-time metadata: c1_special, cN_playable, kings_on_home_row)
│   └── loaded_game.py (value object returned by GameFile.load())
├── repl/
│   ├── repl.py        (Numbered-list REPL; auto-detects win/loss; saves on exit)
│   └── command_parser.py
└── autoplay/
    ├── autoplayer.py
    ├── batch_runner.py
    └── strategies/
        ├── strategy.py (duck-typed protocol; not enforced)
        ├── first_move.py
        ├── random_strategy.py
        ├── non_blocking.py (foundation +1.5 bonus prevents cycling)
        ├── nply.py (recursive search, depth N; evaluator: foundation_cards + 0.1×face_up)
        └── reveal_first.py (+100 reveal-face-down, +1.5 foundation, +len(future) tiebreak)
```

**Save file format (current):**
- Markdown with front-matter style metadata at the top
- `## Initial Deal` (always) and `## Final State` (omitted on win) — pipe tables of cards
- `## Moves` section: numbered list of move descriptions (e.g., `7♥ from C2 moved to C1`)
- Header fields:
  - `version`, deal metadata (`c1_special`, `cN_playable`, `kings_on_home_row`), `strategy`
  - Outcome: `won`, `foundation_cards`, `moves`
  - Outcome stats: `time_to_first_foundation`, `face_down_at_end`, `stuck_threshold_move`, `legal_moves_per_turn`
- `LoadedGame.prior_metadata` excludes outcome keys — they're recomputed every save

**CLI features:**
- `--no-save` skip persistence
- `--load <path>` load a saved game (drops into REPL)
- `--debug` reveal face-down cards
- `--autoplay --strategy <name>` run autoplay (skips REPL)
- Strategies: `first`, `random`, `non-blocking`, `nply --depth N`, `reveal-first`
- `--runs N` batch autoplay with summary stats (incompatible with `--load`)

**Conventions:**
- TDD with strict Arlo notation (`t`, `r`, `R`, `F`, `b`, `d`) — single character, no colon
- Smalltalk-inspired OOP, no `@staticmethod` (only `@classmethod` for alternate constructors)
- Tests in `tests/solitaire/unit/` are AI-editable; `tests/solitaire/characterization/` is PROTECTED
- Trunk-based development on `main`

**Documentation layout:**
- `CLAUDE.md` — auto-loaded project guide (rules, structure, conventions)
- `README.md` — project front door
- `docs/rules.md`, `docs/gameplay.md` — game rules and user guide
- `docs/gameplay-hints.md` — data-driven advice for human players
- `docs/batch-commands.md` — autoplay batch command reference
- `docs/future-features-plan.md` — this file
- `docs/development-journal.md` — historical log
- `docs/analysis/` — dataset writeups (`winnability-signals.md`, `thousand-non-blocking-games.md`, `thousand-nply-3-games.md`, plus `.html` siblings for printing)
- `docs/superpowers/` — original specs and plans (historical, do not edit)

**Key data assets:**
- Up to 20,000+ autoplay save files in `data/` (cleaned periodically; regenerate via batch commands)
- Analysis scripts in `playground/` — see Tooling reference above
- Detailed findings: `docs/analysis/winnability-signals.md` (10K games, with significance), `docs/analysis/thousand-non-blocking-games.md`, `docs/analysis/thousand-nply-3-games.md`
