from solitaire.core.foundations import Foundations


class Game:
    def __init__(self, tableau, foundations=None):
        self._tableau = tableau
        self._foundations = foundations if foundations is not None else Foundations()
        self._moves = []

    @property
    def tableau(self):
        return self._tableau

    @property
    def foundations(self):
        return self._foundations

    @property
    def moves(self) -> list:
        return self._moves

    @property
    def is_won(self) -> bool:
        return self._foundations.is_complete

    def can_apply(self, move) -> bool:
        return move.is_legal_on(self._tableau, self._foundations)
