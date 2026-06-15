from pathlib import Path

from calendar_receipts.project_view import build_project_view


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_project_view_shows_current_initiative_subtasks_and_upcoming_weeks(tmp_path):
    write(
        tmp_path / "expectations" / "weekly" / "2026-W25.yaml",
        """
expectations:
  - id: semax-phase-1
    horizon: weekly
    period: 2026-W25
    project: semantic-axis
    phase: "1"
    phase_name: Scientific Artifact Loop
    promise: Save reports and reconstruct them from permalinks.
    tests:
      - id: saved-report-artifact
        type: receipt_exists
        severity: critical
        weight: 5
        query:
          project: semantic-axis
          type: semax_ux_artifact_capture
          phase: phase-1
          period: 2026-W25
      - id: ben-signoff
        type: receipt_exists
        severity: critical
        weight: 8
        query:
          project: semantic-axis
          type: ben_phase_signoff
          phase: phase-1
          period: 2026-W25
""",
    )
    write(
        tmp_path / "expectations" / "weekly" / "2026-W26.yaml",
        """
expectations:
  - id: semax-phase-2
    horizon: weekly
    period: 2026-W26
    project: semantic-axis
    phase: "2"
    phase_name: Analyst Instrument
    promise: Add chip editor and sensitivity checks.
    tests:
      - id: chip-editor-artifact
        type: receipt_exists
        query:
          project: semantic-axis
          type: semax_ux_artifact_capture
          phase: phase-2
          period: 2026-W26
""",
    )

    markdown = build_project_view(
        project="semantic-axis",
        current_period="2026-W25",
        root=tmp_path,
        weeks_ahead=2,
    )

    assert "# semantic-axis project view" in markdown
    assert "## Current initiative — 2026-W25" in markdown
    assert "Scientific Artifact Loop" in markdown
    assert "Save reports and reconstruct them from permalinks." in markdown
    assert "- [ ] saved-report-artifact" in markdown
    assert "- [ ] ben-signoff" in markdown
    assert "## Upcoming weeks" in markdown
    assert "2026-W26 — Analyst Instrument" in markdown
    assert "Add chip editor and sensitivity checks." in markdown


def test_project_view_marks_completed_subtasks_from_receipts(tmp_path):
    write(
        tmp_path / "expectations" / "weekly" / "2026-W25.yaml",
        """
expectations:
  - id: semax-phase-1
    horizon: weekly
    period: 2026-W25
    project: semantic-axis
    phase_name: Scientific Artifact Loop
    promise: Save reports and reconstruct them from permalinks.
    tests:
      - id: saved-report-artifact
        type: receipt_exists
        query:
          project: semantic-axis
          type: semax_ux_artifact_capture
          artifact: saved_report_permalink_walkthrough
          period: 2026-W25
      - id: ben-signoff
        type: receipt_exists
        query:
          project: semantic-axis
          type: ben_phase_signoff
          period: 2026-W25
""",
    )
    write(
        tmp_path / "receipts" / "weekly" / "2026-W25.jsonl",
        '{"id":"r1","project":"semantic-axis","type":"semax_ux_artifact_capture","artifact":"saved_report_permalink_walkthrough","period":"2026-W25","promise":"capture","result":"captured","status":"closed_hit","evidence":["url"]}\n',
    )

    markdown = build_project_view(
        project="semantic-axis",
        current_period="2026-W25",
        root=tmp_path,
        weeks_ahead=1,
    )

    assert "- [x] saved-report-artifact" in markdown
    assert "- [ ] ben-signoff" in markdown
    assert "Progress: 1/2 tests passed" in markdown
