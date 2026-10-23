# Validation Fixtures — Not Analytical Data

These small CSVs are deliberately invalid inputs produced by `src/generate_synthetic_dataset.py` to exercise ingestion controls. They contain a duplicate key, blank ID, malformed date, unsupported market/currency, orphan order, negative quantity, and non-numeric quantity.

Run them through the n8n validation/reject path only. Do not load them into the clean `supply_chain` tables, include them in KPI queries, or combine them with `data/synthetic/`.

Regenerate them with:

```bash
python3 src/generate_synthetic_dataset.py
```
