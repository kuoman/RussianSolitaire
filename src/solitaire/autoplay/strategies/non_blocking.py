from solitaire.core.move_filter import MoveFilter
from solitaire.core.move_generator import MoveGenerator


class NonBlockingStrategy:
    FOUNDATION_BONUS = 1.5

    def select(self, game, visible_moves):
        best_move = visible_moves[0]
        best_score = float("-inf")
        for move in visible_moves:
            snap = game.snapshot()
            game.apply(move)
            future = MoveFilter(MoveGenerator(game).legal_moves()).visible()
            score = len(future)
            if move.destination.is_foundation():
                score += self.FOUNDATION_BONUS
            game.restore(snap)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
