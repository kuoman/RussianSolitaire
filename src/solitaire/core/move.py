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

    def is_legal_on(self, tableau, foundations) -> bool:
        # 1. count must be at least 1
        if self._count < 1:
            return False

        # 2. source column must exist
        columns = tableau.columns
        if self._source_column < 0 or self._source_column >= len(columns):
            return False

        source_col = columns[self._source_column]

        # 3. count cannot exceed column length
        if self._count > len(source_col):
            return False

        # 4. source card (topmost of moving stack) must be face-up
        source_card = source_col[len(source_col) - self._count]
        if not source_card.face_up:
            return False

        return False


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
