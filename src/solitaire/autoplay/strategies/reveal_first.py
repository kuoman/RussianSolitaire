from solitaire.core.move_generator import MoveGenerator
from solitaire.core.move_filter import MoveFilter


class RevealFirstStrategy:
    REVEAL_BONUS = 100
    FOUNDATION_BONUS = 1.5

    def select(self, game, visible_moves):
        best_move = visible_moves[0]
        best_score = float("-inf")
        for move in visible_moves:
            score = self._score(game, move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _score(self, game, move):
        score = 0.0
        if self._reveals_face_down(game, move):
            score += self.REVEAL_BONUS
        if move.destination.is_foundation():
            score += self.FOUNDATION_BONUS
        snap = game.snapshot()
        game.apply(move)
        future = MoveFilter(MoveGenerator(game).legal_moves()).visible()
        score += len(future)
        game.restore(snap)
        return score

    def _reveals_face_down(self, game, move):
        src_col = game.tableau.columns[move.source_column]
        if move.count >= len(src_col):
            return False
        new_bottom_card = src_col[len(src_col) - move.count - 1]
        return not new_bottom_card.face_up
