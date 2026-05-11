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
