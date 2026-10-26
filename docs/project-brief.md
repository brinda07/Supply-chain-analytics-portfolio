# Project Brief — Completed Implementation

## Project at a glance

- **Title:** AI-Assisted Order Fulfillment Analytics on a Synthetic Retail Dataset
- **Type:** Supply chain analyst portfolio project using deterministic, fully synthetic records.
- **Business scenario:** A fictional specialty-food wholesaler serving customers in the US and India wants visibility into order fulfillment reliability.
- **Analysis question:** How can an analyst measure on-time and complete delivery, identify differences across the generated sample, and verify the calculations before communicating them?
- **Core tools used:** Python, PostgreSQL 18, SQL, Power BI, and AI assistance.
- **Automation status:** n8n and other workflow automation were not implemented. CSVs were loaded manually.

## Implemented workflow

1. Generated five reproducible synthetic CSV files and a dataset manifest.
2. Ran structural validation on the generated dataset.
3. Installed PostgreSQL, created the `supply_chain_portfolio` database, and created the `supply_chain` schema and tables.
4. Imported `customers.csv`, `products.csv`, `carriers.csv`, `orders.csv`, and `order_lines.csv`.
5. Executed `01_create_tables.sql`, `02_quality_checks.sql`, `03_fulfillment_kpis.sql`, `04_segment_diagnostics.sql`, and `05_dashboard_views.sql`.
6. Created `supply_chain.order_service`, a one-row-per-order view, and manually checked `ORD-000001` and `ORD-000036` against the service and cancellation rules.
7. Connected Power BI to PostgreSQL, imported `order_service`, `order_lines`, `customers`, `products`, and `carriers`, built the relationship model and seven KPI measures, and created three pages: Fulfillment Overview, Diagnostic Segments, and Data & Methodology.
8. Used AI assistance for schema understanding, SQL review, KPI validation, PostgreSQL troubleshooting, dashboard design review, and documentation support.

The detailed explanation of how these stages fit together, how to interpret each measure, and how to write findings is in [`project-explainer.md`](project-explainer.md).

## Measures implemented

The Power BI report includes Submitted Orders, Delivered Orders, On-Time Rate, In-Full Order Rate, OTIF Rate, Cancellation Rate, and Unit Fill Rate. Their grains and denominator rules are defined in [`metric-definitions.md`](metric-definitions.md). Service rates exclude cancelled orders; cancellation rate uses all submitted orders; unit fill compares delivered units with ordered units on delivered orders.

## What this project demonstrates

- Reproducible synthetic-data generation and structural validation.
- Relational modeling, primary/foreign keys, and PostgreSQL table creation/import.
- SQL data checks, KPI calculation, diagnostic segmentation, and a dashboard-ready order-level view.
- Manual validation of order-level KPI logic against source records.
- Power BI data modeling, DAX measure concepts, and multi-page reporting.
- Responsible use of AI as an assistant, with human review of analysis claims.

## Interpretation and boundaries

Every record is fictional. The generator intentionally programs variations in delivery and partial fulfillment so that the analyst can practice reporting and validation. Any difference seen by market, carrier, customer segment, or product is a property of this generated sample—not evidence of actual carrier/customer performance, a causal explanation, or an industry benchmark.

The data does not contain inventory on hand, stock movements, purchase orders, suppliers, actual carrier scans, contractual service targets, actual costs, or intervention outcomes. Do not claim inventory optimization, root causes, savings, or real-world service improvement.

The `load_audit` table was created as part of the schema. Since no automation was implemented, do not claim that an automated process wrote or monitored load batches unless you have separate evidence that you populated it.

## Remaining repository publication work

The implementation is complete according to the author’s report, but the GitHub repository does not currently contain the Power BI `.pbix` file or report screenshots. Add the `.pbix` if it can be shared safely, or add sanitized images of the three pages under `dashboard/screenshots/`. Then write the actual findings and recommendations using the report's values, order counts, denominators, filters, and periods. Do not insert invented values; use the fill-in format in [`project-explainer.md`](project-explainer.md).
