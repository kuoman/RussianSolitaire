class Display:
    def __init__(self, tableau, debug: bool = False):
        self._tableau = tableau
        self._debug = debug

    def render(self) -> str:
        lines = []
        lines.append("Foundations: ♠--  ♥--  ♦--  ♣--")
        lines.append("")
        lines.append(self._header_row())
        max_rows = max(len(col) for col in self._tableau.columns)
        for row in range(max_rows):
            lines.append(self._card_row(row))
        return "\n".join(lines)

    def _header_row(self) -> str:
        headers = [f" C{i+1} " for i in range(7)]
        return " ".join(headers)

    def _card_row(self, row: int) -> str:
        slots = []
        for col in self._tableau.columns:
            if row < len(col):
                card = col[row]
                text = card.render(debug=self._debug)
                slots.append(f"{text:<4}")
            else:
                slots.append("    ")
        return " ".join(slots)
