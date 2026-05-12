from solitaire.core.move_generator import MoveGenerator
from solitaire.repl.command_parser import CommandParser


class Repl:
    PROMPT = "> "
    HELP_TEXT = (
        "Commands:\n"
        "  <number>                            pick from list of legal moves\n"
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
        self._current_moves = []

    def run(self) -> None:
        while True:
            self._output(self._display.render())
            if self._game.is_won:
                self._output("You won! Congratulations.")
                return

            self._current_moves = MoveGenerator.legal_moves(self._game)
            self._output(self._format_move_list(self._current_moves))

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
            elif kind == "pick":
                n = result[1]
                if 1 <= n <= len(self._current_moves):
                    self._game.apply(self._current_moves[n - 1])
                else:
                    self._output(
                        f"Pick out of range: {n}. Choose 1 to {len(self._current_moves)}."
                    )
            elif kind == "move":
                move = result[1]
                if self._game.can_apply(move):
                    self._game.apply(move)
                else:
                    self._output("Illegal move.")

    def _format_move_list(self, moves) -> str:
        if not moves:
            return "No legal moves available."
        lines = ["Available moves:"]
        for i, move in enumerate(moves, start=1):
            lines.append(f"  {i}. {move.describe(self._game.tableau)}")
        return "\n".join(lines)
