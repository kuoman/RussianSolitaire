class Strategy:
    """Base interface for autoplay strategies. Duck-typed; inheritance optional."""

    def select(self, game, visible_moves):
        raise NotImplementedError
