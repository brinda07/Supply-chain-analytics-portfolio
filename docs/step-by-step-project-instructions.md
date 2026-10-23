# Step-by-Step Instructions: Synthetic Order Fulfillment Analytics

This guide now uses the **fully synthetic dataset included in this repository**. It does not redistribute the tutorial creator’s restricted dataset. Follow the phases in sequence. The records are useful for practicing a reproducible analytics workflow, but any results describe only a programmed example—not a real company, market, customer, carrier, or industry benchmark.

## What you will build

A portfolio demonstration that uses generated order, order-line, customer, product, and carrier data to practice:

- reproducible data generation;

- relational modeling and SQL;

- repeatable PostgreSQL loading and SQL-based analytics (n8n automation is optional);

- data-quality and failure-path testing;

- order-level fulfillment KPIs;

- AI-assisted drafting with independent validation;

- a dashboard and an honest business-style case presentation.

**Do not describe this as a real-company inventory optimization.** There are no inventory balances, stock movements, purchase orders, supplier lead times, or actual carrier events in the dataset. The synthetic generator intentionally programs variation by carrier, market, and product category, so resulting patterns are practice examples, not discoveries about reality.

## Phase 1 — Set up and understand the repository

### 1.1 Clone the repository

If you do not already have the local project folder, open a terminal and run:

```bash
git clone https://github.com/brinda07/Supply-chain-analytics-portfolio.git
cd Supply-chain-analytics-portfolio
```

The repository may be private. Sign in to GitHub before cloning. If you prefer not to use Git yet, download the repository ZIP, extract it, and work inside the extracted directory. Avoid editing two separate copies of the repository.

### 1.2 Read the project framing first

Read these files in order:

1. `README.md` — portfolio-facing overview.

1. `docs/project-brief.md` — question, scope, and success criteria.

1. `docs/synthetic-data-card.md` — how the generated data may and may not be interpreted.

1. `docs/metric-definitions.md` — exact denominators and formulas.

1. `docs/data-dictionary.md` — field names, row grains, and relationships.

The project should be labeled “synthetic dataset demonstration” wherever you show a dashboard, screenshot, video, or portfolio summary. Do not use fabricated stakeholder quotes, interviews, actual business impact, or real-world conclusions.

### 1.3 Generate or regenerate the data

From the repository root, run:

```bash
python3 --version
python3 src/generate_synthetic_dataset.py
```

On Windows, `python` may be the command instead of `python3`:

```
python --version
python src/generate_synthetic_dataset.py
```

The generator requires only the Python standard library. It writes five clean CSVs and a manifest to `data/synthetic/`, plus separate invalid-input fixtures under `data/fixtures/`. It uses a fixed seed, so rerunning the same script should reproduce the same records.

Expected current file counts are listed in `data/synthetic/README.md` and `dataset_manifest.json`. If you change the script or seed, rerun it and update those documents. Don’t manually edit generated CSVs; change the generator or create a separate documented fixture instead.

### 1.4 Run structural validation

Run:

```bash
python3 src/validate_synthetic_dataset.py
```

The validator checks expected columns, primary keys, foreign keys, market/currency consistency, date logic, quantity rules, and that orders have lines. It deliberately does **not** calculate or report service KPI results. Resolve any validation error before database loading.

The test fixtures are intentionally invalid. Do not run the structural validator against them and do not copy them into `data/synthetic/`. They are optional inputs for testing an ingestion-rejection path if you later choose to build one; n8n is not required for the core project.

### 1.5 Inspect the files yourself

Open each file or print its header and a few sample rows. Confirm that the files match the data card:

- `orders.csv`: one row per order.

- `order_lines.csv`: one row per order-product line.

- `customers.csv`: one row per customer.

- `products.csv`: one row per SKU.

- `carriers.csv`: one row per carrier.

A useful short command is:

```bash
python3 - <<'PY'
import csv
from pathlib import Path
for p in sorted(Path('data/synthetic').glob('*.csv')):
    with p.open(encoding='utf-8', newline='') as f:
        r = csv.DictReader(f)
        print('\n', p.name, r.fieldnames)
        for _, row in zip(range(2), r):
            print(row)
PY
```

Use `docs/data-dictionary.md` to learn field meanings. Note that `orders.csv` has the dates and status at order grain, while quantities are at line grain. This difference matters when calculating order-level OTIF.

**Checkpoint:** the generator runs, the structural validator passes, and you can explain the grain and key of each CSV.

## Phase 2 — Understand the synthetic data before building charts

### 2.1 Know what was designed into the generator

The generator deliberately sets different late-delivery probabilities for fictional carriers and markets, different partial-fulfillment probabilities for markets/categories, and a small cancellation probability. These are **scenario controls**. They are present so you can practice analysis and test whether your code detects the underlying programmed variations.

Your portfolio language must say “in this synthetic sample” or “the generated records.” Don’t write that the results establish typical delivery performance or that a carrier/category actually underperforms in the real world. A segment comparison is not a causal analysis.

### 2.2 Write your analysis questions

Use these questions as exercises:

1. How do on-time, in-full, and OTIF rates vary by market and order month in the generated data?

1. Which fictional carrier has the lowest on-time rate, and how many delivered orders are in that group?

1. Which SKU/category has the most incomplete lines or undelivered units?

1. How do cancellation rates vary by market and month?

1. Does the SQL workflow return the expected data grain and handle the intentionally invalid fixtures?

The business-like recommendation should be explicitly hypothetical, such as: “In an actual operation, this segment would be a candidate for investigation. The synthetic records do not establish a real operational issue.”

### 2.3 Use the available measures correctly

Definitions are in `docs/metric-definitions.md`. Follow these rules:

- Count orders using distinct order IDs, not line rows.

- Exclude cancelled orders from delivery-service denominators; report cancellations separately.

- Calculate order in-full status by checking **every line**; extra units for one SKU must not offset a shortage in another.

- Calculate OTIF as the direct intersection of on-time and in-full at order level.

- Calculate unit fill rate as total delivered units ÷ total ordered units for delivered orders, and label it a unit-weighted measure.

- Use the order month consistently for monthly cohorts unless a visual explicitly uses delivery month.

- Show denominators or eligible order counts with percentages.

- Keep USD and INR amounts separate. This dataset has no historical FX table.

**Checkpoint:** you can distinguish order count, line count, unit fill rate, in-full order rate, on-time rate, and OTIF.

## Phase 3 — Build the PostgreSQL database

### 3.1 Choose a database environment

Use a local PostgreSQL install or a hosted PostgreSQL service you control. Keep the database private and use project-only credentials. Current hosted-service pricing, limits, and security settings may change; check them directly if you use a hosted service.

The example commands below assume `psql` is installed and your local PostgreSQL account can create databases. If not, use your database provider’s SQL editor/console and CSV import feature, or install PostgreSQL using its current official installer.

### 3.2 Create the database and tables

From the repository root:

```bash
createdb supply_chain_portfolio
psql -d supply_chain_portfolio -f sql/01_create_tables.sql
```

If your local account requires a username, add `-U your_postgres_user` to both commands. For pgAdmin, create a database named `supply_chain_portfolio`, open Query Tool for that database, and run the contents of `sql/01_create_tables.sql`.

This creates the `supply_chain` schema and typed tables. Read the SQL before executing it. The foreign keys mean you must load dimension files before orders and order lines.

### 3.3 Load the clean CSVs

For a fast first-pass SQL demonstration, load the generated clean files using PostgreSQL’s `psql` client `\copy` command. `\copy` reads files from the computer running `psql`. Run this from the repository root and substitute your username/database flags as needed:

```bash
psql -d supply_chain_portfolio
```

At the `psql` prompt, enter these one at a time, in order:

```sql
\copy supply_chain.customers(customer_id, customer_name, market, city, customer_segment) FROM 'data/synthetic/customers.csv' WITH (FORMAT csv, HEADER true)
\copy supply_chain.products(sku_id, product_name, category, shelf_life_days, unit_of_measure) FROM 'data/synthetic/products.csv' WITH (FORMAT csv, HEADER true)
\copy supply_chain.carriers(carrier_id, carrier_name, market) FROM 'data/synthetic/carriers.csv' WITH (FORMAT csv, HEADER true)
\copy supply_chain.orders(order_id, customer_id, carrier_id, market, order_date, promised_delivery_date, actual_delivery_date, order_status, currency_code) FROM 'data/synthetic/orders.csv' WITH (FORMAT csv, HEADER true)
\copy supply_chain.order_lines(line_id, order_id, line_number, sku_id, ordered_qty, delivered_qty, unit_price_local, currency_code) FROM 'data/synthetic/order_lines.csv' WITH (FORMAT csv, HEADER true)
```

Exit with `\q`. If a relation already contains data, do not blindly load again: the primary keys will reject duplicates. To reset a practice database, confirm it contains only this project’s data, then drop/recreate the database or truncate the project tables in dependency order before reloading.

For a pgAdmin route, use its Import/Export Data function per table, select CSV, enable Header, and load files in the same dependency order. Confirm each import’s success message and row count.

### 3.4 Verify the load

Run the checks:

```bash
psql -d supply_chain_portfolio -f sql/02_quality_checks.sql
```

The first result gives table row counts; subsequent results should show zero for the listed structural errors. If they do not, stop and inspect the load before continuing. Add database load row counts to your project notes, but do not treat them as business findings.

Create the dashboard view:

```bash
psql -d supply_chain_portfolio -f sql/05_dashboard_views.sql
```

Then test it:

```bash
psql -d supply_chain_portfolio -c "SELECT * FROM supply_chain.order_service LIMIT 10;"
```

### 3.5 Record database details safely

Add non-secret setup notes to `README.md` or `docs/database-setup.md`: PostgreSQL version, commands used, table dependencies, and where the credentials are configured. Never commit passwords, tokens, private connection URLs, `.env` files, or database screenshots containing secrets. The repository ignores raw files under `data/raw/`, but the synthetic files are intentionally committed.

**Checkpoint:** the tables load in dependency order, SQL quality checks pass, and `order_service` returns one row per order.

## Phase 4 — Optional n8n extension (skip for the core project)

You can skip this entire phase and continue to Phase 5. The core analyst project uses the CSV import in Phase 3, PostgreSQL, SQL analysis, dashboard reconciliation, and clear communication. n8n is not required to demonstrate those skills.

The repository keeps `n8n/csv-to-postgresql.json` as a reference, but it is unexecuted and not suitable to claim as completed work. It uses PostgreSQL node version 2.8, while n8n 2.4.6 provides that node only through version 2.6. Do not import this draft into your current instance. The limitation and source reference are recorded in `n8n/workflow-plan.md`.

If you later decide to add automation, first create or adapt a workflow for your installed n8n version. Then test it with your own runtime file path and PostgreSQL credentials. Verify clean loads, rejected fixtures, row counts, and duplicate handling before adding it to your portfolio. Keep credentials outside Git.

**Optional checkpoint:** only if you implement the extension, document the exact n8n version and tests you actually ran. Otherwise, proceed directly to Phase 5.

## Phase 5 — Run and validate the SQL analyses

### 5.1 Run the KPI queries

Execute:

```bash
psql -d supply_chain_portfolio -f sql/03_fulfillment_kpis.sql
psql -d supply_chain_portfolio -f sql/04_segment_diagnostics.sql
```

These queries are examples over the synthetic tables. Their output is not a real business finding. Read each query and confirm the grain before using it. The month in the KPI query is based on `order_date`; do not label it delivery month.

### 5.2 Validate the logic manually

Select a small set of order IDs from different statuses and manually compare `orders.csv` with all matching lines in `order_lines.csv`:

- For a delivered order, compare actual date with promised date.

- For each line, compare delivered quantity with ordered quantity.

- Mark the order in-full only if every line is in-full.

- Mark OTIF only if the order is both in-full and on-time.

- For a cancelled order, confirm it is excluded from delivery-service rates but counted in submitted orders/cancellations.

Record the sample IDs and your checks in `tests/` without changing the generated data. Re-run the SQL queries and compare the classification. Also confirm OTIF is no larger than either on-time or in-full rate when they share the same denominator.

### 5.3 Protect against join-grain mistakes

Before counting orders after a join, check whether one order has several order lines. Use distinct order IDs or first aggregate lines to order grain. Do not sum an order-header value once for every order line. Use line-level measures for line counts/units and order-level measures for service percentages.

### 5.4 Keep currencies separate

`unit_price_local` is a fictional local price. Use a market/currency filter when grouping monetary values. There is no FX table. Do not make cross-market total revenue comparisons by adding INR to USD.

**Checkpoint:** you can reproduce each KPI query, explain its numerator/denominator, and trace sample classifications back to raw CSV rows.

## Phase 6 — Demonstrate AI assistance responsibly

The AI component is your workflow for using a model carefully, not a claim that AI makes the analysis correct.

### 6.1 Ask the AI for a bounded task

Give it the exact schema and metric definitions. Ask it to list missing assumptions before writing SQL. You can use this prompt:

> You are assisting with an explicitly synthetic order-fulfillment project. Use only the provided table names, fields, and definitions. First identify any missing inputs or ambiguity. Then draft SQL for OTIF by market and order month at one row per order. Exclude cancelled orders, define the denominator, and calculate the intersection of on-time and in-full directly. Include an audit query showing each order’s on-time and in-full flags. Do not describe any output as a real-world finding or industry benchmark.

### 6.2 Review and verify the answer

Check that the model:

- uses columns that really exist;

- aggregates order lines to order grain before order KPIs;

- applies the cancellation filter consistently;

- uses actual vs promised dates correctly;

- checks every order line for the in-full flag;

- does not combine USD and INR;

- does not infer inventory or root causes.

Run its query against PostgreSQL. Compare it with the committed SQL and manually checked sample orders. Save the prompt summary, model draft, your final changes, and validation method in `docs/ai-usage-log.md`.

### 6.3 Use AI to summarize only checked outputs

Give the model aggregate query results or a non-sensitive table and ask for a draft that states the unit, period, denominator, and synthetic-data limitation. Verify every number and claim yourself. A good caption says “in this generated sample”; it does not say “this carrier is poor in the real world.”

**Checkpoint:** your log shows what AI did, what you changed, and how you verified it.

## Phase 7 — Build the dashboard

Use **Power BI Desktop** if you have access to it, since it is a recognizable analyst tool. If you do not, use another dashboard tool that connects to PostgreSQL or export the query outputs to CSV and build a reproducible Python/Plotly dashboard. Choose one primary dashboard route rather than making several unfinished ones.

### 7.1 Connect Power BI to PostgreSQL

1. Open Power BI Desktop and choose **Get Data → PostgreSQL database**.

1. Enter your local/hosted server and database (`supply_chain_portfolio`). Use private credentials; do not record the password in the project.

1. Select `supply_chain.order_service`, `supply_chain.order_lines`, `supply_chain.customers`, `supply_chain.products`, and `supply_chain.carriers`. Do not also import the raw `orders` table for this report; the view already has one row per order.

1. Confirm relationship directions and keys. Connect `order_service` (one row per order) to `order_lines` (many rows per order) by `order_id`; connect customer, product, and carrier dimensions through their IDs.

1. Add a page-level or report-level text notice: **Synthetic demonstration — not real business performance.**

If Power BI cannot connect directly in your environment, export query results from `psql` or pgAdmin and state that the dashboard uses static synthetic extracts. Don’t upload a publicly reachable database.

### 7.2 Add basic measures

Use the SQL `order_service` view, or create equivalent DAX measures only after checking the view’s grain and flags. Example measures for the one-row-per-order view:

```
Submitted Orders = DISTINCTCOUNT(order_service[order_id])

Delivered Orders =
CALCULATE(
    DISTINCTCOUNT(order_service[order_id]),
    order_service[order_status] = "delivered"
)

On-Time Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(order_service[order_id]),
        order_service[order_status] = "delivered",
        order_service[is_on_time] = TRUE()
    ),
    [Delivered Orders]
)

In-Full Order Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(order_service[order_id]),
        order_service[order_status] = "delivered",
        order_service[is_in_full] = TRUE()
    ),
    [Delivered Orders]
)

OTIF Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(order_service[order_id]),
        order_service[order_status] = "delivered",
        order_service[is_otif] = TRUE()
    ),
    [Delivered Orders]
)

Cancellation Rate =
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(order_service[order_id]),
        order_service[order_status] = "cancelled"
    ),
    [Submitted Orders]
)
```

For unit fill rate use line-level totals from the line table, restricted to delivered orders, and verify the relationship does not duplicate line rows:

```
Unit Fill Rate =
DIVIDE(
    CALCULATE(SUM(order_lines[delivered_qty]), order_service[order_status] = "delivered"),
    CALCULATE(SUM(order_lines[ordered_qty]), order_service[order_status] = "delivered")
)
```

If Power BI reports a relationship or DAX error, use the SQL query results as the source of truth and adjust the model; don’t change KPI definitions merely to make a chart work.

### 7.3 Lay out three pages

**Page 1 — Fulfillment overview:** synthetic-data notice, submitted/delivered/cancelled order cards, on-time, in-full, OTIF, month trend, market slicer, and eligible order count.

**Page 2 — Diagnostic segments:** on-time by carrier and market, incomplete lines/undelivered units by product/category, and customer segment comparison. Show volume next to rate.

**Page 3 — Data and method (optional):** table grain, KPI definitions, cancellation treatment, data-quality checks, dataset generation seed, and explicit limitations.

Use readable titles and subtitles. Include units and denominator context. Avoid red/green wording that implies a real target or industry benchmark; if you add thresholds for demonstration, label them “illustrative only.”

### 7.4 Validate dashboard totals

Compare each KPI card with the equivalent SQL query for the same filters and date basis. Test market, month, carrier, and customer filters individually. Save one or two screenshots under `dashboard/screenshots/`; each image must visibly state that the data is synthetic. Never include credentials in a screenshot.

**Checkpoint:** dashboard values reconcile with SQL, filter context is clear, and the synthetic limitation appears on every relevant view.

## Phase 8 — Write findings and recommendations without overselling

### 8.1 Record demonstrative patterns accurately

For each query output you choose to discuss, record in a findings log:

- query name and exact filter/date basis;

- segment and numerator/denominator;

- result from the synthetic data;

- a statement that the pattern is programmed/illustrative, not empirical;

- what a real analyst would need to verify before action.

Do not imply a generated segment’s rate was “discovered” as if it came from a real operation. Since the generator intentionally varies groups, say that the project demonstrates whether the pipeline can surface those constructed patterns.

### 8.2 Write a hypothetical operational follow-up

A safe recommendation could be:

> “In a real operation, a similar pattern would justify checking shipment events, inventory availability, and the customer delivery promise before selecting an intervention. These synthetic records do not establish which cause is responsible.”

Do not say to increase inventory or replace a carrier based only on the synthetic data. There is no on-hand stock, supplier, contract, or actual carrier-event evidence.

### 8.3 Don’t calculate fake ROI

Do not estimate cost savings, service improvement, customer retention, or inventory reduction unless you have real, relevant cost and intervention data. This project’s synthetic prices are not business costs. It is completely acceptable to state: “No real-world impact or ROI is measured; this is a technical demonstration.”

**Checkpoint:** all statements distinguish the generated sample from real operational performance.

## Phase 9 — Finish the project documentation

Update these files after you complete each phase:

- `docs/synthetic-data-card.md`: keep generator details, intended use, and limitations current.

- `docs/data-dictionary.md`: record actual schemas, grains, keys, and validation outcomes.

- `docs/metric-definitions.md`: document final formula and display definitions.

- `docs/project-brief.md`: state actual tasks completed and any scope changes.

- `n8n/workflow-plan.md`: if you skip n8n, keep it labeled as an optional, unexecuted reference; update it only if you later build and test that extension.

- `docs/ai-usage-log.md`: record actual AI assistance, edits, and independent checks.

- `README.md`: include a clear project summary, synthetic-data disclosure, status, links, and only completed outputs.

- `docs/limitations.md`: include that the dataset is synthetic, generator-controlled, and lacks inventory history and real costs.

Do not leave placeholders in the portfolio-facing README. Where work is incomplete, state “not yet built” rather than implying it exists.

## Phase 10 — Commit and publish

Before committing, inspect changes and whitespace:

```bash
git status --short
git diff --check
git diff --stat
```

Confirm that data files under `data/synthetic/` are generated by this repository’s script and that invalid fixtures remain outside the clean analytical tables. Make sure no credentials, real customer files, private email, or non-redistributable tutorial files were added.

Commit coherent milestones:

```bash
git add src data docs sql n8n dashboard README.md
git status --short
git commit -m "Add reproducible synthetic fulfillment dataset"
git push
```

The repository is private. Keep it private while unfinished. Before making it public, check the full commit history and screenshots for secrets or private files, and retain the synthetic-data disclosure in the README and dashboard. The generated data itself is intended to be reproducible and shareable with its generator; do not add the third-party tutorial data.

## Phase 11 — Prepare a credible portfolio summary

A concise portfolio description, after you have actually completed the listed analysis, can say:

> “Generated and validated a deterministic synthetic retail order-fulfillment dataset, loaded the relational tables into PostgreSQL, and developed SQL analyses for order-level service KPIs. Independently reconciled selected records to documented metric definitions and used AI to assist with drafting, which I reviewed and verified. All records and patterns are fictional; no real-world performance or impact is claimed.”

Only list tools you actually used. Don’t claim operational results, inventory optimization, or realized impact from the generated records.

For internship applications, this project can demonstrate technical workflow, SQL, KPI logic, and AI validation. Synthetic data is weaker evidence of real business insight than a permitted real dataset. If you later find an openly licensed, redistributable source, add a separate analysis project or a clearly labeled real-data extension; keep this synthetic technical demo as its own reproducible artifact.

## Final checklist

- [ ] Generator runs from the README command and uses the documented seed.

- [ ] Structural validator passes on clean files.

- [ ] Generated data is prominently labeled synthetic in README and dashboard.

- [ ] The original non-redistributable tutorial data is not in Git.

- [ ] SQL uses correct grain, cancellation rules, and currency boundaries.

- [ ] Dashboard totals reconcile to SQL and show denominators.

- [ ] Invalid fixtures are never mixed with analysis data; test an automated rejection branch only if you choose to implement it.

- [ ] AI code and summaries are checked; validations are documented.

- [ ] Recommendations and resume wording do not claim real-world performance or impact.

- [ ] No credentials, private data, or unapproved third-party content is committed.
