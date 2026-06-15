# Semantic Axis Phase 1 receipt breakdown

Period: 2026-W25
Phase: Scientific Artifact Loop
Goal: turn one Semantic Axis measurement into a durable, inspectable, forkable scientific artifact.

These are the individual receipts needed before Ben can sign off. Each artifact receipt should capture the actual user experience, not just API output. A screenshot is acceptable for static states; a short screen recording is better when the receipt depends on a sequence.

## Receipt 1 — Measurement run baseline

Receipt id:
  semax-phase-1-measurement-run-baseline-2026-W25

Type:
  semax_ux_artifact_capture

Artifact:
  measurement_run_baseline

Purpose:
  Prove the user can run the target measurement and see a chart/table result before saving.

User experience to capture:
  run measurement and inspect result

Required evidence:
  - public app URL
  - screenshot or recording of measurement form filled with the AI optimism vs doom inputs
  - screenshot of result chart/table
  - visible document/sample count or bucket count

Acceptance phrase for evidence:
  result chart

## Receipt 2 — Saved report creation

Receipt id:
  semax-phase-1-saved-report-created-2026-W25

Type:
  semax_ux_artifact_capture

Artifact:
  saved_report_creation

Purpose:
  Prove the run can become a durable report artifact instead of disappearing when the page reloads.

User experience to capture:
  run measurement, save report

Required evidence:
  - screenshot/recording of Save Report action
  - report id visible
  - saved report metadata visible
  - persisted measurement definition visible

Acceptance phrase for evidence:
  saved report

## Receipt 3 — Permalink reconstruction

Receipt id:
  semax-phase-1-permalink-reconstruction-2026-W25

Type:
  semax_ux_artifact_capture

Artifact:
  permalink_reconstruction

Purpose:
  Prove the report URL reconstructs the same artifact in a fresh browser/session.

User experience to capture:
  open permalink in a fresh browser

Required evidence:
  - permalink URL
  - screenshot/recording from fresh browser/session
  - same measurement definition visible
  - same chart/result visible

Acceptance phrase for evidence:
  permalink

## Receipt 4 — Provenance inspection

Receipt id:
  semax-phase-1-provenance-inspection-2026-W25

Type:
  semax_ux_artifact_capture

Artifact:
  provenance_inspection

Purpose:
  Prove the report exposes enough provenance for a skeptical analyst to know what was measured.

User experience to capture:
  inspect report provenance

Required evidence:
  - visible datasource
  - visible date range
  - visible embedding/model or analysis method
  - visible code/build/version if available
  - visible request/measurement definition

Acceptance phrase for evidence:
  provenance

## Receipt 5 — Fork lineage

Receipt id:
  semax-phase-1-fork-lineage-2026-W25

Type:
  semax_ux_artifact_capture

Artifact:
  fork_lineage_walkthrough

Purpose:
  Prove analysts can fork a report, alter terms, and preserve parent-child lineage.

User experience to capture:
  fork report and inspect parent lineage

Required evidence:
  - parent report URL/id
  - fork action visible
  - child report URL/id
  - parent_id or lineage visible on child
  - one edited term or configuration field visible

Acceptance phrase for evidence:
  parent_id

## Receipt 6 — Full phase walkthrough

Receipt id:
  semax-phase-1-full-walkthrough-2026-W25

Type:
  semax_ux_artifact_capture

Artifact:
  saved_report_permalink_walkthrough

Purpose:
  Provide the single end-to-end artifact Ben can review without reconstructing the whole story from fragments.

User experience to capture:
  run measurement, save report, open permalink in a fresh browser, fork report

Required evidence:
  - screen recording of the full path
  - report permalink
  - forked report permalink
  - provenance visible
  - result chart visible

Acceptance phrase for evidence:
  provenance

## Receipt 7 — Ben signoff

Receipt id:
  ben-semax-phase-1-signoff-2026-W25

Type:
  ben_phase_signoff

Purpose:
  Close the phase only after Ben reviews the artifact experience.

Required fields:
  - decision: approved
  - reviewer: Ben
  - reviewed_artifacts: links or ids for receipts 1-6
  - result: explicit approval or requested changes

If Ben requests changes, record decision as changes_requested. Do not mark the phase green. Yes, this is annoying. That is the point.

## Minimal JSONL receipt skeletons

Append completed receipts to:
  receipts/daily/2026-06-15.jsonl

Use the template file:
  templates/semantic-axis-phase-1-receipts.jsonl
