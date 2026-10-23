# Project Build Guide: Synthetic Order Fulfillment Analytics

## Should you use generated data?

Use this repository’s synthetic dataset to demonstrate that you can build a reproducible data workflow: generate/inspect records, validate schemas, load PostgreSQL, write SQL, test n8n error paths, use AI with review, and communicate results in a dashboard. It solves the redistribution issue because the tutorial creator’s files are not included.

However, synthetic data is **not empirical evidence**. The generator intentionally varies punctuality and partial fulfillment by fictional groups. A result from those rows is a demonstration that your code can calculate and surface a programmed pattern—not a discovery about real-world supply chains or an industry benchmark. Label the dataset and every dashboard page as synthetic. Do not claim a real company improved, that a carrier is genuinely poor, or that inventory caused short shipments.

For stronger internship evidence, keep this as a technical pipeline project and, if possible, build a separate analysis using an openly licensed real dataset. Do not blend the two sources or imply the synthetic rows are real.

## Project brief

**Title:** AI-Assisted Order Fulfillment Analytics on a Synthetic Retail Dataset

**Question:** How would an operations analyst identify where fulfillment performance needs investigation, and how would the analyst validate an automated, AI-assisted reporting workflow?

**Scope:** Generated orders, order lines, customers, products, and carriers covering two fictional markets; relational modeling; ETL; data-quality testing; order-level service KPIs; diagnostic segmentation; dashboard design; AI validation.

**Not in scope:** Real company performance, inventory-on-hand, stockouts, supplier lead times, safety stock, reorder points, real carrier evaluation, actual savings, or implemented business change.

## Build sequence

1. Generate the CSVs using `src/generate_synthetic_dataset.py` and run `src/validate_synthetic_dataset.py`.
2. Read `docs/synthetic-data-card.md` and `docs/data-dictionary.md`; keep the synthetic disclosure visible.
3. Create PostgreSQL tables from `sql/01_create_tables.sql` and load dimensions before orders and lines.
4. Run `sql/02_quality_checks.sql`; resolve structural problems before the dashboard.
5. Build an n8n manual-trigger workflow for accepted data and deliberately invalid `data/fixtures/` inputs. Keep secrets outside Git.
6. Run the committed KPI and segment queries. Verify order-grain logic manually and use the SQL output as the dashboard source.
7. Use an AI assistant only for bounded drafting/review. Record what it generated, what you changed, and the independent check in `docs/ai-usage-log.md`.
8. Build a dashboard with prominent synthetic-data labels and denominators; reconcile its values to SQL.
9. Write a short case study that describes the technical demonstration without presenting synthetic patterns as real operational findings.

## Project quality bar

A reviewer should be able to regenerate the dataset, understand table grains, rerun SQL, see invalid records rejected, follow AI validation, and distinguish demonstration data from empirical data. The detailed instructions are in [`step-by-step-project-instructions.md`](step-by-step-project-instructions.md).
