# Thousand Non-Blocking Games

**Dataset:** 1,103 Yukon Russian Solitaire games autoplayed with the `non-blocking` strategy.
**Date analysed:** 2026-05-12.
**Source:** `data/*.md` save files filtered by `strategy: non-blocking`.
**Analysis script:** `playground/analyze_non_blocking.py`.

---

## Overall

- **Games played:** 1,103
- **Total wins:** 40 (**3.63%**)

The `non-blocking` strategy wins about 1 in 28 deals.

---

## Win rate by C1 special card

The first column's only card is dealt face-up. Some deals start with an Ace or King in that slot.

| C1 card | Wins / Games | Win rate |
|---------|--------------|----------|
| A | 4 / 95 | 4.21% |
| K | 2 / 83 | 2.41% |
| none | 34 / 925 | 3.68% |

An Ace in C1 wins slightly more often than the baseline; a King wins less. Sample sizes (95 and 83 games) are small enough that these differences are within noise — an Ace's tiny advantage makes intuitive sense (immediate foundation play available) but isn't statistically conclusive at this dataset size.

---

## Win rate by `kings_on_home_row`

`kings_on_home_row` counts how many of columns C2–C7 have a King as their first face-up card. Anchored Kings (Kings at `column[0]`) cannot move except to the foundation.

| Kings on home row | Wins / Games | Win rate |
|-------------------|--------------|----------|
| 0 | 30 / 676 | **4.44%** |
| 1 | 10 / 367 | 2.72% |
| 2 | 0 / 54 | 0.00% |
| 3 | 0 / 6 | 0.00% |

This is a real signal. Each anchored King reduces win rate sharply:

- 0 anchored Kings → 4.44%
- 1 anchored King → 2.72% (38% relative drop)
- 2 anchored Kings → 0 wins in 54 games
- 3 anchored Kings → 0 wins in 6 games

This matches the anchored-King domain rule: a King at `column[0]` permanently locks that column until it goes to foundation. Two locked columns out of seven means most of the board can't be reorganized productively.

### Distribution

| Kings | Games | Share |
|-------|-------|-------|
| 0 | 676 | 61.29% |
| 1 | 367 | 33.27% |
| 2 | 54 | 4.90% |
| 3 | 6 | 0.54% |

About 95% of deals have at most one anchored King. Three or more is rare.

---

## Win rate by individual column playability

`cN_playable` is `true` when column N's first face-up card has a same-suit, one-rank-higher partner face-up somewhere else on the tableau (i.e., a legal first move exists for that column).

| Column | Playable: wins/games (rate) | Not playable: wins/games (rate) |
|--------|------------------------------|-----------------------------------|
| C2 | 19/593 (3.20%) | 21/510 (4.12%) |
| C3 | 24/579 (4.15%) | 16/524 (3.05%) |
| C4 | 23/583 (3.95%) | 17/520 (3.27%) |
| C5 | 31/572 (**5.42%**) | 9/531 (1.69%) |
| C6 | 30/589 (**5.09%**) | 10/514 (1.95%) |
| C7 | 27/616 (4.38%) | 13/487 (2.67%) |

C5 and C6 playability are the strongest individual signals — having a target available roughly **triples** win rate (5.42% vs 1.69%, 5.09% vs 1.95%). C3, C4, and C7 show milder positive correlations. C2 is mildly inverted, likely a quirk of how non-blocking interacts with C2's shallow stack (only 6 cards, mostly face-up at deal time).

---

## Win rate by count of playable columns

This aggregates the per-column flags into a single deal-quality count, ranging 0–6.

| Playable count | Wins / Games | Win rate |
|----------------|--------------|----------|
| 0 | 0 / 7 | 0.00% |
| 1 | 0 / 73 | 0.00% |
| 2 | 4 / 203 | 1.97% |
| 3 | 10 / 377 | 2.65% |
| 4 | 17 / 311 | **5.47%** |
| 5 | 6 / 114 | 5.26% |
| 6 | 3 / 18 | **16.67%** |

A clear monotonic-ish trend. Roughly:

- **0–1 playable** → effectively unwinnable for `non-blocking` (0 wins in 80 games)
- **2–3 playable** → below average (~2%)
- **4–5 playable** → above average (~5%)
- **6 playable** → very rare (1.6% of deals) but win rate jumps to 16.67% (3/18)

The 4-playable bucket holds the largest share of wins (17/40, 42.5%) since it's both common and above-average.

---

## Combined takeaways

1. **More playable columns at deal time means higher win rate.** Roughly linear from 2 to 4, with a possible spike at 6 playable.
2. **C5 and C6 are the most predictive individual columns** — playability there is a much stronger signal than C2's.
3. **Anchored Kings hurt sharply.** Two or more anchored Kings have produced zero wins in 60 games.
4. **C1 advantage is weak.** Ace-in-C1 trends positive but is noise at this sample size; King-in-C1 trends negative for similar-noise reasons.
5. The deal-time metadata (`c1_special`, `cN_playable`, `kings_on_home_row`) collectively captures meaningful, predictive information about winnability. A composite deal-quality score like `4 × playable_count − 6 × kings_on_home_row + (2 if c1 == "A" else 0)` might stratify wins cleanly — worth testing against a larger dataset.

---

## Caveats

- This dataset is autoplay-only. Human play with foresight would presumably win more often, and the per-feature correlations may shift.
- The `non-blocking` strategy itself biases the data — its preference for preserving future move count is one specific heuristic among many.
- All deals were freshly shuffled. Some deals are mathematically unwinnable; the wins/total ratios mix "strategy quality" with "deal winnability."
- Sample sizes for rare buckets (`kings_on_home_row >= 2`, 6 playable columns, etc.) are small. Treat percentages there as suggestive rather than precise.
