# src/solitaire/core/foundations.py
from solitaire.core.foundation import Foundation


class Foundations:
    SUITS = ("♠", "♥", "♦", "♣")

    def __init__(self):
        self._by_suit = {suit: Foundation(suit) for suit in self.SUITS}

    @property
    def total_cards(self) -> int:
        return sum(f.size for f in self._by_suit.values())

    @property
    def is_complete(self) -> bool:
        return self.total_cards == 52

    def for_suit(self, suit: str) -> Foundation:
        return self._by_suit[suit]

    def can_accept(self, card) -> bool:
        return self.for_suit(card.suit).can_accept(card)

    def add(self, card) -> None:
        self.for_suit(card.suit).add(card)
