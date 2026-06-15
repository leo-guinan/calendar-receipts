#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from calendar_receipts.evaluator import evaluate_expectation, load_expectations, load_receipts, summarize


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate calendar expectations against receipts")
    parser.add_argument("--horizon", required=True, choices=["daily", "weekly", "monthly", "yearly"])
    parser.add_argument("--period", required=True)
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    expectations = load_expectations(args.horizon, args.period, ROOT)
    receipts = load_receipts(ROOT)
    results = []
    for expectation in expectations:
        results.extend(evaluate_expectation(expectation, receipts))
    summary = summarize(results)

    payload = {
        "id": f"{args.horizon}-test-run-{args.period}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "type": "calendar_test_run",
        "horizon": args.horizon,
        "period": args.period,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "promise": f"Run {args.horizon} expectation tests against receipts for {args.period}.",
        "result": f"{summary['passed']}/{summary['total']} tests passed; weighted pass rate {summary['weighted_pass_rate']:.1%}.",
        "status": "closed_hit" if summary["failed"] == 0 else "closed_partial",
        "summary": summary,
        "failures": [r.__dict__ for r in results if not r.passed],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))

    if args.write_result:
        out_dir = ROOT / "test-results" / args.horizon
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{args.period}.red.json"
        out_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {out_path}")

    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
