# Russian Solitaire Rules

## Overview
Russian Solitaire is a single-player card game variant of Yukon. The key difference from Yukon is that tableau building is **by suit** instead of by alternate color, making it significantly more challenging.

## Setup
- **Deck**: Single standard 52-card deck
- **Tableau**: 7 columns with 1, 6, 7, 8, 9, 10, 11 cards respectively
  - The **top up to 5 cards** in each column are face-up; the remainder are face-down
  - Column 1 has a single card, which is face-up
  - Columns 2 and 3 are entirely face-up (6 and 7 cards, but only the top 5 are
    "exposed" — face-down cards exist only when the column has more than 5)
  - Columns 4–7 each have face-down cards underneath their top 5 face-up cards
- **Stock**: None — all 52 cards are dealt at the start (no draw pile)
- **Foundations**: 4 piles, one per suit, initially empty

## Objective
Build all four foundation piles from Ace to King by suit.

## Foundation Building
- Foundations build **upward by suit** (Ace → King)
- Only cards in ascending rank order and matching suit can be placed
- Example: A♠ → 2♠ → 3♠ → ... → K♠

## Tableau Building
- Tableau columns build **downward by suit** (King → Ace)
- **Critical Rule**: Cards must be same suit (not alternate color like Yukon)
- Example: 5♥ can only be placed on 6♥ (not on 6♣ or 6♠)

## Moving Cards
- **Single cards**: Any face-up card can be moved if it follows building rules
- **Card groups**: Multiple cards can be moved together as a group
  - Only the **top card of the group** and **target card** must follow the building rule
  - Cards underneath the top card can be in any order
  - Example: Stack has 5♥-3♦-9♣-2♠ (top to bottom). Moving onto 6♥, all four cards move together

## Revealing Cards
- When a face-down card becomes the top card of a tableau column, it is immediately turned face-up
- Empty columns can be filled with any King (and any cards beneath it)

## Anchored King Rule (House Rule)

This implementation enforces an **Anchored King** constraint:

- A King that is the **deepest (bottommost) card** of its column — i.e. the
  one originally dealt face-up at column index 0 — is *anchored*.
- An anchored King may only be moved by sending it **directly to its
  foundation** as a single card. It cannot lead a same-suit run into another
  column, and it cannot move with cards on top of it.
- A King that ends up at the bottom of an empty column after moving (e.g. a
  King moved from one tableau pile to a freshly-emptied column) is not
  anchored by this rule until/unless it is the originally-dealt deepest
  card of its column.

In practice: each of the seven columns starts with one face-up card at its
bottom; if that card is a King, it stays put — only foundation play can
remove it. This prevents pathological "infinite re-King" reshuffling.

## Winning
The game is won when all four foundations are complete (A through K in each suit).

## Strategy
- Expose face-down cards as quickly as possible
- Move Aces to foundations immediately when available
- Create empty columns to increase maneuverability
- The suit-matching requirement makes this significantly harder than Yukon - careful planning is essential
