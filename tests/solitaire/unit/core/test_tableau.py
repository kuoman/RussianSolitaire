from solitaire.core.deck import Deck
from solitaire.core.tableau import Tableau
from tests.solitaire.assertions import expect_tableau


def test_tableau_has_seven_columns():
    deck = Deck()
    tableau = Tableau(deck)
    expect_tableau(tableau).to_have_column_count(7)


def test_tableau_column_sizes():
    deck = Deck()
    tableau = Tableau(deck)
    expected_sizes = [1, 6, 7, 8, 9, 10, 11]
    for i, size in enumerate(expected_sizes, start=1):
        expect_tableau(tableau).column(i).to_have_card_count(size)


def test_column_1_has_one_face_up_card():
    deck = Deck()
    tableau = Tableau(deck)
    expect_tableau(tableau).column(1).to_have_face_up_count(1)


def test_column_1_has_no_face_down_cards():
    deck = Deck()
    tableau = Tableau(deck)
    expect_tableau(tableau).column(1).to_have_face_down_count(0)


def test_columns_2_to_7_have_five_face_up_cards():
    deck = Deck()
    tableau = Tableau(deck)
    for col in range(2, 8):
        expect_tableau(tableau).column(col).to_have_face_up_count(5)


def test_columns_2_to_7_face_down_counts():
    deck = Deck()
    tableau = Tableau(deck)
    expected_face_down = [1, 2, 3, 4, 5, 6]
    for col, expected in zip(range(2, 8), expected_face_down):
        expect_tableau(tableau).column(col).to_have_face_down_count(expected)
