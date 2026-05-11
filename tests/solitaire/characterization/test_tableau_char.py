# PROTECTED: do not modify without explicit human permission

from solitaire.deck import Deck
from solitaire.tableau import Tableau
from tests.solitaire.assertions import expect_tableau

def make_tableau():
    deck = Deck()
    deck.shuffle()
    return Tableau(deck)

def test_deal_produces_exactly_52_cards():
    tableau = make_tableau()
    total = sum(len(col) for col in tableau.columns)
    assert total == 52

def test_deal_produces_a_complete_standard_deck():
    deck = Deck()
    tableau = Tableau(deck)
    all_cards = [card for col in tableau.columns for card in col]
    suits = {c.suit for c in all_cards}
    ranks = {c.rank for c in all_cards}
    assert suits == {"♠", "♥", "♦", "♣"}
    assert ranks == {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"}

def test_c1_has_one_face_up_card():
    expect_tableau(make_tableau()).column(1).to_have_face_up_count(1)

def test_c1_has_no_face_down_cards():
    expect_tableau(make_tableau()).column(1).to_have_face_down_count(0)

def test_c2_has_one_face_down_card():
    expect_tableau(make_tableau()).column(2).to_have_face_down_count(1)

def test_c2_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(2).to_have_face_up_count(5)

def test_c3_has_two_face_down_cards():
    expect_tableau(make_tableau()).column(3).to_have_face_down_count(2)

def test_c3_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(3).to_have_face_up_count(5)

def test_c4_has_three_face_down_cards():
    expect_tableau(make_tableau()).column(4).to_have_face_down_count(3)

def test_c4_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(4).to_have_face_up_count(5)

def test_c5_has_four_face_down_cards():
    expect_tableau(make_tableau()).column(5).to_have_face_down_count(4)

def test_c5_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(5).to_have_face_up_count(5)

def test_c6_has_five_face_down_cards():
    expect_tableau(make_tableau()).column(6).to_have_face_down_count(5)

def test_c6_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(6).to_have_face_up_count(5)

def test_c7_has_six_face_down_cards():
    expect_tableau(make_tableau()).column(7).to_have_face_down_count(6)

def test_c7_has_five_face_up_cards():
    expect_tableau(make_tableau()).column(7).to_have_face_up_count(5)
