# tests/solitaire/unit/test_game_analyzer.py
from solitaire.card import Card
from solitaire.tableau import _RawTableau
from solitaire.game_analyzer import GameAnalyzer


def make_column(*cards):
    return list(cards)


def make_tableau(columns):
    return _RawTableau(columns)


def face_up(suit, rank):
    return Card(suit, rank, face_up=True)


def face_down(suit, rank):
    return Card(suit, rank, face_up=False)


def test_c1_special_is_A_when_c1_is_ace():
    tableau = make_tableau([
        make_column(face_up("♠", "A")),
        make_column(face_down("♥", "3"), face_up("♥", "5"), face_up("♣", "6"), face_up("♦", "7"), face_up("♠", "8"), face_up("♣", "9")),
        make_column(face_down("♠", "2"), face_down("♦", "4"), face_up("♣", "5"), face_up("♥", "6"), face_up("♠", "7"), face_up("♦", "8"), face_up("♣", "9")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "8"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "K")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "K"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["c1_special"] == "A"


def test_c1_special_is_K_when_c1_is_king():
    tableau = make_tableau([
        make_column(face_up("♠", "K")),
        make_column(face_down("♥", "3"), face_up("♥", "5"), face_up("♣", "6"), face_up("♦", "7"), face_up("♠", "8"), face_up("♣", "9")),
        make_column(face_down("♠", "2"), face_down("♦", "4"), face_up("♣", "5"), face_up("♥", "6"), face_up("♠", "7"), face_up("♦", "8"), face_up("♣", "9")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "8"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "K")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "K"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["c1_special"] == "K"


def test_c1_special_is_none_when_c1_is_not_ace_or_king():
    tableau = make_tableau([
        make_column(face_up("♠", "7")),
        make_column(face_down("♥", "3"), face_up("♥", "5"), face_up("♣", "6"), face_up("♦", "7"), face_up("♠", "8"), face_up("♣", "9")),
        make_column(face_down("♠", "2"), face_down("♦", "4"), face_up("♣", "5"), face_up("♥", "6"), face_up("♠", "7"), face_up("♦", "8"), face_up("♣", "9")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "8"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "K")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "K"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["c1_special"] == "none"


def test_column_is_playable_when_higher_same_suit_exists():
    # C2 first face-up card is 7♥ — 8♥ is face-up in C3
    tableau = make_tableau([
        make_column(face_up("♠", "5")),
        make_column(face_down("♦", "3"), face_up("♥", "7"), face_up("♠", "9"), face_up("♦", "J"), face_up("♣", "Q"), face_up("♠", "K")),
        make_column(face_down("♦", "2"), face_down("♣", "4"), face_up("♥", "8"), face_up("♠", "10"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "8"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "K")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "K"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["c2_playable"] == "true"


def test_column_is_not_playable_when_higher_same_suit_missing():
    # C2 first face-up card is 7♥ — no 8♥ face-up anywhere
    tableau = make_tableau([
        make_column(face_up("♠", "5")),
        make_column(face_down("♦", "3"), face_up("♥", "7"), face_up("♠", "9"), face_up("♦", "J"), face_up("♣", "Q"), face_up("♠", "K")),
        make_column(face_down("♦", "2"), face_down("♣", "4"), face_up("♠", "8"), face_up("♠", "10"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "9"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "K")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "K"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["c2_playable"] == "false"


def test_king_first_face_up_is_not_playable():
    # C2 first face-up card is K♠ — no rank higher than K
    tableau = make_tableau([
        make_column(face_up("♠", "5")),
        make_column(face_down("♦", "3"), face_up("♠", "K"), face_up("♥", "9"), face_up("♦", "J"), face_up("♣", "Q"), face_up("♥", "2")),
        make_column(face_down("♦", "2"), face_down("♣", "4"), face_up("♠", "8"), face_up("♠", "10"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "8"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "K")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "K"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♥", "A"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["c2_playable"] == "false"


def test_analyse_returns_all_seven_keys():
    from solitaire.deck import Deck
    from solitaire.tableau import Tableau
    tableau = Tableau(Deck())
    result = GameAnalyzer.analyse(tableau)
    assert set(result.keys()) == {"c1_special", "c2_playable", "c3_playable", "c4_playable", "c5_playable", "c6_playable", "c7_playable"}


def test_kings_on_home_row_is_zero_when_no_kings_are_first_face_up():
    from solitaire.deck import Deck
    from solitaire.tableau import Tableau
    # Use a standard unshuffled deck — unlikely to have kings as first face-up
    # Build a tableau where no column C2-C7 has a King as first face-up
    tableau = make_tableau([
        make_column(face_up("♠", "5")),
        make_column(face_down("♦", "3"), face_up("♥", "7"), face_up("♠", "9"), face_up("♦", "J"), face_up("♣", "Q"), face_up("♠", "2")),
        make_column(face_down("♦", "2"), face_down("♣", "4"), face_up("♠", "8"), face_up("♠", "10"), face_up("♦", "Q"), face_up("♣", "3"), face_up("♥", "2")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "9"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♣", "9"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "3")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "2"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "2"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["kings_on_home_row"] == 0


def test_kings_on_home_row_counts_kings_as_first_face_up_in_c2_to_c7():
    # C2 and C5 have King as first face-up card
    tableau = make_tableau([
        make_column(face_up("♠", "5")),
        make_column(face_down("♦", "3"), face_up("♠", "K"), face_up("♠", "9"), face_up("♦", "J"), face_up("♣", "Q"), face_up("♠", "2")),
        make_column(face_down("♦", "2"), face_down("♣", "4"), face_up("♠", "8"), face_up("♠", "10"), face_up("♦", "Q"), face_up("♣", "3"), face_up("♥", "2")),
        make_column(face_down("♥", "2"), face_down("♠", "4"), face_down("♦", "6"), face_up("♣", "7"), face_up("♥", "9"), face_up("♠", "9"), face_up("♦", "10"), face_up("♣", "J")),
        make_column(face_down("♣", "2"), face_down("♥", "4"), face_down("♠", "6"), face_down("♦", "8"), face_up("♥", "K"), face_up("♥", "10"), face_up("♠", "J"), face_up("♦", "Q"), face_up("♣", "3")),
        make_column(face_down("♥", "3"), face_down("♦", "5"), face_down("♣", "7"), face_down("♠", "9"), face_down("♥", "J"), face_up("♦", "Q"), face_up("♣", "2"), face_up("♥", "2"), face_up("♠", "3"), face_up("♦", "4")),
        make_column(face_down("♣", "3"), face_down("♥", "5"), face_down("♠", "7"), face_down("♦", "9"), face_down("♣", "J"), face_down("♥", "Q"), face_up("♠", "2"), face_up("♦", "2"), face_up("♣", "3"), face_up("♥", "4"), face_up("♠", "5")),
    ])
    result = GameAnalyzer.analyse(tableau)
    assert result["kings_on_home_row"] == 2


def test_kings_on_home_row_is_in_analyse_result_keys():
    from solitaire.deck import Deck
    from solitaire.tableau import Tableau
    tableau = Tableau(Deck())
    result = GameAnalyzer.analyse(tableau)
    assert "kings_on_home_row" in result
