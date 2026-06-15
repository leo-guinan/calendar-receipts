import pytest

from calendar_receipts.evaluator import evaluate_expectation, load_expectations, load_receipts, repo_root

HORIZON = "weekly"


def _weekly_periods() -> list[str]:
    expectation_dir = repo_root() / "expectations" / HORIZON
    return sorted(path.stem for path in expectation_dir.glob("*.yaml"))


def _cases():
    receipts = load_receipts()
    for period in _weekly_periods():
        for expectation in load_expectations(HORIZON, period):
            for result in evaluate_expectation(expectation, receipts):
                yield period, result


@pytest.mark.parametrize(
    "period,result",
    list(_cases()),
    ids=lambda case: case if isinstance(case, str) else f"{case.expectation_id}::{case.test_id}",
)
def test_weekly_expectation_is_green(period, result):
    assert result.passed, f"{period}: {result.message}"
