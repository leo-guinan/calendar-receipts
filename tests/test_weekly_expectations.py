import pytest

from calendar_receipts.evaluator import evaluate_expectation, load_expectations, load_receipts

PERIOD = "2026-W25"
HORIZON = "weekly"


def _cases():
    receipts = load_receipts()
    for expectation in load_expectations(HORIZON, PERIOD):
        for result in evaluate_expectation(expectation, receipts):
            yield result


@pytest.mark.parametrize("result", list(_cases()), ids=lambda r: f"{r.expectation_id}::{r.test_id}")
def test_weekly_expectation_is_green(result):
    assert result.passed, result.message
