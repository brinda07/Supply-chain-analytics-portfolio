# AI Usage and Validation Log

## Author-reported use in this project

The project author reports using an AI assistant for the following parts of the implementation:

- Understanding the schema and data model.
- Reviewing SQL.
- Checking KPI definitions and validation logic.
- Troubleshooting PostgreSQL.
- Reviewing Power BI dashboard design.
- Supporting project documentation.

The specific AI product/model, dates, exact prompts, generated drafts, and per-task human edits were not supplied for this log. This summary records the author's report; it is **not** a prompt-level audit trail and should not be represented as one. Do not backfill dates or prompt wording from memory unless you can verify them.

## How AI was bounded in the project

The repository's source files, SQL definitions, manually checked orders, and the author's Power BI report are the evidence for project calculations. AI assistance does not establish that a number is correct. Before publishing a finding, check it against the relevant SQL result or Power BI filter context, verify the numerator and denominator, and keep the synthetic-data limitation visible.

## Validation evidence currently documented

- The generated dataset has a deterministic structural validator: `src/validate_synthetic_dataset.py`.
- The project includes explicit KPI definitions in `metric-definitions.md`.
- Manual record checks for `ORD-000001` and `ORD-000036` are documented in `../tests/manual-kpi-validation.md`.
- The author reports running the SQL analyses and creating the corresponding Power BI measures and pages.

## Optional prompt-level audit additions

If you still have access to the original AI sessions and want a more detailed audit, add a dated entry for each material task with the tool/model, a short prompt summary, what was accepted or changed, and the independent check. Exclude credentials, personal information, and private database connection details.
