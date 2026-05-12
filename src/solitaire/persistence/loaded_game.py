class LoadedGame:
    def __init__(self, tableau, prior_moves=None, prior_metadata=None):
        self._tableau = tableau
        self._prior_moves = list(prior_moves) if prior_moves else []
        self._prior_metadata = dict(prior_metadata) if prior_metadata else {}

    @property
    def tableau(self):
        return self._tableau

    @property
    def prior_moves(self):
        return list(self._prior_moves)

    @property
    def prior_metadata(self):
        return dict(self._prior_metadata)
