# tests/solitaire/unit/core/test_foundation.py
import pytest
from solitaire.core.card import Card
from solitaire.core.foundation import Foundation


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def test_new_foundation_has_size_zero():
    foundation = Foundation("♠")
    assert foundation.size == 0


def test_new_foundation_has_no_top():
    foundation = Foundation("♠")
    assert foundation.top is None


def test_foundation_is_suit_true_for_its_own_suit():
    foundation = Foundation("♥")
    assert foundation.is_suit("♥") is True


def test_foundation_is_suit_false_for_other_suit():
    foundation = Foundation("♥")
    assert foundation.is_suit("♠") is False


def test_empty_foundation_accepts_ace_of_its_suit():
    foundation = Foundation("♠")
    assert foundation.can_accept(face_up("♠", "A")) is True


def test_empty_foundation_rejects_ace_of_other_suit():
    foundation = Foundation("♠")
    assert foundation.can_accept(face_up("♥", "A")) is False


def test_empty_foundation_rejects_non_ace_of_its_suit():
    foundation = Foundation("♠")
    assert foundation.can_accept(face_up("♠", "5")) is False


def test_add_increases_size():
    foundation = Foundation("♠")
    foundation.add(face_up("♠", "A"))
    assert foundation.size == 1


def test_top_is_last_added_card():
    foundation = Foundation("♠")
    ace = face_up("♠", "A")
    foundation.add(ace)
    assert foundation.top is ace


def test_foundation_with_ace_accepts_two_of_same_suit():
    foundation = Foundation("♠")
    foundation.add(face_up("♠", "A"))
    assert foundation.can_accept(face_up("♠", "2")) is True


def test_foundation_with_ace_rejects_three_of_same_suit():
    foundation = Foundation("♠")
    foundation.add(face_up("♠", "A"))
    assert foundation.can_accept(face_up("♠", "3")) is False


def test_foundation_with_ace_rejects_two_of_different_suit():
    foundation = Foundation("♠")
    foundation.add(face_up("♠", "A"))
    assert foundation.can_accept(face_up("♥", "2")) is False


def test_foundation_accepts_full_sequence_to_king():
    foundation = Foundation("♠")
    for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
        assert foundation.can_accept(face_up("♠", rank)) is True
        foundation.add(face_up("♠", rank))
    assert foundation.size == 13
    assert foundation.is_complete is True


def test_incomplete_foundation_is_not_complete():
    foundation = Foundation("♠")
    foundation.add(face_up("♠", "A"))
    assert foundation.is_complete is False
