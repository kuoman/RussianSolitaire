from solitaire.core.card import Card
from solitaire.core.foundations import Foundations
from solitaire.core.tableau import _RawTableau


class Game:
    def __init__(self, tableau, foundations=None, prior_moves=None, metadata=None):
        self._tableau = tableau
        self._initial_columns = [list(col) for col in tableau.columns]
        self._foundations = foundations if foundations is not None else Foundations()
        self._moves = []
        self._session_descriptions = []
        self._prior_descriptions = list(prior_moves) if prior_moves else []
        self._metadata = dict(metadata) if metadata else {}

    @property
    def tableau(self):
        return self._tableau

    @property
    def initial_tableau(self):
        return _RawTableau([list(col) for col in self._initial_columns])

    @property
    def metadata(self) -> dict:
        return dict(self._metadata)

    @property
    def foundations(self):
        return self._foundations

    @property
    def moves(self) -> list:
        return self._moves

    @property
    def move_descriptions(self) -> list:
        return self._prior_descriptions + self._session_descriptions

    @property
    def total_moves(self) -> int:
        return len(self._prior_descriptions) + len(self._session_descriptions)

    @property
    def is_won(self) -> bool:
        return self._foundations.is_complete

    def can_apply(self, move) -> bool:
        return move.is_legal_on(self._tableau, self._foundations)

    def apply(self, move) -> None:
        assert self.can_apply(move), f"Illegal move: {move}"
        # Capture description BEFORE mutating so source card is correctly named.
        self._session_descriptions.append(move.describe(self._tableau))

        columns = self._tableau.columns
        source_col = columns[move.source_column]
        n = move.count
        moving_cards = source_col[-n:]
        columns[move.source_column] = source_col[:-n]

        destination = move.destination
        if destination.is_column():
            columns[destination.column_index()].extend(moving_cards)
        elif destination.is_foundation():
            self._foundations.add(moving_cards[0])

        new_source_col = columns[move.source_column]
        if new_source_col and not new_source_col[-1].face_up:
            exposed = new_source_col[-1]
            new_source_col[-1] = Card(exposed.suit, exposed.rank, face_up=True)

        self._moves.append(move)

    def snapshot(self):
        return {
            "columns": [list(col) for col in self._tableau.columns],
            "foundations": {
                suit: self._foundations.for_suit(suit).snapshot()
                for suit in ("♠", "♥", "♦", "♣")
            },
            "moves": list(self._moves),
            "session_descriptions": list(self._session_descriptions),
        }

    def restore(self, snap) -> None:
        for i, col in enumerate(snap["columns"]):
            self._tableau.columns[i] = list(col)
        for suit, cards in snap["foundations"].items():
            self._foundations.for_suit(suit).restore(cards)
        self._moves = list(snap["moves"])
        self._session_descriptions = list(snap["session_descriptions"])
