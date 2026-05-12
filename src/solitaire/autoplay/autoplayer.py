from solitaire.core.move_filter import MoveFilter
from solitaire.core.move_generator import MoveGenerator


class Autoplayer:
    def __init__(self, game, max_moves=10000):
        self._game = game
        self._max_moves = max_moves
        self._initial_total = game.total_moves

    def play(self) -> str:
        while not self._game.is_won:
            moves_played_this_session = self._game.total_moves - self._initial_total
            if moves_played_this_session >= self._max_moves:
                return "aborted"
            moves = MoveFilter(MoveGenerator(self._game).legal_moves()).visible()
            if not moves:
                return "false"
            self._game.apply(moves[0])
        return "true"
