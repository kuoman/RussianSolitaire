from solitaire.repl.command_parser import CommandParser


class Repl:
    PROMPT = "> "
    HELP_TEXT = (
        "Commands:\n"
        "  <card> <source> moved to <dest>   e.g. 7h c2 moved to c5\n"
        "  q | quit                            quit\n"
        "  ? | h | help                        this help\n"
        "Suits: s=♠ h=♥ d=♦ c=♣\n"
        "Destinations: c1..c7 or f (foundation)"
    )

    def __init__(self, game, display, input_fn=input, output_fn=print):
        self._game = game
        self._display = display
        self._input = input_fn
        self._output = output_fn
        self._parser = CommandParser(game)

    def run(self) -> None:
        while True:
            self._output(self._display.render())
            if self._game.is_won:
                self._output("You won! Congratulations.")
                return
            try:
                line = self._input(self.PROMPT)
            except (EOFError, KeyboardInterrupt):
                self._output("")
                return
            result = self._parser.parse(line)
            kind = result[0]
            if kind == "quit":
                return
            elif kind == "help":
                self._output(self.HELP_TEXT)
            elif kind == "noop":
                continue
            elif kind == "error":
                self._output(f"Error: {result[1]}")
            elif kind == "move":
                move = result[1]
                if self._game.can_apply(move):
                    self._game.apply(move)
                else:
                    self._output("Illegal move.")
