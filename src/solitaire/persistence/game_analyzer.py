# src/solitaire/game_analyzer.py
from solitaire.core.card import RANKS
from solitaire.core.tableau import COLUMN_SIZES

_NUM_COLUMNS = len(COLUMN_SIZES)


class GameAnalyzer:
    def __init__(self, tableau):
        self._tableau = tableau

    def analyse(self) -> dict:
        metadata = {}
        metadata["c1_special"] = self._c1_special()
        metadata.update(self._column_playability())
        metadata["kings_on_home_row"] = self._kings_on_home_row()
        return metadata

    def _c1_special(self) -> str:
        c1_card = self._tableau.columns[0][0]
        return c1_card.rank if c1_card.rank in ("A", "K") else "none"

    def _column_playability(self) -> dict:
        all_face_up = [
            card
            for col in self._tableau.columns
            for card in col
            if card.face_up
        ]
        result = {}
        for col_idx in range(1, _NUM_COLUMNS):
            first_face_up = self._first_face_up(self._tableau.columns[col_idx])
            key = f"c{col_idx + 1}_playable"
            if first_face_up is None or first_face_up.rank == "K":
                result[key] = "false"
                continue
            target_rank = RANKS[RANKS.index(first_face_up.rank) + 1]
            playable = any(
                card.suit == first_face_up.suit
                and card.rank == target_rank
                and card is not first_face_up
                for card in all_face_up
            )
            result[key] = "true" if playable else "false"
        return result

    def _kings_on_home_row(self) -> int:
        count = 0
        for col_idx in range(1, _NUM_COLUMNS):
            first = self._first_face_up(self._tableau.columns[col_idx])
            if first is not None and first.rank == "K":
                count += 1
        return count

    def _first_face_up(self, column):
        return next((card for card in column if card.face_up), None)
