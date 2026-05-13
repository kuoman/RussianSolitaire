# Thousand N-ply (depth 3) Games

**Dataset:** 1,100 Yukon Russian Solitaire games autoplayed with the `nply --depth 3` strategy.
**Date analysed:** 2026-05-12.
**Source:** `data/*.md` save files filtered by `strategy: nply-3`.
**Analysis script:** `playground/analyze_strategy.py`.

---

## Overall

- **Games played:** 1,100
- **Total wins:** 41 (**3.73%**)

The `nply --depth 3` strategy wins about 1 in 27 deals — essentially identical to `non-blocking`'s 3.63%. The interesting differences are in *which* deals each strategy wins.

---

## Win rate by C1 special card

| C1 card | Wins / Games | Win rate |
|---------|--------------|----------|
| A | 3 / 74 | 4.05% |
| K | 3 / 97 | 3.09% |
| none | 35 / 929 | 3.77% |

Like with `non-blocking`, an Ace in C1 trends positive and a King trends negative, but sample sizes (74 and 97 games) keep the differences within noise.

---

## Win rate by `kings_on_home_row`

This is where `nply-3` diverges most from `non-blocking`.

| Kings on home row | Wins / Games | Win rate |
|-------------------|--------------|----------|
| 0 | 18 / 639 | 2.82% |
| 1 | 23 / 398 | **5.78%** |
| 2 | 0 / 56 | 0.00% |
| 3 | 0 / 7 | 0.00% |

**Inverted signal.** With 1 King anchored on the home row, `nply-3` wins more than twice as often as it does with 0 (5.78% vs 2.82%). For `non-blocking` the relationship is the reverse (4.44% with 0 anchored Kings, dropping to 2.72% with 1).

Hypothesis: `nply-3`'s lookahead can find foundation-building paths that *use* an anchored King — it's a guaranteed late-game foundation play once spades climb to Q. `non-blocking`'s "preserve future options" heuristic treats the same King as a constraint and avoids working around it. With 0 anchored Kings, `nply-3`'s lookahead has more freedom but also more decision noise; with 1 King, the constraint focuses the search toward viable lines.

2+ anchored Kings still kills both strategies dead — that's a structural barrier no strategy in the dataset has cracked.

### Distribution

| Kings | Games | Share |
|-------|-------|-------|
| 0 | 639 | 58.09% |
| 1 | 398 | 36.18% |
| 2 | 56 | 5.09% |
| 3 | 7 | 0.64% |

---

## Win rate by individual column playability

| Column | Playable: wins/games (rate) | Not playable: wins/games (rate) |
|--------|------------------------------|-----------------------------------|
| C2 | 22/590 (3.73%) | 19/510 (3.73%) |
| C3 | 26/607 (4.28%) | 15/493 (3.04%) |
| C4 | 24/587 (4.09%) | 17/513 (3.31%) |
| C5 | 20/588 (3.40%) | 21/512 (4.10%) |
| C6 | 26/583 (**4.46%**) | 15/517 (2.90%) |
| C7 | 28/618 (**4.53%**) | 13/482 (2.70%) |

`nply-3`'s per-column signals are flatter than `non-blocking`'s. C6 and C7 still trend positive — having a target gives ~50% better odds — but the differences are smaller than non-blocking's (where C5 and C6 playability roughly *tripled* the win rate).

C5 is mildly *inverted* under nply-3 (3.40% playable vs 4.10% not), the opposite of non-blocking's strongest signal column.

The takeaway: **lookahead reduces dependence on any single deal-time feature.** Where `non-blocking` leans heavily on C5–C6 playability, `nply-3` finds wins more uniformly across deal shapes.

---

## Win rate by count of playable columns

| Playable count | Wins / Games | Win rate |
|----------------|--------------|----------|
| 0 | 0 / 8 | 0.00% |
| 1 | 3 / 72 | **4.17%** |
| 2 | 6 / 212 | 2.83% |
| 3 | 10 / 354 | 2.82% |
| 4 | 12 / 286 | 4.20% |
| 5 | 7 / 137 | 5.11% |
| 6 | 3 / 31 | **9.68%** |

The standout cell here is **1 playable column → 4.17% win rate** (3/72). Compare with `non-blocking`: 0 wins out of 73 games in that bucket. This is the lookahead pay-off — `nply-3` finds wins in deals that simpler heuristics give up on.

The trade-off: with 6 playable columns (the rich deals), `nply-3` wins 9.68% (3/31) versus `non-blocking`'s 16.67% (3/18). Lookahead doesn't capitalize on good deals as aggressively.

Mid-range deals (2–5 playable) show comparable win rates between the two strategies.

---

## Combined takeaways

1. **Same overall win rate, very different play patterns.** Both strategies win ~3.7% of deals, but `nply-3` finds wins in deals `non-blocking` rejects (1 playable column) while `non-blocking` exploits rich deals (6 playable) more aggressively.
2. **The Kings-on-home-row inversion is the most striking finding.** Anchored Kings can *help* when paired with lookahead by reducing search-space ambiguity. Worth digging deeper — does the King-friendly bias hold up at higher depths?
3. **`nply-3`'s per-column signals are flatter** — lookahead reduces dependence on any single feature.
4. **Both strategies fail completely with 2+ anchored Kings.** A hard structural barrier.
5. **Ensemble or hybrid strategies might outperform either alone.** Try `nply` for low-playable deals, `non-blocking` for high-playable. Or augment `nply`'s leaf evaluator with a "preserve future options" term.

---

## Caveats

- Autoplay-only data — human play with foresight may show different correlations.
- `nply --depth 3` evaluator is `foundations.total_cards + 0.1 * face_up_count`. Different evaluators or depths may shift these numbers significantly.
- All deals freshly shuffled; some are mathematically unwinnable. Wins/total ratios mix strategy quality with deal winnability.
- Sample sizes for rare buckets (`kings_on_home_row >= 2`, 0–1 playable columns, 6 playable columns) are small. Treat percentages there as suggestive rather than precise.
