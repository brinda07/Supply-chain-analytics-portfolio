# Validation Fixtures — Not Analytical Data

These small CSVs are deliberately invalid inputs produced by `src/generate_synthetic_dataset.py` to exercise ingestion controls. They contain duplicate keys, blank IDs, malformed dates, unsupported markets or currencies, orphan orders, negative quantities, and non-numeric quantities.

They are optional test inputs. You may use them if you later build an n8n workflow or another ingestion-validation step, but testing them through n8n is not required to complete the core project. Never load them into the clean `supply_chain` tables, include them in KPI queries, or combine them with `data/synthetic/`.

Regenerate them with:

```bash
python3 src/generate_synthetic_dataset.py
```
