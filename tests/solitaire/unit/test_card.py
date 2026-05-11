import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from solitaire.card import Card
from tests.solitaire.assertions import expect_card

def test_card_has_suit_and_rank():
    card = Card("♠", "A")
    expect_card(card).to_have_suit("♠").and_rank("A")
