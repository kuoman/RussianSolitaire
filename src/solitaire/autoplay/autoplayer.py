from solitaire.autoplay.strategies.first_move import FirstMoveStrategy
from solitaire.core.move_filter import MoveFilter
from solitaire.core.move_generator import MoveGenerator


class Autoplayer:
    def __init__(self, game, strategy=None, max_moves=10000):
        self._game = game
        self._strategy = strategy if strategy is not None else FirstMoveStrategy()
        self._max_moves = max_moves
        self._initial_total = game.total_moves

    def play(self) -> str:
        while not self._game.is_won:
            moves_played_this_session = self._game.total_moves - self._initial_total
            if moves_played_this_session >= self._max_moves:
                return "aborted"
            visible = MoveFilter(MoveGenerator(self._game).legal_moves()).visible()
            if not visible:
                return "false"
            move = self._strategy.select(self._game, visible)
            self._game.apply(move)
        return "true"
