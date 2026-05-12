from solitaire.core.move_filter import MoveFilter
from solitaire.core.move_generator import MoveGenerator


class NplyStrategy:
    def __init__(self, depth: int):
        if depth < 1:
            raise ValueError("depth must be >= 1")
        self._depth = depth

    def select(self, game, visible_moves):
        best_move = visible_moves[0]
        best_score = float("-inf")
        for move in visible_moves:
            snap = game.snapshot()
            game.apply(move)
            score = self._score_after(game, self._depth - 1)
            game.restore(snap)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _score_after(self, game, depth):
        if game.is_won or depth == 0:
            return self._evaluate(game)
        future = MoveFilter(MoveGenerator(game).legal_moves()).visible()
        if not future:
            return self._evaluate(game)
        best = float("-inf")
        for move in future:
            snap = game.snapshot()
            game.apply(move)
            score = self._score_after(game, depth - 1)
            game.restore(snap)
            if score > best:
                best = score
        return best

    def _evaluate(self, game):
        face_up_count = sum(
            1 for col in game.tableau.columns for card in col if card.face_up
        )
        return game.foundations.total_cards + 0.1 * face_up_count
