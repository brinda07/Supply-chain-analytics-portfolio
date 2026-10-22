# Project Brief

## Project at a glance

- **Working title:** AI-Assisted Order Fulfillment Performance Analysis
- **Project type:** Tutorial-data portfolio case study; confirm and state whether the supplied files are synthetic or otherwise before describing their provenance.
- **Scenario:** The video presents a fictional food retailer operating in India and the US and describes order-header and order-line files.
- **Primary question:** Which market, product, customer, or time period shows the clearest fulfillment issue that an operations team should investigate?
- **Planned tools:** n8n, PostgreSQL, SQL, Python for validation, and one dashboard tool. An AI-enabled spreadsheet/assistant may be used as a copilot.

## Problem statement

The fictional business wants better visibility into order fulfillment before expanding. The available tutorial files may support descriptive analysis of orders and lines, but the exact columns and coverage must be verified before choosing KPIs. The analysis will identify patterns and investigation priorities; it will not claim causal explanations that are absent from the data.

## Objectives

1. Inspect and document source-file grain, field meanings, coverage, and quality.
2. Create a repeatable, auditable file-ingestion and data-preparation workflow.
3. Define and calculate supported fulfillment measures at the correct grain.
4. Compare service patterns across available markets, products, customers, and months.
5. Use AI to assist with drafting or summarizing, then independently validate the output.
6. Communicate evidence-backed findings, limitations, and next steps.

## Scope

**In scope:** tutorial-provided order data, data profiling, data ingestion, PostgreSQL modeling, supported fulfillment KPIs, descriptive comparisons, a dashboard, AI-use documentation, and reproducibility.

**Out of scope unless additional data supports it:** actual inventory levels, stockout rates, safety-stock or reorder-point recommendations, supplier performance, verified root causes, financial savings, implementation impact, and claims about a real company's performance.

## Stakeholders

Use roles such as operations leader, customer-service lead, and analyst as **proposed personas** for framing the questions. No stakeholder interview or approval should be claimed unless it actually occurred. Dataset observations are evidence; scenario details supplied by the video are context, not independently verified business facts.

## Deliverables

- Data provenance, dictionary, and quality notes.
- Reproducible n8n-to-PostgreSQL workflow notes/export, with secrets removed.
- SQL and validation code.
- KPI definitions and tested dashboard.
- Findings log with evidence and limitations.
- AI usage/validation log.
- README and short screen-recorded case-study walkthrough.

## Open questions to resolve before analysis

- What files are available, and what license/reuse terms apply?
- What does one row represent in each file?
- Do promised date, actual delivery date, ordered quantity, and delivered quantity exist?
- How are canceled, returned, split, or partially delivered orders represented?
- Are price values in multiple currencies, and is a valid conversion-rate series available?
- Which fields are identifiers versus measures, and what are the stable join keys?
