from solitaire.core.card import Card
from solitaire.core.deck import Deck

COLUMN_SIZES = [1, 6, 7, 8, 9, 10, 11]


class Tableau:
    def __init__(self, deck: Deck):
        self.columns = []
        for i, size in enumerate(COLUMN_SIZES):
            cards = deck.deal(size)
            face_down_count = 0 if i == 0 else size - 5
            column = [
                Card(card.suit, card.rank, face_up=(j >= face_down_count))
                for j, card in enumerate(cards)
            ]
            self.columns.append(column)


class _RawTableau:
    def __init__(self, columns: list, prior_moves=None, prior_metadata=None):
        self.columns = columns
        self.prior_moves = list(prior_moves) if prior_moves else []
        self.prior_metadata = dict(prior_metadata) if prior_metadata else {}
