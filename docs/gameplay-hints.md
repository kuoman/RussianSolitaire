# Gameplay Hints — Yukon Russian Solitaire

Practical wisdom for human players, derived from analysing 20,000+ autoplay games across multiple strategies. The numbers come from the `non-blocking` and `nply-3` strategies, but the signals are deal-structure properties, not strategy artifacts — they describe what makes a *deal itself* easier or harder.

## How hard is the game?

Across every strategy tested (`first`, `random`, `non-blocking`, `nply-3`, `reveal-first`), autoplay wins about **4% of random deals**. Most deals are either mathematically unwinnable or require lookahead far deeper than three plies to solve. Don't be discouraged by losing — many deals are unwinnable from the start.

## Reading a fresh deal — the "is this winnable?" checklist

After the deal is dealt and you can see the seven columns, look for these structural features. They're listed in order of how strongly they predict winnability.

### 1. Count the playable columns (strongest signal)

For each column C2 through C7, look at the bottom face-up card. Is there a same-suit, one-rank-higher card face-up *somewhere else* on the tableau? If yes, that column is "playable" — you have a legal first move targeting it.

| Playable count (out of 6) | Win rate | What it means |
|---|---|---|
| 0–1 | < 1.5% | Effectively unwinnable. Quit and re-deal. |
| 2 | ~2% | Difficult, low-percentage. |
| 3 | ~3.7% | Average. |
| 4 | ~4.6% | Above average. |
| 5 | ~7.4% | Strong deal. |
| 6 | ~9% | Excellent — play it carefully. |

Most deals (~63%) have 3 or 4 playable columns. Going from 3 to 5 nearly doubles your odds.

### 2. C1 special card

If column 1 (the lone face-up card) is an Ace or King, it changes your odds:

- **Ace in C1**: ~6.1% win rate (vs 4.0% baseline). The Ace goes straight to foundation — costs you nothing and clears C1 for a King.
- **King in C1**: ~2.7% win rate (vs 4.0% baseline). The King is anchored and can't move except to its foundation, locking C1 until spades climb to Q.
- **Anything else**: baseline odds.

### 3. Anchored Kings on C2–C7

Look at the bottom face-up card of columns C2 through C7. Each column whose first face-up card is a King has an "anchored King" — that King can't move to another column under the standard rule.

| Anchored Kings | Win rate |
|---|---|
| 0 | ~4.3% |
| 1 | ~3.9% (basically baseline) |
| 2+ | ~2.4% — game-ending impact |

One anchored King barely affects your odds. Two or more is a structural problem that few deals overcome.

### 4. Per-column playability (which columns matter most)

Among C2–C7, the deeper columns are the most predictive when playable:

- **C7 playable** is the single strongest column-level signal — about a 70% relative boost when it has a target.
- **C6 playable** is second-strongest.
- **C5 and C3 playable** are real but smaller.
- **C2 and C4 playable** trend positive but are within statistical noise.

This makes intuitive sense: deeper columns hide more cards. Making C7 playable unlocks far more potential progress than making C2 playable.

## Combined deal quality

If you want a single rough score:

```
deal_quality = playable_count − 2 × anchored_kings + (1 if C1 == Ace else 0)
```

| Score | Win rate |
|---|---|
| ≤ −2 | ~2% (very difficult) |
| −1 to 1 | ~3% (below average) |
| 2 to 4 | ~4% (typical) |
| 5+ | ~7%+ (good deal) |
| 6+ | ~8%+ (excellent) |

The score is rough — the real signals are stronger when combined non-linearly. But it's a useful one-number summary at deal time.

## In-game tactical wisdom (from the data and analysis)

These tips came up consistently across analyses:

1. **Move Aces to foundation immediately.** This is unambiguously correct. Aces in foundation are needed before anything else can build there, and an Ace stuck in the tableau blocks a column.

2. **Don't move Kings prematurely.** Games where Kings move while many face-down cards remain underneath them tend to lose. Kings moved with 0–1 face-down cards beneath them correlate with wins; Kings moved with 5–6 face-down underneath correlate with losses. Translation: only commit a King to a different column when you're already deep in the game and the rest of the board is in good shape.

3. **Foundation moves usually beat column moves.** When the same card can go either to a column or to foundation, the foundation play is almost always correct. Yukon Russian is a "build up" game — cards on foundation are progress; cards on the tableau are still fragile.

4. **Empty columns are expensive.** Only Kings can fill them, so vacating a column without a King ready to use it wastes the slot.

5. **Anchored Kings are dead weight.** A King at the bottom of a column can only go to its foundation. Don't try to "rescue" it — focus on getting `♠ A through Q` to foundation so the anchored `♠ K` can finally move. Until then, the column's other cards are your only resource there.

6. **If you started with a "≤ −2" deal, expect to lose.** It's not your play; it's the deal. If the game has been around five minutes and you're not making progress, the deal is most likely unwinnable.

## Caveats

- Numbers are from autoplay strategies, not human play. A skilled human with foresight may win at higher rates, especially on borderline deals.
- "Win rate" mixes deal winnability with strategy quality. The strategies tested here are simple greedy heuristics; a perfect-play solver would identify which deals are theoretically winnable and might show a different shape.
- Statistical confidence intervals at 10,000 games are roughly ±0.4 percentage points. Numbers like "4.05% vs 4.21%" are not meaningfully different. Numbers like "2.4% vs 4.3%" are.

## Source data

- 20,000+ autoplay games across `non-blocking` and `nply-3` strategies
- Analysis scripts: `playground/winnability_signals.py`, `playground/king_face_down_analysis.py`
- Detailed writeups: `docs/analysis/winnability-signals.md`, `docs/analysis/thousand-non-blocking-games.md`, `docs/analysis/thousand-nply-3-games.md`
