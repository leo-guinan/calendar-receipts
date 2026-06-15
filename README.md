# Calendar Receipts

A calendar-shaped receipt system for running RED -> GREEN -> REFACTOR against daily, weekly, monthly, and yearly commitments.

The repo treats expectations as tests. A period starts red because the promised receipts do not exist yet. As work happens, receipts are appended. At close, the test score is the operating receipt: what passed, what missed, and what must be refactored.

Core loop:

```text
expectation -> test -> receipt -> score -> refactor
```

## First baseline

The first committed expectation is `expectations/weekly/2026-W25.yaml` for the Time War publishing baseline.

It is intentionally red on day one. That is the point. The failure is not a broken scaffold; it is an honest absence of receipts.

Run:

```bash
python3 -m pytest -q
```

Or evaluate one period without pytest:

```bash
python3 scripts/run_period_tests.py --horizon weekly --period 2026-W25
```

## Structure

```text
expectations/     Promise files that compile into tests
receipts/         Append-only observed results, JSONL
scripts/          Period test runner and report utilities
calendar_receipts/ Evaluation library
tests/            Pytest suite over expectations and receipts
test-results/     Captured RED/GREEN/CLOSE outputs
schemas/          JSON schemas for expectation and receipt records
```

## Project stakeholder views

Generate a shareable view for any project with receipt expectations:

```bash
python3 scripts/generate_project_view.py --project semantic-axis --current-period 2026-W25 --weeks-ahead 4
```

Default output:

```text
views/projects/<project>.md
```

The view shows the current initiative, artifact subtasks for the week, RED/GREEN state from receipts, and upcoming weekly phases. It is meant to be sent to stakeholders without asking them to inspect YAML. A small mercy in a universe otherwise committed to YAML.

## Operating rule

Never silently delete a failing expectation. End-of-period failures must become one of:

- a miss receipt
- a carry-forward expectation
- a refactored expectation with reason
- a killed expectation with reason

The dashboard can be wrong. The receipts should at least be inspectable.
