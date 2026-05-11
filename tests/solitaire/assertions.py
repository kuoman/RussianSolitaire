class CardAssertion:
    def __init__(self, card):
        self._card = card

    def to_have_suit(self, suit):
        assert self._card.suit == suit, f"Expected suit {suit!r}, got {self._card.suit!r}"
        return self

    def and_rank(self, rank):
        assert self._card.rank == rank, f"Expected rank {rank!r}, got {self._card.rank!r}"
        return self

    def and_be_face_up(self):
        assert self._card.face_up, "Expected card to be face-up"
        return self

    def and_be_face_down(self):
        assert not self._card.face_up, "Expected card to be face-down"
        return self

    def and_render_as(self, text, debug=False):
        actual = self._card.render(debug=debug)
        assert actual == text, f"Expected render {text!r}, got {actual!r}"
        return self


class DeckAssertion:
    def __init__(self, deck):
        self._deck = deck

    def to_have_card_count(self, count):
        actual = len(self._deck.cards)
        assert actual == count, f"Expected {count} cards, got {actual}"
        return self

    def to_contain_all_suits_and_ranks(self):
        suits = {"♠", "♥", "♦", "♣"}
        ranks = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}
        found_suits = {c.suit for c in self._deck.cards}
        found_ranks = {c.rank for c in self._deck.cards}
        assert found_suits == suits, f"Missing suits: {suits - found_suits}"
        assert found_ranks == ranks, f"Missing ranks: {ranks - found_ranks}"
        return self


class ColumnAssertion:
    def __init__(self, column):
        self._column = column

    def to_have_card_count(self, count):
        actual = len(self._column)
        assert actual == count, f"Expected {count} cards in column, got {actual}"
        return self

    def to_have_face_up_count(self, count):
        actual = sum(1 for c in self._column if c.face_up)
        assert actual == count, f"Expected {count} face-up cards, got {actual}"
        return self

    def to_have_face_down_count(self, count):
        actual = sum(1 for c in self._column if not c.face_up)
        assert actual == count, f"Expected {count} face-down cards, got {actual}"
        return self


class TableauAssertion:
    def __init__(self, tableau):
        self._tableau = tableau

    def to_have_column_count(self, count):
        actual = len(self._tableau.columns)
        assert actual == count, f"Expected {count} columns, got {actual}"
        return self

    def column(self, number):
        return ColumnAssertion(self._tableau.columns[number - 1])


def expect_card(card):
    return CardAssertion(card)

def expect_deck(deck):
    return DeckAssertion(deck)

def expect_tableau(tableau):
    return TableauAssertion(tableau)
