class Move:
    def __init__(self, source_column: int, count: int, destination):
        self._source_column = source_column
        self._count = count
        self._destination = destination

    @property
    def source_column(self) -> int:
        return self._source_column

    @property
    def count(self) -> int:
        return self._count

    @property
    def destination(self):
        return self._destination


class ColumnDestination:
    def __init__(self, column_index: int):
        self._column_index = column_index

    def is_column(self) -> bool:
        return True

    def is_foundation(self) -> bool:
        return False

    def column_index(self) -> int:
        return self._column_index

    def __eq__(self, other):
        return isinstance(other, ColumnDestination) and other._column_index == self._column_index

    def __repr__(self):
        return f"ColumnDestination({self._column_index})"


class FoundationDestination:
    def is_column(self) -> bool:
        return False

    def is_foundation(self) -> bool:
        return True

    def __eq__(self, other):
        return isinstance(other, FoundationDestination)

    def __repr__(self):
        return "FoundationDestination()"
