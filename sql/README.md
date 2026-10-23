# SQL Layer — Synthetic Dataset

Run these files from the repository root after generating the CSVs:

1. `01_create_tables.sql` — creates the `supply_chain` schema, dimension/fact tables, and load audit table.
2. Load CSVs in dependency order: customers, products, carriers, orders, order lines.
3. `02_quality_checks.sql` — structural and reconciliation checks.
4. `05_dashboard_views.sql` — creates one row per order with line-aggregated flags for dashboard use.
5. `03_fulfillment_kpis.sql` — order-level service rates, unit fill rate, and cancellations.
6. `04_segment_diagnostics.sql` — illustrative synthetic comparisons by carrier, SKU, and segment.

The queries are reproducible practice material. Outputs describe only generator-produced records and are not empirical or causal supply-chain findings. Read `docs/metric-definitions.md` before interpreting them. Keep currencies separate and do not infer inventory causes from this dataset.
