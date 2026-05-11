from solitaire.card import Card
from solitaire.deck import Deck

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
