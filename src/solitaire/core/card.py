RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]


class Card:
    def __init__(self, suit: str, rank: str, face_up: bool = False):
        self._suit = suit
        self._rank = rank
        self._face_up = face_up

    @property
    def suit(self) -> str:
        return self._suit

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def face_up(self) -> bool:
        return self._face_up

    def render(self, debug: bool = False) -> str:
        if self._face_up:
            return f"{self._rank}{self._suit}"
        if debug:
            return f"*{self._rank}{self._suit}"
        return "░░"

    def to_save_token(self) -> str:
        prefix = "" if self._face_up else "*"
        return f"{prefix}{self._rank}{self._suit}"

    @classmethod
    def from_save_token(cls, token: str) -> "Card":
        face_up = not token.startswith("*")
        raw = token.lstrip("*")
        suit = raw[-1]
        rank = raw[:-1]
        return cls(suit, rank, face_up=face_up)
