from solitaire.core.deck import Deck
from solitaire.core.tableau import Tableau
from solitaire.display import Display


def make_fixed_tableau():
    deck = Deck()  # unshuffled, deterministic
    return Tableau(deck)


def test_display_includes_foundation_header():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    assert "Foundations: ♠--  ♥--  ♦--  ♣--" in output


def test_display_includes_column_headers():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    assert "C1" in output
    assert "C7" in output


def test_display_shows_face_down_as_blocks_in_normal_mode():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    assert "░░" in output
    assert "*" not in output


def test_display_has_eleven_card_rows():
    tableau = make_fixed_tableau()
    output = Display(tableau).render()
    lines = output.strip().split("\n")
    card_lines = [l for l in lines if any(s in l for s in ["♠", "♥", "♦", "♣", "░░"]) and "Foundations" not in l]
    assert len(card_lines) == 11


def test_display_shows_star_prefix_for_face_down_in_debug_mode():
    tableau = make_fixed_tableau()
    output = Display(tableau, debug=True).render()
    assert "*" in output
    assert "░░" not in output


def test_display_normal_mode_has_no_star_prefix():
    tableau = make_fixed_tableau()
    output = Display(tableau, debug=False).render()
    assert "*" not in output
