# tests/solitaire/unit/core/test_foundations.py
import pytest
from solitaire.core.card import Card
from solitaire.core.foundation import Foundation
from solitaire.core.foundations import Foundations


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def test_new_foundations_total_cards_is_zero():
    foundations = Foundations()
    assert foundations.total_cards == 0


def test_new_foundations_is_not_complete():
    foundations = Foundations()
    assert foundations.is_complete is False


def test_for_suit_returns_a_foundation_for_each_suit():
    foundations = Foundations()
    for suit in ("♠", "♥", "♦", "♣"):
        f = foundations.for_suit(suit)
        assert isinstance(f, Foundation)
        assert f.is_suit(suit) is True


def test_for_suit_returns_same_foundation_each_call():
    foundations = Foundations()
    a = foundations.for_suit("♠")
    b = foundations.for_suit("♠")
    assert a is b


def test_for_suit_raises_for_unknown_suit():
    foundations = Foundations()
    with pytest.raises(KeyError):
        foundations.for_suit("X")


def test_can_accept_delegates_to_correct_suit():
    foundations = Foundations()
    assert foundations.can_accept(face_up("♠", "A")) is True
    assert foundations.can_accept(face_up("♠", "5")) is False


def test_add_delegates_to_correct_suit():
    foundations = Foundations()
    foundations.add(face_up("♠", "A"))
    assert foundations.for_suit("♠").size == 1
    assert foundations.for_suit("♥").size == 0


def test_total_cards_sums_all_four_foundations():
    foundations = Foundations()
    foundations.add(face_up("♠", "A"))
    foundations.add(face_up("♥", "A"))
    foundations.add(face_up("♥", "2"))
    assert foundations.total_cards == 3


def test_is_complete_true_when_all_52_cards_added():
    foundations = Foundations()
    for suit in ("♠", "♥", "♦", "♣"):
        for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            foundations.add(face_up(suit, rank))
    assert foundations.total_cards == 52
    assert foundations.is_complete is True
