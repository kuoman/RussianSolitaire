class BatchRunner:
    def __init__(self, runs, run_one):
        self._runs = runs
        self._run_one = run_one

    def run(self):
        outcomes = []
        for _ in range(self._runs):
            outcomes.append(self._run_one())

        won = sum(1 for o in outcomes if o["outcome"] == "true")
        lost = sum(1 for o in outcomes if o["outcome"] == "false")
        aborted = sum(1 for o in outcomes if o["outcome"] == "aborted")
        total_moves = sum(o["moves"] for o in outcomes)
        total_fc = sum(o["foundation_cards"] for o in outcomes)
        avg_moves = total_moves / self._runs if self._runs else 0
        avg_fc = total_fc / self._runs if self._runs else 0
        return {
            "runs": self._runs,
            "won": won,
            "lost": lost,
            "aborted": aborted,
            "avg_moves": avg_moves,
            "avg_foundation_cards": avg_fc,
        }
