# Project Build Guide: What Was Implemented

This guide records the actual workflow completed for the order-fulfillment analytics project. Use it as a concise orientation; use the detailed [`project explainer`](project-explainer.md) to understand the model, KPIs, and how to write findings and recommendations.

## Completed workflow

```text
Synthetic data generation
→ Structural validation
→ PostgreSQL database/schema and manual CSV loading
→ SQL quality checks, KPIs, and segment diagnostics
→ Manual KPI verification
→ Power BI data model, measures, and report pages
→ Project documentation and findings write-up
```

## Implementation record

- **Data:** Generated five synthetic CSV tables and ran the structural validator.
- **Database:** Installed PostgreSQL 18, created `supply_chain_portfolio`, created the `supply_chain` tables, and imported customers, products, carriers, orders, and order lines.
- **SQL:** Executed all five project SQL files: DDL, quality checks, fulfillment KPIs, segment diagnostics, and dashboard view creation. The view `supply_chain.order_service` contains one row per order.
- **Manual KPI check:** Verified the date and quantity logic for delivered order `ORD-000001`; verified that cancelled order `ORD-000036` contributes to cancellation/submitted-order measures but not delivery-service rates.
- **Power BI:** Connected to PostgreSQL; imported the order-level view, order lines, and the customer, product, and carrier tables; built the relationship model; created seven named KPI measures; and built the Fulfillment Overview, Diagnostic Segments, and Data & Methodology pages.
- **AI assistance:** Used for schema understanding, SQL review, KPI validation, PostgreSQL troubleshooting, dashboard design review, and documentation support.

These implementation details are based on the project author's completion report. Repository evidence for manual KPI checks is in [`tests/manual-kpi-validation.md`](../tests/manual-kpi-validation.md).

## Not implemented

n8n and any other automated ingestion or scheduling are outside this project. The actual pipeline uses manual CSV imports into PostgreSQL. The existing n8n draft is not part of the completed deliverable and should not be described as implemented.

## Final items to publish

The actual Power BI report is built, but a `.pbix` file or page screenshots are not present in this repository yet. Add one safe-to-share `.pbix` or sanitized screenshots of the three completed report pages. Then add the actual findings/recommendations from those pages, including the period, comparison, numerator, denominator, and sample volume. Do not invent results or present synthetic patterns as evidence about a real business.
