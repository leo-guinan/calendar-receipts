from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import yaml


@dataclass(frozen=True)
class EvaluationResult:
    expectation_id: str
    test_id: str
    passed: bool
    message: str
    observed: Any = None
    expected: Any = None
    severity: str = "important"
    weight: int = 1


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_expectations(horizon: str, period: str, root: Path | None = None) -> list[dict[str, Any]]:
    root = root or repo_root()
    path = root / "expectations" / horizon / f"{period}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Expectation file not found: {path}")
    data = yaml.safe_load(path.read_text()) or {}
    if isinstance(data, dict) and "expectations" in data:
        return data["expectations"]
    if isinstance(data, list):
        return data
    return [data]


def load_receipts(root: Path | None = None) -> list[dict[str, Any]]:
    root = root or repo_root()
    receipts_root = root / "receipts"
    receipts: list[dict[str, Any]] = []
    if not receipts_root.exists():
        return receipts
    for path in sorted(receipts_root.rglob("*.jsonl")):
        for line_no, line in enumerate(path.read_text().splitlines(), start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL in {path}:{line_no}: {exc}") from exc
            record.setdefault("_source", str(path.relative_to(root)))
            receipts.append(record)
    return receipts


def matches_query(receipt: dict[str, Any], query: dict[str, Any]) -> bool:
    for key, expected in (query or {}).items():
        actual = receipt.get(key)
        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    return True


def field_value(record: dict[str, Any], dotted: str) -> Any:
    current: Any = record
    for part in dotted.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def evaluate_test(expectation: dict[str, Any], test: dict[str, Any], receipts: list[dict[str, Any]]) -> EvaluationResult:
    expectation_id = expectation["id"]
    test_id = test["id"]
    test_type = test["type"]
    severity = test.get("severity", expectation.get("severity", "important"))
    weight = int(test.get("weight", expectation.get("weight", 1)))
    query = test.get("query", {})
    matched = [r for r in receipts if matches_query(r, query)]

    if test_type == "receipt_exists":
        required = int(test.get("required_count", 1))
        observed = len(matched)
        return EvaluationResult(
            expectation_id, test_id, observed >= required,
            f"expected at least {required} matching receipt(s); observed {observed}",
            observed, required, severity, weight,
        )

    if test_type == "receipt_count":
        required = int(test["required_count"])
        observed = len(matched)
        return EvaluationResult(
            expectation_id, test_id, observed >= required,
            f"expected at least {required} matching receipt(s); observed {observed}",
            observed, required, severity, weight,
        )

    if test_type == "receipt_count_by_day":
        required = int(test["required_per_day"])
        days = test["days"]
        counts = {day: 0 for day in days}
        for receipt in matched:
            day = receipt.get("date") or str(receipt.get("created_at", ""))[:10]
            if day in counts:
                counts[day] += 1
        failing = {day: count for day, count in counts.items() if count < required}
        passed = not failing
        return EvaluationResult(
            expectation_id, test_id, passed,
            f"expected {required}/day; failing days: {failing or 'none'}",
            counts, {"required_per_day": required, "days": days}, severity, weight,
        )

    if test_type == "field_contains":
        field = test["field"]
        contains = test["contains"]
        failures = []
        for receipt in matched:
            value = field_value(receipt, field)
            haystack = "\n".join(map(str, value)) if isinstance(value, list) else str(value or "")
            if contains not in haystack:
                failures.append(receipt.get("id", "<unknown>"))
        passed = bool(matched) and not failures
        message = (
            f"expected every matching receipt field {field!r} to contain {contains!r}; "
            f"matched {len(matched)}, failures {failures}"
        )
        return EvaluationResult(expectation_id, test_id, passed, message, failures, contains, severity, weight)

    raise ValueError(f"Unknown test type: {test_type}")


def evaluate_expectation(expectation: dict[str, Any], receipts: list[dict[str, Any]]) -> list[EvaluationResult]:
    return [evaluate_test(expectation, test, receipts) for test in expectation.get("tests", [])]


def summarize(results: list[EvaluationResult]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    total_weight = sum(r.weight for r in results)
    passed_weight = sum(r.weight for r in results if r.passed)
    critical_failures = [r for r in results if not r.passed and r.severity == "critical"]
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "raw_pass_rate": (passed / total) if total else 1.0,
        "total_weight": total_weight,
        "passed_weight": passed_weight,
        "weighted_pass_rate": (passed_weight / total_weight) if total_weight else 1.0,
        "critical_failures": len(critical_failures),
    }
