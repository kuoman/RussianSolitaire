import random


class RandomStrategy:
    def select(self, game, visible_moves):
        return random.choice(visible_moves)
