# Winnability Signals in Yukon Russian Solitaire

**Dataset:** 10,000 Yukon Russian Solitaire games autoplayed with the `non-blocking` strategy.
**Date analysed:** 2026-05-12.
**Source:** `data/*.md` save files, all `strategy: non-blocking`.
**Analysis script:** `playground/winnability_signals.py`.

This is a follow-up to `thousand-non-blocking-games.md` with a 10× larger sample. With ~10,000 deals we have proper statistical power on the rare buckets that the earlier 1,103-game writeup couldn't speak to with confidence.

---

## Overall

- **Games played:** 10,000
- **Total wins:** 405 (**4.05% ± 0.39**, 95% CI)
- **Avg moves per game:** 16.9
- **Avg foundation cards at end:** 4.8
- **Aborted games:** 0 (anchored-King fix is holding)

The non-blocking strategy wins about 1 in 25 deals — a slightly higher rate than the earlier 1,103-game sample (3.63%) but well within its confidence interval.

---

## Significance methodology

For each slice of the data, the analysis script computes the win rate and the 95% CI half-width using a normal approximation: `1.96 × √(p(1−p)/n)`. A signal is flagged with `*` when its delta from baseline exceeds the half-width AND is greater than 0.5 percentage points. Negative signals exceeding the half-width are flagged `(low)`.

This is a rough significance check (treats each game as independent, which they are; ignores multiple-testing correction, which would shrink some borderline calls). Treat single-asterisk results as "real but modest" and unflagged results as "within noise."

---

## Single-feature signals

### `c1_special` (Ace, King, or none in column 1)

| C1 card | Wins / Games | Win rate ± CI | Δ vs baseline |
|---------|--------------|----------------|---------------|
| A | 49 / 797 | 6.15% ± 1.67 | **+2.10** * |
| K | 21 / 774 | 2.71% ± 1.14 | **−1.34** (low) |
| none | 335 / 8,429 | 3.97% ± 0.42 | −0.08 |

**Both the Ace bonus and the King penalty are statistically significant.** An Ace in C1 lifts win rate from ~4% to ~6% — a ~50% relative boost. A King has the opposite effect.

The 1,103-game sample couldn't detect either signal because the Ace bucket had only 95 games and the King bucket 83. Tenfold more data resolves the ambiguity.

Why it makes sense: an Ace in C1 is an immediate foundation play that costs nothing — the C1 column had only one card to begin with. A King in C1 is anchored there for the entire game (anchored-King rule), permanently locking C1 until spades climb to Q.

### `kings_on_home_row`

| Kings | Wins / Games | Win rate ± CI | Δ |
|-------|--------------|----------------|---|
| 0 | 260 / 6,046 | 4.30% ± 0.51 | +0.25 |
| 1 | 130 / 3,327 | 3.91% ± 0.66 | −0.14 |
| 2 | 14 / 589 | 2.38% ± 1.23 | **−1.67** (low) |
| 3 | 1 / 37 | 2.70% ± 5.23 | −1.35 (small N) |
| 4 | 0 / 1 | — | — |

**Only 2+ anchored Kings is a real signal.** The earlier 1,103-game sample suggested 1 King hurt (2.72% vs 4.44%), but that result doesn't replicate with 10× the data. With 3,327 single-King games we now see 3.91% — within 0.66 percentage points of baseline. That earlier finding was a small-sample fluke.

Two anchored Kings cuts win rate from ~4% to ~2.4%. Three anchored Kings shows a similar drag but the sample (37 games) is too small to be confident.

### Per-column playability

| Column | Playable: rate ± CI | Not playable: rate ± CI | Δ |
|--------|----------------------|---------------------------|---|
| C2 | 4.43% ± 0.54 | 3.58% ± 0.54 | +0.85 (borderline) |
| C3 | **4.62% ± 0.56** | 3.39% ± 0.52 | **+1.23** * |
| C4 | 4.40% ± 0.55 | 3.64% ± 0.54 | +0.76 (borderline) |
| C5 | **4.71% ± 0.56** | 3.27% ± 0.52 | **+1.44** * |
| C6 | **4.91% ± 0.58** | 3.03% ± 0.50 | **+1.88** * |
| C7 | **4.98% ± 0.58** | 2.94% ± 0.49 | **+2.04** * |

**Four columns show real signals: C3, C5, C6, C7.** The effect strengthens as you move right — C7 playability is the strongest individual column predictor, with about a 70% relative win-rate boost when its first face-up card has a same-suit-one-rank-higher target available elsewhere.

C2 and C4 effects are positive but don't quite cross the threshold. They likely represent real but small advantages.

The pattern makes sense: deeper columns have more cards, so making their bottom face-up card playable unlocks deeper sequences that would otherwise be stranded. Shallower columns offer less upside even when playable.

---

## Aggregate signal: count of playable columns

This is the single strongest predictor in the dataset.

| Playable count | Wins / Games | Win rate ± CI | Δ |
|----------------|--------------|----------------|---|
| 0 | 0 / 77 | 0.00% | **−4.05** (low) |
| 1 | 8 / 561 | 1.43% ± 0.98 | **−2.62** (low) |
| 2 | 39 / 1,905 | 2.05% ± 0.64 | **−2.00** (low) |
| 3 | 121 / 3,236 | 3.74% ± 0.65 | −0.31 |
| 4 | 130 / 2,818 | 4.61% ± 0.77 | +0.56 |
| 5 | 88 / 1,189 | **7.40% ± 1.49** | **+3.35** * |
| 6 | 19 / 214 | **8.88% ± 3.81** | **+4.83** * |

The relationship is monotonic and nearly linear from 1 to 5 playable. The jump from 4 to 5 playable nearly *doubles* the win rate.

**The bottom and top of the distribution are striking.** With 0 playable columns (0 wins in 77 games) you're effectively guaranteed to lose under non-blocking. With 6 playable (only 2.1% of deals) you win at over 2× the baseline rate.

Most deals (54%) have 3 or 4 playable columns and sit near the baseline.

---

## Combined signals

The single best combinations of `kings_on_home_row` and `playable_count` (filtered to buckets with N ≥ 20):

| Kings | Playable | Win rate ± CI | Sample | Δ |
|-------|----------|----------------|--------|---|
| 0 | 6 | 8.88% ± 3.81 | 214 | +4.83 |
| 1 | 5 | 7.85% ± 3.82 | 191 | +3.80 |
| 0 | 5 | **7.31% ± 1.62** | 998 | **+3.26** |
| 1 | 4 | 5.52% ± 1.55 | 834 | +1.47 |
| 0 | 4 | 4.31% ± 0.91 | 1,927 | +0.26 |

The most reliably "good" combination, with the most games in its bucket, is **0 anchored Kings + 5 playable columns** (998 games, 7.31% win rate).

The bottom of the same table:

| Kings | Playable | Win rate | Sample |
|-------|----------|----------|--------|
| 0 | 1 | 0.00% | 203 |
| 1 | 0 | 0.00% | 31 |
| 0 | 0 | 0.00% | 22 |
| 2 | 1 | 1.02% ± 1.99 | 98 |
| 2 | 4 | 1.75% ± 3.41 | 57 |

The "0 Kings + 1 playable" bucket is the standout dud: 203 games, zero wins. Anchored Kings + few playable columns compound to near-zero winnability.

---

## Composite deal-quality score

`score = playable_count − 2·kings_on_home_row + (1 if c1 == "A" else 0)`

This rough hand-tuned combination uses what the data identifies as the strongest signals.

| Score | Wins / Games | Win rate | Δ |
|-------|--------------|----------|---|
| ≤ −4 | 0 / 45 | 0.00% | −4.05 |
| −3 | 1 / 99 | 1.01% ± 1.97 | −3.04 (low) |
| −2 | 5 / 231 | 2.16% ± 1.88 | −1.89 (low) |
| −1 | 14 / 444 | 3.15% ± 1.63 | −0.90 |
| 0 | 18 / 853 | 2.11% ± 0.96 | −1.94 (low) |
| 1 | 38 / 1,358 | 2.80% ± 0.88 | −1.25 (low) |
| 2 | 62 / 1,678 | 3.69% ± 0.90 | −0.36 |
| 3 | 84 / 1,983 | 4.24% ± 0.89 | +0.19 |
| 4 | 79 / 1,960 | 4.03% ± 0.87 | −0.02 |
| 5 | 80 / 1,073 | **7.46% ± 1.57** | **+3.41** * |
| 6 | 21 / 260 | **8.08% ± 3.31** | **+4.03** * |
| 7 | 3 / 16 | 18.75% ± 19.13 | small N |

The score stratifies the dataset cleanly — but only at the extremes. From scores 0 to 4 the win rate hovers near baseline. The big jumps are below score −2 (clearly unwinnable) and at score 5+ (significantly above baseline).

A simple unweighted score isn't quite enough to predict winnability across the full range. A logistic regression or weighted feature model would likely separate scores 0–4 better.

---

## Five takeaways

1. **Count of playable columns is the strongest single predictor.** Below 3 playable → losing odds. At 5+ → win rate roughly doubles.
2. **An Ace in C1 is a real ~50% boost.** A King in C1 is a real penalty.
3. **C7 playability is the strongest individual column signal.** Effect strengthens deeper in the tableau (C2 < C3 < C5 < C6 < C7).
4. **One anchored King does NOT hurt at this sample size.** The earlier impression that it did was a small-sample fluke. Two anchored Kings is the threshold for real damage.
5. **The combined sweet spot is 0–1 anchored Kings AND 5+ playable columns.** Roughly 12% of deals hit this profile and win at almost twice the baseline rate.

---

## Caveats

- Dataset is autoplay-only. The same deal-time signals may behave differently under human play with foresight.
- All correlations are conditional on the `non-blocking` strategy. The earlier `nply-3` analysis showed a different signal pattern (weaker per-column effects, an inverted Kings-on-home-row signal at low counts, lookahead finding wins from "bad" deal positions). Different strategies "see" different deals as winnable.
- Deals are randomly shuffled. Some are mathematically unwinnable; what we call "win rate" mixes "deal winnability" with "strategy quality."
- Significance check is normal-approximation-based and ignores multiple-testing correction. Borderline single-asterisk results should be treated as "real but modest," not "definitely real."
