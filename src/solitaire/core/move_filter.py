class MoveFilter:
    def __init__(self, moves):
        self._moves = moves

    def visible(self) -> list:
        foundation_sources = set()
        for move in self._moves:
            if move.destination.is_foundation():
                foundation_sources.add((move.source_column, move.count))
        result = []
        for move in self._moves:
            if move.destination.is_foundation():
                result.append(move)
            else:
                if (move.source_column, move.count) not in foundation_sources:
                    result.append(move)
        return result
