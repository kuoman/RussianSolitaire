from solitaire.core.card import RANKS


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

        # 5. destination-specific validation
        if self._destination.is_column():
            dest_idx = self._destination.column_index()
            # cannot move to the same column
            if dest_idx == self._source_column:
                return False
            # destination index must exist
            if dest_idx < 0 or dest_idx >= len(columns):
                return False
            dest_col = columns[dest_idx]
            # empty column: only kings allowed
            if not dest_col:
                return source_card.rank == "K"
            # non-empty: same suit, one rank lower than dest top
            dest_top = dest_col[-1]
            if not dest_top.face_up:
                return False
            if source_card.suit != dest_top.suit:
                return False
            source_rank_idx = RANKS.index(source_card.rank)
            dest_rank_idx = RANKS.index(dest_top.rank)
            return dest_rank_idx == source_rank_idx + 1

        # foundation destination
        if self._destination.is_foundation():
            if self._count != 1:
                return False
            # source card must be the deepest card (last in column)
            if source_card is not source_col[-1]:
                return False
            return foundations.can_accept(source_card)

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
