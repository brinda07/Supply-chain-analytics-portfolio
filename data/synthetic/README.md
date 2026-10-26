# Synthetic Dataset Files

**All records in this folder are generated, fictional, and deterministic.** They do not represent actual companies, customers, carriers, orders, prices, or delivery performance. This dataset is for demonstrating data preparation, workflow automation, SQL, validation, and dashboards. Do not present calculated patterns as real-world evidence.

Regenerate from the repository root:

```bash
python3 src/generate_synthetic_dataset.py
```

The generator uses Python’s standard library and seed `20261023`.

| File | Grain | Rows |
|---|---|---:|
| `orders.csv` | One row per order | 1,440 |
| `order_lines.csv` | One row per order-product line | 3,601 |
| `customers.csv` | One row per fictional customer | 80 |
| `products.csv` | One row per fictional SKU | 24 |
| `carriers.csv` | One row per fictional carrier | 6 |
| `dataset_manifest.json` | Generation metadata | — |

Date coverage is January 2025 through June 2026. The synthetic schema includes order, promise, and delivery dates plus ordered/delivered quantities for practicing fulfillment calculations. It does not include inventory balances, replenishment, suppliers, or real carrier events. USD and INR values are local synthetic prices and must not be aggregated as one currency.

Use only the files in this folder for analytical table loads and KPI calculations. See `docs/synthetic-data-card.md` for the generation approach and disclosure language.
