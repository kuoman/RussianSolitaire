import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from solitaire.core.card import Card
from tests.solitaire.assertions import expect_card

def test_card_has_suit_and_rank():
    card = Card("♠", "A")
    expect_card(card).to_have_suit("♠").and_rank("A")

def test_card_is_face_down_by_default():
    card = Card("♥", "K")
    expect_card(card).and_be_face_down()

def test_card_can_be_face_up():
    card = Card("♦", "5", face_up=True)
    expect_card(card).and_be_face_up()

def test_face_up_card_renders_as_rank_and_suit():
    card = Card("♠", "A", face_up=True)
    expect_card(card).and_render_as("A♠")

def test_face_up_ten_renders_as_three_chars():
    card = Card("♥", "10", face_up=True)
    expect_card(card).and_render_as("10♥")

def test_face_down_card_renders_as_block():
    card = Card("♣", "Q", face_up=False)
    expect_card(card).and_render_as("░░")

def test_face_down_card_renders_with_star_prefix_in_debug_mode():
    card = Card("♣", "Q", face_up=False)
    expect_card(card).and_render_as("*Q♣", debug=True)

def test_face_up_card_to_save_token_has_no_prefix():
    card = Card("♠", "A", face_up=True)
    assert card.to_save_token() == "A♠"

def test_face_down_ten_to_save_token_uses_star_prefix():
    card = Card("♥", "10", face_up=False)
    assert card.to_save_token() == "*10♥"

def test_from_save_token_parses_face_up_card():
    card = Card.from_save_token("A♠")
    expect_card(card).to_have_suit("♠").and_rank("A").and_be_face_up()

def test_from_save_token_parses_face_down_ten():
    card = Card.from_save_token("*10♥")
    expect_card(card).to_have_suit("♥").and_rank("10").and_be_face_down()

def test_save_token_round_trip_face_up_ace():
    original = Card("♠", "A", face_up=True)
    restored = Card.from_save_token(original.to_save_token())
    expect_card(restored).to_have_suit("♠").and_rank("A").and_be_face_up()

def test_save_token_round_trip_face_down_ten():
    original = Card("♥", "10", face_up=False)
    restored = Card.from_save_token(original.to_save_token())
    expect_card(restored).to_have_suit("♥").and_rank("10").and_be_face_down()

def test_save_token_round_trip_face_up_king_of_clubs():
    original = Card("♣", "K", face_up=True)
    restored = Card.from_save_token(original.to_save_token())
    expect_card(restored).to_have_suit("♣").and_rank("K").and_be_face_up()

def test_save_token_round_trip_face_down_two_of_diamonds():
    original = Card("♦", "2", face_up=False)
    restored = Card.from_save_token(original.to_save_token())
    expect_card(restored).to_have_suit("♦").and_rank("2").and_be_face_down()
