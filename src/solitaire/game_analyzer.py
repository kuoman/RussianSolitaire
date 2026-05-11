# src/solitaire/game_analyzer.py
from solitaire.tableau import COLUMN_SIZES

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
_NUM_COLUMNS = len(COLUMN_SIZES)


class GameAnalyzer:
    @staticmethod
    def analyse(tableau) -> dict:
        metadata = {}

        c1_card = tableau.columns[0][0]
        metadata["c1_special"] = c1_card.rank if c1_card.rank in ("A", "K") else "none"

        all_face_up = [
            card
            for col in tableau.columns
            for card in col
            if card.face_up
        ]

        for col_idx in range(1, _NUM_COLUMNS):
            col = tableau.columns[col_idx]
            first_face_up = next((card for card in col if card.face_up), None)
            key = f"c{col_idx + 1}_playable"

            if first_face_up is None or first_face_up.rank == "K":
                metadata[key] = "false"
                continue

            rank_idx = RANKS.index(first_face_up.rank)
            target_rank = RANKS[rank_idx + 1]

            playable = any(
                card.suit == first_face_up.suit
                and card.rank == target_rank
                and card is not first_face_up
                for card in all_face_up
            )
            metadata[key] = "true" if playable else "false"

        return metadata
