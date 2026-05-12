# src/solitaire/core/foundation.py

from solitaire.core.card import RANKS


class Foundation:
    def __init__(self, suit: str):
        self._suit = suit
        self._cards = []

    def is_suit(self, suit: str) -> bool:
        return self._suit == suit

    @property
    def size(self) -> int:
        return len(self._cards)

    @property
    def top(self):
        return self._cards[-1] if self._cards else None

    @property
    def is_complete(self) -> bool:
        return self.size == len(RANKS)

    def can_accept(self, card) -> bool:
        if card.suit != self._suit:
            return False
        if not self._cards:
            return card.rank == "A"
        top_idx = RANKS.index(self._cards[-1].rank)
        if top_idx + 1 >= len(RANKS):
            return False
        return card.rank == RANKS[top_idx + 1]

    def add(self, card) -> None:
        assert self.can_accept(card), f"Cannot add {card.rank}{card.suit} to {self._suit} foundation"
        self._cards.append(card)
