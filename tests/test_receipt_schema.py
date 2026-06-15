from calendar_receipts.evaluator import load_receipts


def test_all_committed_receipts_have_promise_result_status_and_evidence():
    for receipt in load_receipts():
        assert receipt.get("promise"), f"{receipt.get('id')} missing promise"
        assert "result" in receipt, f"{receipt.get('id')} missing result"
        assert receipt.get("status") in {"open", "closed_hit", "closed_partial", "closed_miss", "blocked", "cancelled"}
        assert isinstance(receipt.get("evidence", []), list), f"{receipt.get('id')} evidence must be a list"
