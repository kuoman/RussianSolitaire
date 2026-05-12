from solitaire.core.move import Move, ColumnDestination, FoundationDestination


class MoveGenerator:
    @staticmethod
    def legal_moves(game) -> list:
        result = []
        tableau = game.tableau
        foundations = game.foundations
        n_cols = len(tableau.columns)

        for src_idx in range(n_cols):
            col = tableau.columns[src_idx]
            for count in range(1, len(col) + 1):
                source_card = col[len(col) - count]
                if not source_card.face_up:
                    break

                for dest_idx in range(n_cols):
                    move = Move(src_idx, count, ColumnDestination(dest_idx))
                    if move.is_legal_on(tableau, foundations):
                        result.append(move)

                if count == 1:
                    move = Move(src_idx, count, FoundationDestination())
                    if move.is_legal_on(tableau, foundations):
                        result.append(move)

        return result
