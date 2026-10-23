# Tests and Validation Evidence

## Current automated structural check

From the repository root:

```bash
python3 src/validate_synthetic_dataset.py
```

This checks the generated CSV schemas, unique keys, foreign-key relationships, market/currency consistency, date validity, and quantity rules. It does not calculate service KPI results.

## Evidence to add during the build

- A short list of manually checked order IDs and their line/order classifications.
- n8n fixture outcomes and rejected-row reasons.
- PostgreSQL row-count and quality-check results.
- Reconciliation between SQL KPI outputs and the dashboard.
- Any regression test added for repeat loads/idempotency.

Keep these as reproducible checks, not only screenshots. Do not put credentials or real personal data in test output.
