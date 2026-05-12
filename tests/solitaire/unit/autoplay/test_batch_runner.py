from solitaire.autoplay.batch_runner import BatchRunner


def test_batch_runner_tallies_outcomes():
    outcomes = iter([
        {"outcome": "true", "moves": 50, "foundation_cards": 52},
        {"outcome": "false", "moves": 10, "foundation_cards": 4},
        {"outcome": "aborted", "moves": 10000, "foundation_cards": 30},
    ])
    runner = BatchRunner(3, lambda: next(outcomes))
    result = runner.run()
    assert result["runs"] == 3
    assert result["won"] == 1
    assert result["lost"] == 1
    assert result["aborted"] == 1


def test_batch_runner_computes_averages():
    outcomes = iter([
        {"outcome": "false", "moves": 10, "foundation_cards": 2},
        {"outcome": "false", "moves": 20, "foundation_cards": 4},
    ])
    runner = BatchRunner(2, lambda: next(outcomes))
    result = runner.run()
    assert result["avg_moves"] == 15.0
    assert result["avg_foundation_cards"] == 3.0


def test_batch_runner_handles_zero_runs():
    runner = BatchRunner(0, lambda: {"outcome": "false", "moves": 0, "foundation_cards": 0})
    result = runner.run()
    assert result["runs"] == 0
    assert result["won"] == 0
    assert result["avg_moves"] == 0
