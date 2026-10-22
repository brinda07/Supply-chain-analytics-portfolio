# AI-Assisted Supply Chain Order Fulfillment Analysis

> **Status: project scaffold.** The tutorial dataset has not yet been inspected in this repository, so no KPI results or business findings are claimed.

## Project question

Which markets, products, or customers show the clearest order-fulfillment risk, and what should an operations team investigate first?

This portfolio project adapts the workflow in the supplied video: order-header and order-line CSVs flow through an automated intake into PostgreSQL, then into a documented analysis and dashboard. The video describes a fictional retailer and tutorial-provided files. Results from those files must not be presented as real operating-company performance.

## What this project is—and is not

The goal is to demonstrate supply-chain analysis, data quality, SQL, workflow automation, dashboard communication, and responsible AI-assisted work. The initial scope is **order fulfillment**, not proven inventory optimization. Inventory conclusions require appropriate stock, replenishment, and lead-time data. On-time and OTIF measures will only be calculated if the source includes the required promised/actual delivery dates and delivered quantities.

AI tools may help draft code and summarize validated results. They are not the authority for metric definitions or final numbers; generated outputs must be independently checked.

## Repository map

- `docs/project-build-guide.md` — detailed build sequence and portfolio advice.
- `docs/project-brief.md` — project purpose, scope, assumptions, and open questions.
- `docs/metric-definitions.md` — KPI definitions and field requirements.
- `docs/data-dictionary.md` — mapping template to complete after inspecting source files.
- `docs/ai-usage-log.md` — template for recording AI assistance and validation.
- `docs/reference/` — the attached general business-analysis template for reference.
- `data/raw/` — intentionally empty; raw tutorial data is excluded by default.
- `n8n/` — workflow plan; add an exported, credential-redacted workflow after building it.
- `sql/`, `src/`, `tests/` — planned analysis and validation code.
- `dashboard/` — planned dashboard screenshots or permitted sharing instructions.

## Build status

1. [x] Create project documentation scaffold.
2. [ ] Obtain and inspect the tutorial files; document provenance and reuse terms.
3. [ ] Map actual fields, row grain, keys, and data-quality issues.
4. [ ] Implement and test ingestion and clean SQL views.
5. [ ] Calculate only supported KPIs; independently validate results.
6. [ ] Build the dashboard, summarize findings, and record AI validation.
7. [ ] Publish a short case study and reproducible setup instructions.

## Before publishing

Replace placeholders with verified details. Do not commit credentials, private email data, or tutorial files unless redistribution is permitted. Keep real findings, estimates, assumptions, and simulated scenario details clearly distinguished. See `docs/project-build-guide.md` for the full build plan.
