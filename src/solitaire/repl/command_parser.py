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
        return ("error", f"unrecognized command: {stripped!r}")
