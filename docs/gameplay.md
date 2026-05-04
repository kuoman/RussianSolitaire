# Russian Solitaire Gameplay

## Game Flow

### Initial Setup
1. Shuffle a standard 52-card deck
2. Deal 7 tableau columns:
   - Column 1: 1 card
   - Column 2: 6 cards (top 5 face-up, bottom 1 face-down)
   - Column 3: 7 cards (top 5 face-up, bottom 2 face-down)
   - Column 4: 8 cards (top 5 face-up, bottom 3 face-down)
   - Column 5: 9 cards (top 5 face-up, bottom 4 face-down)
   - Column 6: 10 cards (top 5 face-up, bottom 5 face-down)
   - Column 7: 11 cards (top 5 face-up, bottom 6 face-down)
3. Set up 4 empty foundation piles

### Player Actions

On each turn, a player can:

1. **Move a card or group to another tableau column**
   - Select a face-up card from any column
   - Move it (and any cards on top of it) to another column where the target card is one rank higher and the same suit
   - Example: Move 5♠ onto 6♠

2. **Move a card to a foundation**
   - Move an Ace to an empty foundation to start that suit
   - Move the next card in sequence to an existing foundation
   - Example: If foundation has A♥-2♥, can move 3♥

3. **Move a King to an empty column**
   - Any King (with cards beneath it) can be moved to an empty tableau column
   - This is critical for creating space and revealing cards

4. **Automatic reveals**
   - When a face-down card is exposed (becomes the top card), it automatically flips face-up

### Valid Moves

#### Tableau to Tableau
- **Target**: Must be one rank higher and same suit
- **Moving**: Can move a single card or a group starting from that card
- Cards below the selected card don't need to be in sequence

#### Tableau to Foundation
- **Ace**: Can move to any empty foundation
- **Other cards**: Must be next in sequence (one rank higher) and same suit as the foundation

#### King to Empty Column
- Any King can start a new tableau column
- Useful for freeing up cards and creating space

### Game End

The game ends when:
- **Win**: All four foundations are complete (A through K)
- **Loss**: No more legal moves available and foundations are not complete

## Example Turn Sequence

1. Look for Aces and move them to foundations
2. Scan tableau for moves that reveal face-down cards
3. Build sequences in tableau by suit (downward)
4. Move cards to foundations when possible
5. Create empty columns by moving Kings when strategic
6. Continue until win or no moves remain

## Tips

- **Priority 1**: Move Aces to foundations immediately
- **Priority 2**: Reveal face-down cards
- **Priority 3**: Build long same-suit sequences
- **Empty columns**: Save for strategic King moves
- **Planning**: Think several moves ahead - the suit restriction makes the game much tighter than other solitaire variants
