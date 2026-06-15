# Calendar Protocol

Calendar Receipts is not a todo app. It is a clock for promises.

## Horizons

- daily: execution queue
- weekly: cadence and campaign commitments
- monthly: campaign rollups and metric thresholds
- yearly: thesis-level scorecards

## RED / GREEN / REFACTOR

- RED: expected receipts are absent or insufficient.
- GREEN: receipts exist and satisfy the tests.
- REFACTOR: failed expectations are closed as misses, carried forward, rewritten, or killed with a reason.

## Receipt minimum

Every receipt must expose:

- `promise`
- `result`
- `evidence`
- `status`

A receipt without evidence is a claim wearing a hat.
