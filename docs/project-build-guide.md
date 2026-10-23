# Project Build Guide: Synthetic Order Fulfillment Analytics

## Should you use generated data?

Use this repository’s synthetic dataset to demonstrate a reproducible analyst workflow: generate and inspect records, validate the schema and relationships, load PostgreSQL, write and check SQL, analyze service KPIs, use AI with review, and communicate the results in a dashboard. The project does not redistribute the tutorial creator’s restricted files.

Synthetic data is **not empirical evidence**. The generator intentionally varies punctuality and partial fulfillment by fictional groups. A result from these rows demonstrates that your analysis can calculate and display a programmed pattern; it is not a discovery about real-world supply chains or an industry benchmark. Label the dataset and every dashboard page as synthetic. Do not claim that a real company improved, that a carrier is genuinely poor, or that inventory caused short shipments.

n8n is optional. The core project can use the documented direct CSV-to-PostgreSQL loading steps and focus on data validation, SQL, KPI logic, dashboarding, and communication. The workflow export in `n8n/` is an unexecuted reference, not evidence that you built or ran automation. It has not been verified for n8n 2.4.6.

For stronger internship evidence, keep this as a technical demonstration and, if possible, build a separate analysis using an openly licensed real dataset. Do not blend the two sources or imply the synthetic rows are real.

## Project brief

**Title:** AI-Assisted Order Fulfillment Analytics on a Synthetic Retail Dataset

**Question:** How can an operations analyst identify segments in the generated sample that merit investigation and verify the service measures used to communicate them?

**Scope:** Generated orders, order lines, customers, products, and carriers covering two fictional markets; relational modeling; PostgreSQL loading; data-quality checks; order-level service KPIs; diagnostic segmentation; dashboard design; and AI validation. Workflow automation with n8n is an optional extension.

**Not in scope:** Real company performance, inventory-on-hand, stockouts, supplier lead times, safety stock, reorder points, real carrier evaluation, actual savings, or implemented business change.

## Core build sequence

1. Generate the CSVs using `src/generate_synthetic_dataset.py` and run `src/validate_synthetic_dataset.py`.
2. Read `docs/synthetic-data-card.md` and `docs/data-dictionary.md`; keep the synthetic disclosure visible.
3. Create PostgreSQL tables from `sql/01_create_tables.sql` and load dimensions before orders and lines using the documented database setup/import steps.
4. Run `sql/02_quality_checks.sql`; resolve structural problems before analysis.
5. Run the committed KPI and segment queries. Verify order-grain logic manually and use checked SQL output as the dashboard source.
6. Use an AI assistant only for bounded drafting or review. Record what it generated, what you changed, and the independent check in `docs/ai-usage-log.md`.
7. Build a dashboard with prominent synthetic-data labels and denominators; reconcile its values to SQL.
8. Write a short case study that describes the technical demonstration without presenting synthetic patterns as real operational findings.

## Optional n8n extension

Skip this while building the core portfolio. If you later choose to implement workflow automation, treat `n8n/csv-to-postgresql.json` and `n8n/workflow-plan.md` as draft reference material only. They are unexecuted and their compatibility with n8n 2.4.6 has not been verified. Update or recreate the workflow for your exact n8n version, then import, execute, and test it before describing it as completed work.

## Project quality bar

A reviewer should be able to regenerate the dataset, understand table grains, rerun SQL, see your independent KPI checks, follow AI validation, and distinguish demonstration data from empirical data. The n8n workflow and fixture-rejection branch are optional and must not be implied to have run unless you actually test them. Detailed instructions are in [`step-by-step-project-instructions.md`](step-by-step-project-instructions.md).
