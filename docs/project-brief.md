# Project Brief

## Project at a glance

- **Title:** AI-Assisted Order Fulfillment Analytics on a Synthetic Retail Dataset
- **Type:** Portfolio skills demonstration using fully synthetic, deterministic records.
- **Business scenario:** A fictional specialty-food retailer serves wholesale customers in the US and India and wants visibility into fulfillment reliability.
- **Primary question:** How can an analyst identify segments in this generated sample that warrant investigation, and independently verify the service measures used to communicate them?
- **Analyst role:** Independent portfolio analyst; no real stakeholder interviews or operational implementation are claimed.
- **Core stack:** Python generator and validator, PostgreSQL, SQL, one dashboard tool, and an AI assistant used as a copilot. n8n is an optional extension, not a core requirement.

## Problem framing

The project demonstrates how an analyst can understand order and order-line data, validate its quality, calculate explicitly defined service measures, and present diagnostic cuts by market, product, customer, and carrier. The CSVs can be loaded into PostgreSQL using the documented database-import steps. Any patterns discovered are characteristics of the synthetic data generator, not findings about a real supply chain.

## Objectives

1. Reproduce the synthetic dataset from a version-controlled generator and fixed seed.
2. Document each table’s grain, keys, fields, and intended relationships.
3. Load the synthetic tables into PostgreSQL and run data-quality checks.
4. Implement order- and line-level fulfillment measures in SQL.
5. Independently verify the calculations using selected records and documented KPI definitions.
6. Use AI to draft or review a bounded analysis task, then record human validation.
7. Build a clear dashboard and communicate the synthetic-data limitation prominently.

Workflow automation with n8n may be added later as a separate extension. Skipping it does not prevent completion of the core analyst project.

## Analysis questions

- How do order-level on-time, in-full, and OTIF rates vary by market and month in this generated sample?
- Which products, customers, or carriers appear in lower-service segments in the generated records, and how much order volume do those segments represent?
- How do cancellations and incomplete order lines affect service measures under the documented denominator rules?
- Do the data-quality checks and manual record reconciliations support the KPI calculations and reveal any data limitations?

These are practice questions. Their answers describe only this constructed dataset and must not be presented as empirical or causal real-world conclusions.

## Scope and boundaries

**In scope:** synthetic orders, order lines, customers, products, carriers; data validation; relational modeling; PostgreSQL loading; service KPI calculations; dashboard and AI-validation process. n8n-based workflow automation is optional.

**Out of scope:** real company performance, actual supplier/carrier contract performance, stockout diagnosis, inventory optimization, safety stock, reorder points, realized cost savings, and claims of implemented business change. The dataset does not contain on-hand inventory or replenishment history.

## Deliverables

- `data/synthetic/` reproducible CSV tables and manifest.
- `src/generate_synthetic_dataset.py` deterministic generator and separate `data/fixtures/` invalid test inputs.
- Data dictionary, metric definitions, source/data card, and limitation disclosures.
- SQL DDL, data-quality checks, KPI queries, and diagnostic queries.
- Dashboard with clear “synthetic demonstration” labeling.
- AI use/validation log, README, and a short project walkthrough.
- **Optional only:** the n8n JSON and notes under `n8n/` are unexecuted reference material, are not needed for the core deliverable, and have not been verified for n8n 2.4.6.

## Success criteria for the core project

A reviewer can regenerate and validate the input, understand the row grains, reproduce the SQL, inspect a few KPI classifications against source rows, follow the AI validation, and distinguish generated example patterns from real-world evidence. Success does **not** require a workflow automation tool and does not mean improving any actual company KPI.
