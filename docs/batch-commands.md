# Batch Commands

Reference commands for running each autoplay strategy at different volumes. All commands run from the project root.

Add `--no-save` to any command to suppress the per-game `data/*.md` files (useful for the larger batches).

Strategies:
- `first` — picks the first legal move from the foundation-preferred filtered list
- `random` — picks uniformly at random from legal moves
- `non-blocking` — prefers moves that preserve the most future options (foundation moves get a small bonus)
- `nply --depth N` — recursive lookahead to depth N, scores by `foundations.total_cards + 0.1 * face_up_count`
- `reveal-first` — heavy bonus (+100) for moves that flip a face-down card, small bonus (+1.5) for foundation moves; future-move count breaks ties

---

## 1 Play

Single-game smoke runs. Each writes one save file to `data/`.

```bash
python3 src/main.py --autoplay --strategy first
python3 src/main.py --autoplay --strategy random
python3 src/main.py --autoplay --strategy non-blocking
python3 src/main.py --autoplay --strategy nply --depth 3
python3 src/main.py --autoplay --strategy reveal-first
```

---

## 100 Plays

Quick statistical sample — useful for sanity checks. Each command saves 100 files unless `--no-save` is added.

```bash
python3 src/main.py --runs 100 --strategy first
python3 src/main.py --runs 100 --strategy random
python3 src/main.py --runs 100 --strategy non-blocking
python3 src/main.py --runs 100 --strategy nply --depth 3
python3 src/main.py --runs 100 --strategy reveal-first
```

Or without saving:

```bash
python3 src/main.py --runs 100 --strategy first --no-save
python3 src/main.py --runs 100 --strategy random --no-save
python3 src/main.py --runs 100 --strategy non-blocking --no-save
python3 src/main.py --runs 100 --strategy nply --depth 3 --no-save
python3 src/main.py --runs 100 --strategy reveal-first --no-save
```

---

## 1,000 Plays

Mid-size dataset for finding real signal in deal-time metadata.

```bash
python3 src/main.py --runs 1000 --strategy first
python3 src/main.py --runs 1000 --strategy random
python3 src/main.py --runs 1000 --strategy non-blocking
python3 src/main.py --runs 1000 --strategy nply --depth 3
python3 src/main.py --runs 1000 --strategy reveal-first
```

Or without saving:

```bash
python3 src/main.py --runs 1000 --strategy first --no-save
python3 src/main.py --runs 1000 --strategy random --no-save
python3 src/main.py --runs 1000 --strategy non-blocking --no-save
python3 src/main.py --runs 1000 --strategy nply --depth 3 --no-save
python3 src/main.py --runs 1000 --strategy reveal-first --no-save
```

---

## 10,000 Plays

Large batch — useful for tightening confidence intervals on rare buckets (kings_on_home_row >= 2, 6 playable columns, etc.). The `nply --depth 3` run will be slow; expect tens of minutes.

Always pair with `--no-save` for a run this large unless you really want 10,000 markdown files in `data/`.

```bash
python3 src/main.py --runs 10000 --strategy first --no-save
python3 src/main.py --runs 10000 --strategy random --no-save
python3 src/main.py --runs 10000 --strategy non-blocking --no-save
python3 src/main.py --runs 10000 --strategy nply --depth 3 --no-save
python3 src/main.py --runs 10000 --strategy reveal-first --no-save
```

---

## Analysing the saved data

After a batch with saves enabled, run the analyser script for any strategy label:

```bash
python3 playground/analyze_strategy.py first
python3 playground/analyze_strategy.py random
python3 playground/analyze_strategy.py non-blocking
python3 playground/analyze_strategy.py nply-3
python3 playground/analyze_strategy.py reveal-first
```

The script slices win rate by `c1_special`, `kings_on_home_row`, individual `cN_playable` flags, and the count of playable columns.
