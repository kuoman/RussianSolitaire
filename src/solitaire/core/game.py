from solitaire.core.card import Card
from solitaire.core.foundations import Foundations


class Game:
    def __init__(self, tableau, foundations=None):
        self._tableau = tableau
        self._foundations = foundations if foundations is not None else Foundations()
        self._moves = []

    @property
    def tableau(self):
        return self._tableau

    @property
    def foundations(self):
        return self._foundations

    @property
    def moves(self) -> list:
        return self._moves

    @property
    def is_won(self) -> bool:
        return self._foundations.is_complete

    def can_apply(self, move) -> bool:
        return move.is_legal_on(self._tableau, self._foundations)

    def apply(self, move) -> None:
        assert self.can_apply(move), f"Illegal move: {move}"
        columns = self._tableau.columns
        source_col = columns[move.source_column]
        n = move.count
        moving_cards = source_col[-n:]
        columns[move.source_column] = source_col[:-n]

        destination = move.destination
        if destination.is_column():
            columns[destination.column_index()].extend(moving_cards)

        self._moves.append(move)
