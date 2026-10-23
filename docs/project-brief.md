# Project Brief

## Project at a glance

- **Title:** AI-Assisted Order Fulfillment Analytics on a Synthetic Retail Dataset
- **Type:** Portfolio skills demonstration using fully synthetic, deterministic records.
- **Business scenario:** A fictional specialty-food retailer serves wholesale customers in the US and India and wants visibility into fulfillment reliability.
- **Primary question:** How would an operations analyst identify where fulfillment performance needs investigation, and how would the analyst validate an automated, AI-assisted reporting workflow?
- **Analyst role:** Independent portfolio analyst; no real stakeholder interviews or operational implementation are claimed.
- **Planned stack:** Python generator/validation, n8n, PostgreSQL, SQL, one dashboard tool, and an AI assistant used as a copilot.

## Problem framing

The project demonstrates how an analyst could ingest order and order-line records, validate their quality, calculate explicitly defined service measures, and present diagnostic cuts by market, product, customer, and carrier. The input records are designed for practice and contain known synthetic variation. Any patterns discovered are characteristics of the dataset generator, not findings about a real supply chain.

## Objectives

1. Reproduce the synthetic dataset from a version-controlled generator and fixed seed.
2. Document every table’s grain, keys, fields, and intended relationships.
3. Build a repeatable n8n-to-PostgreSQL pipeline with error handling and load audit.
4. Implement order- and line-level fulfillment measures in SQL.
5. Independently verify the calculations and test bad-input fixtures.
6. Use AI to draft or review a bounded analysis task, then record human validation.
7. Build a clear dashboard and communicate the synthetic-data limitation prominently.

## Analysis questions

- How do order-level on-time, in-full, and OTIF rates vary by market and month in this generated sample?
- Which products, customers, or carriers appear in lower-service segments in the generated records, and how much order volume do those segments represent?
- How do cancellations and incomplete order lines affect service measures under the documented denominator rules?
- Does the workflow correctly reject malformed or duplicate input and avoid double-loading a repeated batch?

These are practice questions. Their answers describe only this constructed dataset and must not be presented as empirical or causal real-world conclusions.

## Scope and boundaries

**In scope:** synthetic orders, order lines, customers, products, carriers; validation fixtures; data model; ETL/workflow automation; service KPI calculations; dashboard and AI-validation process.

**Out of scope:** real company performance, actual supplier/carrier contract performance, stockout diagnosis, inventory optimization, safety stock, reorder points, realized cost savings, and claims of implemented business change. The dataset does not contain on-hand inventory or replenishment history.

## Deliverables

- `data/synthetic/` reproducible CSV tables and manifest.
- `src/generate_synthetic_dataset.py` deterministic generator and `data/fixtures/` invalid test inputs.
- Data dictionary, metric definitions, source/data card, and limitation disclosures.
- SQL DDL, data-quality checks, KPI queries, and diagnostic queries.
- Redacted n8n workflow export/notes, database load log, and validation evidence.
- Dashboard with clear “synthetic demonstration” labeling.
- AI use/validation log, README, and a short screen-recorded project walkthrough.

## Success criteria for the project

Success means a reviewer can regenerate the input, understand the row grains, reproduce the SQL, see the pipeline handle valid and invalid inputs, trace AI-assisted code to independent checks, and distinguish generated example patterns from real-world evidence. Success does **not** mean improving any actual company KPI.
