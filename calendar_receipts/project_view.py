from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from calendar_receipts.evaluator import evaluate_expectation, load_expectations, load_receipts, repo_root, summarize


@dataclass(frozen=True)
class ProjectPeriod:
    period: str
    expectations: list[dict[str, Any]]
    results: list[Any]


def _parse_week(period: str) -> tuple[int, int]:
    year, week = period.split("-W", 1)
    return int(year), int(week)


def _format_week(year: int, week: int) -> str:
    return f"{year:04d}-W{week:02d}"


def add_weeks(period: str, offset: int) -> str:
    # Good enough for project views; handles normal ISO year rollover conservatively.
    # If we later schedule across year boundaries heavily, replace with datetime.fromisocalendar.
    year, week = _parse_week(period)
    week += offset
    while week > 53:
        year += 1
        week -= 53
    while week < 1:
        year -= 1
        week += 53
    return _format_week(year, week)


def _load_project_period(project: str, period: str, root: Path, receipts: list[dict[str, Any]]) -> ProjectPeriod:
    try:
        expectations = [
            expectation
            for expectation in load_expectations("weekly", period, root)
            if expectation.get("project") == project
        ]
    except FileNotFoundError:
        expectations = []

    results = []
    for expectation in expectations:
        results.extend(evaluate_expectation(expectation, receipts))
    return ProjectPeriod(period=period, expectations=expectations, results=results)


def _phase_title(expectation: dict[str, Any]) -> str:
    phase_name = expectation.get("phase_name") or expectation.get("id", "Unnamed initiative")
    phase = expectation.get("phase")
    if phase:
        return f"Phase {phase}: {phase_name}"
    return str(phase_name)


def _status_label(results: list[Any]) -> str:
    if not results:
        return "No tests"
    summary = summarize(results)
    if summary["failed"] == 0:
        return "GREEN"
    if summary["passed"] == 0:
        return "RED"
    return "PARTIAL"


def _render_expectation_detail(expectation: dict[str, Any], results: list[Any]) -> list[str]:
    lines = [f"### {_phase_title(expectation)}", ""]
    lines.append(f"Promise: {expectation.get('promise', '').strip()}")
    lines.append("")

    expectation_results = [r for r in results if r.expectation_id == expectation.get("id")]
    summary = summarize(expectation_results)
    lines.append(
        f"Progress: {summary['passed']}/{summary['total']} tests passed "
        f"({summary['weighted_pass_rate']:.0%} weighted)."
    )
    lines.append("")
    lines.append("Subtasks / artifact gates:")
    for result in expectation_results:
        marker = "x" if result.passed else " "
        lines.append(f"- [{marker}] {result.test_id} — {result.message}")
    lines.append("")
    return lines


def _render_upcoming(periods: list[ProjectPeriod]) -> list[str]:
    lines = ["## Upcoming weeks", ""]
    for project_period in periods:
        if not project_period.expectations:
            lines.append(f"- {project_period.period} — no expectation file for this project yet")
            continue
        for expectation in project_period.expectations:
            title = expectation.get("phase_name") or expectation.get("id")
            lines.append(f"- {project_period.period} — {title}")
            promise = str(expectation.get("promise", "")).strip()
            if promise:
                lines.append(f"  - {promise}")
            status = _status_label([r for r in project_period.results if r.expectation_id == expectation.get("id")])
            lines.append(f"  - Status: {status}")
    lines.append("")
    return lines


def build_project_view(project: str, current_period: str, root: Path | None = None, weeks_ahead: int = 4) -> str:
    root = root or repo_root()
    receipts = load_receipts(root)
    current = _load_project_period(project, current_period, root, receipts)
    upcoming = [
        _load_project_period(project, add_weeks(current_period, offset), root, receipts)
        for offset in range(1, weeks_ahead)
    ]

    lines: list[str] = [
        f"# {project} project view",
        "",
        f"Current period: {current_period}",
        f"Current status: {_status_label(current.results)}",
        "",
        f"## Current initiative — {current_period}",
        "",
    ]

    if not current.expectations:
        lines.append("No current expectation found for this project.")
        lines.append("")
    else:
        for expectation in current.expectations:
            lines.extend(_render_expectation_detail(expectation, current.results))

    lines.extend(_render_upcoming(upcoming))
    lines.extend(
        [
            "## How this view turns green",
            "",
            "Append JSONL receipts whose fields match the checked subtasks, then rerun the project view generator.",
            "Ben signoff is a separate receipt; it is not implied by the artifact existing.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
