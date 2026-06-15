# semantic-axis project view

Current period: 2026-W25
Current status: RED

## Current initiative — 2026-W25

### Phase 1: Scientific Artifact Loop

Promise: By the end of 2026-W25, Semantic Axis turns a measurement into a durable, inspectable scientific artifact: saved report block, permalink, fresh-browser reconstruction, fork lineage, full provenance, and Ben approval. The captured artifact must show the complete user experience, not just a backend response.

Progress: 0/10 tests passed (0% weighted).

Subtasks / artifact gates:
- [ ] measurement-run-baseline-captured — expected at least 1 matching receipt(s); observed 0
- [ ] saved-report-created-captured — expected at least 1 matching receipt(s); observed 0
- [ ] permalink-reconstruction-captured — expected at least 1 matching receipt(s); observed 0
- [ ] provenance-inspection-captured — expected at least 1 matching receipt(s); observed 0
- [ ] fork-lineage-ux-artifact-captured — expected at least 1 matching receipt(s); observed 0
- [ ] full-walkthrough-captured — expected at least 1 matching receipt(s); observed 0
- [ ] full-walkthrough-names-required-experience — expected every matching receipt field 'user_experience' to contain 'run measurement, save report, open permalink in a fresh browser, fork report'; matched 0, failures []
- [ ] provenance-visible-in-artifacts — expected every matching receipt field 'evidence' to contain 'provenance'; matched 0, failures []
- [ ] fork-lineage-shows-parent-id — expected every matching receipt field 'evidence' to contain 'parent_id'; matched 0, failures []
- [ ] ben-phase-1-signoff-recorded — expected at least 1 matching receipt(s); observed 0

## Upcoming weeks

- 2026-W26 — Analyst Instrument
  - By the end of 2026-W26, Semantic Axis supports the analyst loop from the spec: cluster chips for x/a/b, fast perturbation of cluster terms, sensitivity re-runs, sample-size honesty, and exportable evidence. The captured artifact must show a user varying terms and seeing whether a finding survives the perturbation.
  - Status: RED
- 2026-W27 — Comparative Space
  - By the end of 2026-W27, Semantic Axis supports multiple concepts in the same semantic space and distinguishes framing movement from attention movement. The captured artifact must show at least three concepts overlaid against the same axis, per-bucket document counts, and a first-pass interaction readout such as correlation or lead/lag.
  - Status: RED
- 2026-W28 — Prediction and Canary Scaffold
  - By the end of 2026-W28, Semantic Axis has a falsifiable prediction/canary scaffold: reports can produce prediction receipts, retrospective calibration can compare a semantic signal against a dated real-world event, and author/source metadata can identify candidate early movers without pretending that correlation is causation.
  - Status: RED

## How this view turns green

Append JSONL receipts whose fields match the checked subtasks, then rerun the project view generator.
Ben signoff is a separate receipt; it is not implied by the artifact existing.
