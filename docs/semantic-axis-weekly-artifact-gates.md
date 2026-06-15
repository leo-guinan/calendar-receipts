# Semantic Axis Weekly Artifact Gates

Each phase is one calendar week. The tests are deliberately RED until a real user-experience artifact and Ben's signoff receipt exist.

The unit is not a feature checkbox. The unit is an artifact Ben can inspect: screen recording, public URL, JSON export, screenshot, or report file showing the experience described in the Semantic Axis spec.

## Receipt types

### `semax_ux_artifact_capture`

Required top-level fields for matching tests:

```json
{
  "id": "semax-phase-1-saved-report-2026-W25",
  "project": "semantic-axis",
  "type": "semax_ux_artifact_capture",
  "phase": "phase-1-scientific-artifact",
  "artifact": "saved_report_permalink_walkthrough",
  "period": "2026-W25",
  "date": "2026-06-19",
  "promise": "Capture the user experience for saved report permalinks.",
  "result": "Observed result, with misses stated plainly.",
  "user_experience": "run measurement, save report, open permalink in a fresh browser, fork report",
  "evidence": [
    "screen_recording: path-or-url",
    "permalink: https://...",
    "provenance: visible",
    "export: path-or-url"
  ]
}
```

### `ben_phase_signoff`

Required top-level fields:

```json
{
  "id": "ben-semax-phase-1-signoff-2026-W25",
  "project": "semantic-axis",
  "type": "ben_phase_signoff",
  "phase": "phase-1-scientific-artifact",
  "period": "2026-W25",
  "decision": "approved",
  "promise": "Ben reviews phase 1 artifact gate before the phase is considered done.",
  "result": "Approved / changes requested, with evidence pointer.",
  "evidence": ["message screenshot, email, issue comment, or meeting note"]
}
```

## Weekly phase gates

### 2026-W25 — Phase 1: Scientific Artifact Loop

Goal: turn a measurement into a durable scientific object.

Required UX artifacts:
- `saved_report_permalink_walkthrough`
- `fork_lineage_walkthrough`

Must show:
- run measurement
- save report
- open permalink in a fresh browser
- reconstruct same chart/data/provenance
- fork report
- child records parent id
- Ben approval receipt

### 2026-W26 — Phase 2: Analyst Instrument

Goal: make axis perturbation cheap enough that an analyst can learn from variation.

Required UX artifacts:
- `cluster_chip_editor_walkthrough`
- `sensitivity_check_walkthrough`

Must show:
- x/a/b terms as chips
- add/remove/toggle terms
- rerun quickly
- sensitivity output
- export evidence
- Ben approval receipt

### 2026-W27 — Phase 3: Comparative Space

Goal: compare multiple concepts in the same semantic space and separate framing from attention.

Required UX artifacts:
- `multi_concept_overlay_walkthrough`
- `attention_vs_framing_walkthrough`

Must show:
- three or more concepts overlaid on the same axis
- per-concept/per-bucket document counts
- interaction readout, e.g. correlation or lead/lag
- Ben approval receipt

### 2026-W28 — Phase 4: Prediction and Canary Scaffold

Goal: make the prediction/canary claims falsifiable instead of decorative.

Required UX artifacts:
- `prediction_log_walkthrough`
- `retrospective_calibration_walkthrough`
- `canary_candidate_walkthrough`

Must show:
- a report can generate a prediction receipt
- falsifier visible in the UX
- retrospective event/date comparison
- candidate early movers from author/source metadata
- explicit correlation-not-causation caveat
- Ben approval receipt

## Operating rule

Do not close a phase by deleting the failing expectation. Close it by appending the artifact receipts and Ben signoff receipt. If the phase misses, append a miss receipt or carry-forward expectation. Dashboard makeup is still makeup.
