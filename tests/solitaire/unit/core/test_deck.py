from solitaire.core.deck import Deck
from tests.solitaire.assertions import expect_deck


def test_deck_has_52_cards():
    deck = Deck()
    expect_deck(deck).to_have_card_count(52)


def test_deck_contains_all_suits_and_ranks():
    deck = Deck()
    expect_deck(deck).to_contain_all_suits_and_ranks()


def test_deal_removes_cards_from_deck():
    deck = Deck()
    dealt = deck.deal(5)
    assert len(dealt) == 5
    expect_deck(deck).to_have_card_count(47)


def test_deal_returns_cards_from_top():
    deck = Deck()
    top_card = deck.cards[0]
    dealt = deck.deal(1)
    assert dealt[0] is top_card
