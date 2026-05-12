import random
from solitaire.core.card import Card, RANKS

SUITS = ["♠", "♥", "♦", "♣"]


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n: int) -> list:
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt
