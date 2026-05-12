# Russian Solitaire Gameplay

This document covers both the abstract game flow and the concrete user
interface of the Python implementation. For the formal rules, see
[`rules.md`](rules.md).

## Running the Program

```bash
python3 src/main.py                                    # new shuffled deal, autosaved, REPL
python3 src/main.py --no-save                          # play without writing to ./data
python3 src/main.py --debug                            # show face-down ranks (with a *)
python3 src/main.py --load data/2026-05-12-000003.md   # resume a saved game
python3 src/main.py --autoplay                         # autoplay (default strategy: first)
python3 src/main.py --autoplay --strategy non-blocking
python3 src/main.py --autoplay --strategy nply --depth 3
```

### Reading the Display

```
Foundations: ♠--  ♥A  ♦--  ♣--

 C1   C2   C3   C4   C5   C6   C7
4♥   K♠   ##   ##   ##   ##   ##
     7♣   ##   ##   ##   ##   ##
     ...
```

- The **Foundations** header shows the top rank of each suit's foundation,
  or `--` if empty.
- Columns `C1`..`C7` are displayed left-to-right, with the deal's *deepest*
  card on top of each column (closest to the header).
- Face-down cards render as `##` in normal mode, or `*<rank><suit>` in
  `--debug` mode (e.g. `*7♥`).

### Making Moves

After each render the REPL prints a numbered list of every legal move and a
prompt:

```
Available moves:
  1. A♥ from C4 moved to foundation
  2. K♣ from C2 moved to C5
  ...
>
```

You can enter:

| Input | Meaning |
|-------|---------|
| `1` (a number) | Play the corresponding move from the list |
| `7h c2 moved to c5` | Long form — move 7♥ from column 2 to column 5 |
| `Ah c4 moved to f` | Long form — move A♥ from column 4 to its foundation |
| `q` or `quit` | Quit (autosaves on exit unless `--no-save`) |
| `?`, `h`, or `help` | Show command help |

Suit letters: `s ♠`, `h ♥`, `d ♦`, `c ♣` (case-insensitive; unicode also accepted).
Destinations: `c1`..`c7` for tableau columns, `f` for foundation.

The list is filtered: if a card has a legal foundation move, the equivalent
tableau-only move for the same source-and-stack is hidden to keep the menu
tight and steer play toward foundations first.

### End of Game

- **Win** — when all four foundations are complete the REPL prints
  `You won! Congratulations.` and exits.
- **Loss / stuck** — when no legal moves remain the REPL prints
  `No legal moves remain. Game over.` and exits.
- Either way the final state, outcome, and full move log are written back
  to the original save file (unless `--no-save`).

## Save Files

Games persist as Markdown files under `./data/` named
`YYYY-MM-DD-NNNNNN.md`, with `NNNNNN` an incrementing per-day counter
(`GameRegistry`).

A save contains:

1. `# Game <id>` heading
2. Header metadata: `version`, deal-shape analysis (`c1_special`,
   `cN_playable`, `kings_on_home_row`), and outcome (`won`,
   `foundation_cards`, `moves`, `strategy`,
   `time_to_first_foundation`, `face_down_at_end`,
   `stuck_threshold_move`, `legal_moves_per_turn`)
3. A pipe-table representation of the tableau — face-down cards prefixed
   with `*`
4. `## Moves` — numbered list of moves played in this session

Outcome metric definitions:
- `time_to_first_foundation` — 1-indexed move number of the first foundation move, or `none`.
- `face_down_at_end` — count of face-down cards in the final tableau.
- `stuck_threshold_move` — 1-indexed first move where visible-legal-move count became ≤2 and stayed ≤2 through game-end, or `none`.
- `legal_moves_per_turn` — comma-separated visible-legal-move counts before each move (length equals total moves).

Saves are overwritten on game end so each file always reflects the latest
state. To replay from the original deal you would need to re-shuffle; saves
are designed for resuming, not for replaying from scratch.

## Autoplay

`--autoplay` runs a strategy headlessly until the game is won, gets stuck,
or hits a 10 000-move safety cap.

| Strategy | Behaviour |
|----------|-----------|
| `first` (default) | Pick the first legal move from the visible list |
| `non-blocking` | One-move lookahead; pick the move that leaves the most legal follow-ups (foundation moves get a small bonus) |
| `nply --depth N` | N-ply minimax; leaf evaluation is `foundation_cards + 0.1 * face_up_cards` |
| `random` | Pick uniformly at random from the visible legal moves each turn |
| `reveal-first` | Heavy bonus (+100) for moves that flip a face-down card, small bonus (+1.5) for foundation moves; future-move count breaks ties |

When autoplay finishes the program prints e.g.
`Result: won after 142 moves (52 cards on foundations)` and saves the result
just like the REPL.

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
   - **Exception (Anchored King rule):** a King that is the originally-dealt
     bottom card of its column is anchored — it can only leave by going to
     the foundation as a single card. See [`rules.md`](rules.md) for details.

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
