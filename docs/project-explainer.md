# Project Explainer: What This Fulfillment Analysis Does

> **Purpose:** Help you explain your completed project, understand how the components fit together, and turn your Power BI results into careful findings and recommendations.
>
> **Important:** The source records are fully synthetic. Use this as a technical demonstration of analyst methods—not evidence about a real retailer, market, customer, product, or carrier.

## 1. The project in one sentence

You built a repeatable analysis workflow that takes a generated order dataset, checks and loads it into PostgreSQL, calculates fulfillment KPIs in SQL, spot-checks the KPI rules against individual orders, and presents the resulting synthetic sample in Power BI.

## 2. The business question you modeled

The scenario is a fictional specialty-food wholesaler serving customers in the US and India. The example question is:

> **How can an operations analyst measure order-fulfillment reliability and identify which parts of a generated order sample deserve closer review?**

The project measures whether delivered orders arrived by their promised date and whether every line arrived in full. It also reports cancellations, unit fill, and differences across the generated market, customer, product, and carrier groups.

It does **not** establish that a real company has a service problem. The generator deliberately programs variation into some groups so you can practice identifying, validating, and communicating patterns.

## 3. Your completed end-to-end workflow

```text
Synthetic data generation
        ↓
Structural data validation
        ↓
PostgreSQL schema creation and manual CSV imports
        ↓
SQL quality checks, KPI analysis, and diagnostic queries
        ↓
Manual KPI verification on selected orders
        ↓
Power BI relationship model, measures, and report pages
        ↓
Project documentation and findings/recommendations write-up
```

The first six steps are implemented according to your completion report. The final written interpretation is the remaining analysis-writing step. The `.pbix` file and dashboard screenshots are not currently in the GitHub repository.

There is no n8n or other automated ingestion component. You imported the CSVs manually. The `load_audit` table exists in the schema, but its presence alone does not mean automated batch auditing was implemented or used.

## 4. What is in the data model

The generator produces five CSVs. In the current version, they contain 80 customers, 24 products, 6 carriers, 1,440 orders, and 3,601 order lines. These records are fictional and reproducible using the documented generator seed.

| Table | One row represents | How it is used |
|---|---|---|
| `customers` | One fictional customer | Adds customer market, city, and segment context to orders. |
| `products` | One fictional SKU | Adds product name and category context to order lines. |
| `carriers` | One fictional carrier | Adds carrier and market context to orders. |
| `orders` | One customer order | Stores order date, promised/actual delivery dates, status, market, customer, and carrier. |
| `order_lines` | One product line within an order | Stores the SKU, ordered and delivered units, and fictional unit price. |
| `load_audit` | One potential load batch | A support table in the schema; do not describe it as automated logging in this project. |
| `order_service` view | One order, after line-level values are aggregated | Supplies order-level flags and totals to Power BI without repeating each order across its lines. |

### Why the row grain matters

An order can contain several product lines. For example, one order with four lines is still **one order**, not four. If you join order headers directly to lines and count rows, you can overcount orders. If you sum an order-level measure after the join, you may count it once per line.

Your SQL view avoids this for order-level reporting by first aggregating `order_lines` to one summary row per `order_id`, then joining that summary to the order header. In Power BI, `order_service` is the one-row-per-order parent for `order_lines`; customer and carrier dimensions filter orders, and the product dimension filters lines.

A common relationship layout is:

- `customers[customer_id]` → `order_service[customer_id]` (one customer to many orders)
- `carriers[carrier_id]` → `order_service[carrier_id]` (one carrier to many orders)
- `order_service[order_id]` → `order_lines[order_id]` (one order to many lines)
- `products[sku_id]` → `order_lines[sku_id]` (one product to many lines)

Check that the Power BI relationship keys and directions match the model you actually created. Avoid linking two many-side tables in a way that duplicates counts.

## 5. What each technical stage proves

### A. Synthetic data generation

`src/generate_synthetic_dataset.py` creates the same fictional records from a fixed seed. This makes your analysis reproducible and shareable without redistributing the tutorial creator’s restricted dataset.

### B. Structural validation

`src/validate_synthetic_dataset.py` checks file structure and data rules such as required columns, unique keys, valid relationships, allowed markets/currencies, date logic, and quantity rules. It does **not** calculate whether the service KPIs are right. That is why you also did manual KPI verification.

### C. PostgreSQL

You created the `supply_chain_portfolio` database and `supply_chain` schema, then loaded customers, products, carriers, orders, and order lines. Load the parent/dimension records before the dependent order and line records because foreign keys require the referenced records to exist.

The executed scripts have distinct responsibilities:

1. `01_create_tables.sql` — creates the tables, keys, and constraints.
2. `02_quality_checks.sql` — runs data-quality and reconciliation queries.
3. `03_fulfillment_kpis.sql` — calculates service rates, unit fill, and cancellation measures.
4. `04_segment_diagnostics.sql` — compares generated service measures by carrier, product/SKU, and customer segment.
5. `05_dashboard_views.sql` — creates `supply_chain.order_service`, a one-row-per-order view for reporting.

### D. Manual KPI verification

You checked two source orders before trusting aggregate charts:

- `ORD-000001` is delivered, with actual date **2025-01-14** before the promised date **2025-01-15**. All four lines meet their ordered quantities (21 ordered, 21 delivered). Expected classification: on-time = Yes, in-full = Yes, OTIF = Yes.
- `ORD-000036` is cancelled and has a blank actual delivery date. It belongs in submitted-order and cancellation metrics, but not in on-time, in-full, or OTIF delivery-service denominators.

The reproducible evidence and SQL queries are in [`../tests/manual-kpi-validation.md`](../tests/manual-kpi-validation.md). These two spot checks validate examples; they are not a complete test of every edge case.

## 6. Understand the seven Power BI measures

Use the definitions in [`metric-definitions.md`](metric-definitions.md) as the source of truth. Always include the relevant period/filter and order counts alongside percentages.

| Measure | Meaning in this project | Denominator / grain |
|---|---|---|
| **Submitted Orders** | Distinct orders placed, including delivered and cancelled orders. | All orders in the current filter context; order grain. |
| **Delivered Orders** | Distinct orders with `order_status = 'delivered'`. | Count of delivered orders; order grain. |
| **On-Time Rate** | Delivered orders whose actual delivery date is on or before the promised date. | Delivered orders with assessable dates; order grain. |
| **In-Full Order Rate** | Delivered orders where every order line delivered at least its ordered quantity. | Delivered orders; first classify every line, then aggregate to order grain. |
| **OTIF Rate** | Delivered orders that are both on time and in full. | Delivered orders; calculate the joint condition directly at order grain. |
| **Cancellation Rate** | Cancelled orders divided by submitted orders. | All submitted orders; order grain. |
| **Unit Fill Rate** | Delivered units divided by ordered units on delivered orders. | Unit totals across eligible order lines, not an order count. |

On-time, in-full, and OTIF are delivered-order service measures. Do not use cancelled orders as failed deliveries in those denominators. Cancellation is measured separately. The overall line unit fill rate can remain high even when some orders are not fully filled, so do not treat unit fill and in-full order rate as interchangeable.

The SQL uses `order_date` to assign order-month cohorts. If a chart is grouped by order month, do not call it delivery month.

## 7. What the three dashboard pages are for

### Fulfillment Overview

This page answers: **What is the overall scale and service mix in the selected synthetic sample?** Use the KPI cards and trend to show submitted/delivered/cancelled volume and on-time, in-full, OTIF, and fill measures. Make the eligible order count visible next to service rates.

### Diagnostic Segments

This page answers: **Where do the synthetic rates or incomplete-line counts differ enough to inspect further?** Compare market, carrier, product/category, and customer segment as supported by the page. Show volume with every rate. A segment with a high or low percentage but only a few orders should not be presented as a stable pattern.

### Data & Methodology

This page answers: **What do these numbers mean, where did they come from, and what should a viewer not infer?** Explain the synthetic data, table grain, KPI definitions, cancellation exclusions, data checks, and limitations.

## 8. How to write findings from your actual report

Do not start by choosing the most dramatic bar. For each possible finding, follow this sequence:

1. **Name the measure and time basis.** Example: OTIF by market and order month.
2. **Read the numerator and denominator.** Record “x of n orders,” not only a percent. Confirm the denominator includes only eligible delivered orders for service rates.
3. **Compare like with like.** Use the same dates, filter context, metric definition, and denominator rules for both groups.
4. **Check volume and context.** Note the group’s order count and compare it with the other groups or overall sample. Avoid strong claims about tiny groups.
5. **Trace the result to records.** Use SQL or the underlying Power BI rows to inspect representative late or incomplete orders/lines.
6. **State the synthetic limitation in the finding itself.** The generator intentionally programs some group-level differences, so a segment result is a demonstration of the analysis—not a real operational discovery or a causal explanation.

### Fill-in finding template

> In the generated sample, **[segment and filter]** had **[x] of [n] eligible delivered orders** on time / in full / OTIF (**[x/n as a percentage]**) for **[order-month period]**, compared with **[y] of [m] ([y/m as a percentage])** for **[comparison group]**. This is a descriptive pattern in synthetic records; it does not establish real-world carrier/customer/product performance or explain a cause.

For product diagnostics, identify the exact SKU/category and report incomplete lines, affected orders, and undelivered units. For cancellation, use cancelled orders divided by all submitted orders—not delivered orders.

### Fill-in recommendation template

> **Portfolio-safe follow-up:** If a similar pattern appeared in real operations, first validate the source events, service-promise rules, data completeness, and the affected orders/lines. Then investigate plausible causes with real shipment scans, inventory availability, and customer-promise data before testing an intervention. This synthetic project does not justify replacing a carrier, changing inventory, or claiming savings.

This is a recommendation for what a real analyst would investigate next, not a claim that the synthetic data proves a business action will work.

## 9. What you can say in an interview

> “I generated and validated a reproducible synthetic order dataset, loaded it into PostgreSQL, and used SQL to calculate order-level on-time, in-full, and OTIF measures plus unit fill and cancellations. I manually checked delivered and cancelled examples against the KPI rules, then connected the one-row-per-order service view and related dimensions/lines to Power BI. I built an overview, segment diagnostics, and methodology pages. The data is synthetic, so I present segment differences as demonstrations of the analysis—not real operational findings. I did not implement n8n automation.”

Only say that the Power BI measures reconcile to SQL if you have checked them under matching filters and recorded that evidence.

## 10. Your remaining repository tasks

The technical implementation is complete according to your report. To make the GitHub project easy for another person to review, you still need to add:

1. **A Power BI artifact:** preferably the `.pbix` file, if you can share it safely; otherwise add clear screenshots of all three pages under `dashboard/screenshots/`. Use [`dashboard/README.md`](../dashboard/README.md) for the exact file list and checks.
2. **Your actual findings and recommendations:** populate the fill-in templates above with the real values, numerators, denominators, periods, and group volumes shown in your Power BI report. Do not use example numbers that are not in your report.
3. **A reconciliation note:** if you already compared the Power BI measures with the SQL results, record which measures, filter settings, and outputs matched. If you have not done this, compare them before saying they reconcile.
4. **More AI-use detail (optional but useful):** the repository can state the AI tasks you listed, but add exact tool/date/prompt summaries and your human validation if you want a prompt-level audit trail. Do not invent those details after the fact.

See the project’s [`README.md`](../README.md) for the status and entry points. n8n is explicitly outside the implemented workflow.
