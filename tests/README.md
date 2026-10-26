# Tests and Validation Evidence

## Completed checks reported by the project author

- Synthetic dataset generation and structural validation.
- Execution of `02_quality_checks.sql` and the project's KPI, diagnostic, and view-creation SQL files in PostgreSQL.
- Manual KPI checks for delivered order `ORD-000001` and cancelled order `ORD-000036`.

The repository includes the [manual KPI validation note](manual-kpi-validation.md), which shows the source dates, line quantities, expected classifications, and reproducible SQL. The committed Python validator checks CSV structure and data rules; it does not independently calculate service KPI values.

## Database and dashboard result evidence

The author reports creating the PostgreSQL tables/view and Power BI model, measures, and pages. Query-result exports, screenshots, and the `.pbix` report are not in the repository yet. Add a safe-to-share Power BI file or sanitized screenshots under `dashboard/` as described in [`dashboard/README.md`](../dashboard/README.md). If you have already reconciled each Power BI measure to SQL, record the filters and matching values; otherwise perform that comparison before claiming reconciliation.

## Not implemented

n8n fixture-rejection, load-audit automation, and repeat-load automation were not implemented. Do not list those as completed tests. The invalid fixture CSVs remain optional test inputs and must never be loaded into the analytical tables or included in KPI calculations.
