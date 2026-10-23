# Tests and Validation Evidence

## Current automated structural check

From the repository root:

```bash
python3 src/validate_synthetic_dataset.py
```

This checks the generated CSV schemas, unique keys, foreign-key relationships, market/currency consistency, date validity, and quantity rules. It does not calculate service KPI results.

## Core evidence to add during the build

- A short list of manually checked order IDs and their line/order classifications.
- PostgreSQL row-count and quality-check results.
- Reconciliation between SQL KPI outputs and the dashboard.
- Any regression test added for repeat loads or idempotency.

Optional only: if you implement the n8n extension, record fixture outcomes and rejected-row reasons here. Do not describe n8n tests as completed unless you executed them against your configured workflow and database.

Keep evidence reproducible, not only screenshots. Do not put credentials or real personal data in test output.
