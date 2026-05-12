from solitaire.core.card import RANKS
from solitaire.core.move import Move, ColumnDestination, FoundationDestination


SUIT_MAP = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}
UNICODE_SUITS = {"♠", "♥", "♦", "♣"}


class CommandParser:
    def __init__(self, game):
        self._game = game

    def parse(self, line: str):
        stripped = line.strip()
        if stripped == "":
            return ("noop",)
        lowered = stripped.lower()
        if lowered in ("q", "quit"):
            return ("quit",)
        if lowered in ("?", "help"):
            return ("help",)
        return self._parse_move(stripped)

    def _parse_move(self, line: str):
        # Expected shape: <card> <source> moved to <dest>
        # Find "moved to" (case-insensitive) as the connecting phrase.
        lowered = line.lower()
        marker = " moved to "
        idx = lowered.find(marker)
        if idx == -1:
            return ("error", "expected 'moved to' phrase")
        prefix = line[:idx].strip()
        suffix = line[idx + len(marker):].strip()

        prefix_tokens = prefix.split()
        if len(prefix_tokens) != 2:
            return ("error", "expected '<card> <source> moved to <dest>'")
        card_token, source_token = prefix_tokens

        try:
            rank, suit = self._parse_card_token(card_token)
        except ValueError as e:
            return ("error", str(e))

        try:
            source_index = self._parse_column_token(source_token)
        except ValueError as e:
            return ("error", str(e))

        try:
            destination = self._parse_destination(suffix)
        except ValueError as e:
            return ("error", str(e))

        # Locate the named card in the source column. It must be face-up.
        columns = self._game.tableau.columns
        if source_index < 0 or source_index >= len(columns):
            return ("error", f"source column out of range: c{source_index + 1}")
        source_col = columns[source_index]
        card_index = self._find_card_index(source_col, rank, suit)
        if card_index is None:
            return ("error", f"card {rank}{suit} not found face-up in c{source_index + 1}")

        count = len(source_col) - card_index
        return ("move", Move(source_index, count, destination))

    def _parse_card_token(self, token: str):
        if len(token) < 2:
            raise ValueError(f"bad card: {token!r}")
        suit = self._normalize_suit(token[-1])
        rank = token[:-1].upper()
        if rank not in RANKS:
            raise ValueError(f"bad rank: {rank!r}")
        return rank, suit

    def _normalize_suit(self, s: str) -> str:
        s = s.strip()
        if s in UNICODE_SUITS:
            return s
        if s.lower() in SUIT_MAP:
            return SUIT_MAP[s.lower()]
        raise ValueError(f"unknown suit: {s!r}")

    def _parse_column_token(self, token: str) -> int:
        t = token.strip().lower()
        if not t.startswith("c") or len(t) < 2:
            raise ValueError(f"bad source column: {token!r}")
        try:
            n = int(t[1:])
        except ValueError:
            raise ValueError(f"bad source column: {token!r}")
        return n - 1

    def _parse_destination(self, token: str):
        t = token.strip().lower()
        if t == "f":
            return FoundationDestination()
        if t.startswith("c"):
            try:
                n = int(t[1:])
            except ValueError:
                raise ValueError(f"bad destination: {token!r}")
            return ColumnDestination(n - 1)
        raise ValueError(f"bad destination: {token!r}")

    def _find_card_index(self, column, rank, suit):
        for i, card in enumerate(column):
            if card.face_up and card.rank == rank and card.suit == suit:
                return i
        return None
