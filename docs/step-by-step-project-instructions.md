# Step-by-Step Project Instructions

This manual is for building the project in this repository: **AI-Assisted Supply Chain Order Fulfillment Analysis**. Follow the steps in order. The guide deliberately does not assume the tutorial CSVs contain promised delivery dates, actual delivery dates, delivered quantities, inventory balances, or supplier lead times. You will inspect the real files first and only claim results they support.

## The finished project should demonstrate

By the end, a reviewer should be able to see that you can:

1. Translate a supply-chain scenario into a precise analysis question.
2. Inspect and document unfamiliar data before using it.
3. Build a repeatable data load into a relational database.
4. Write SQL and calculate only defensible KPIs.
5. Use AI to accelerate work while checking its output.
6. Build a clear dashboard and make a proportionate recommendation.
7. Explain project limitations, reproduce the work, and discuss your own decisions.

## Phase 0 — Set up your workspace and define your rules

### Step 0.1: Clone the repository

On a computer with Git installed, open a terminal and run:

```bash
git clone https://github.com/brinda07/supply-chain-fulfillment-ai-portfolio.git
cd supply-chain-fulfillment-ai-portfolio
```

The repository is private. Sign in to GitHub before cloning. If you do not use the terminal, download the repository ZIP from GitHub, extract it, and work in that folder. When you make changes, keep a backup copy or learn the basic commit/push steps near the end of this guide.

### Step 0.2: Keep the project data private until you know the reuse terms

Find the tutorial files through the video description or the creator’s linked source. Record the source URL and download date in `docs/data-dictionary.md`. Read any data-license or reuse notes. Do not upload raw data, private emails, customer information, credentials, or the creator’s paid material to GitHub unless the terms clearly allow redistribution.

Keep local source data under `data/raw/`. The repository ignores files in that folder by default. This allows you to analyze local data without publishing it. If the tutorial offers no downloadable files, do not substitute invented values and present them as measured. First ask the creator/source for the files or select a legitimate, documented dataset and revise the project brief accordingly.

### Step 0.3: Decide the analysis question and keep it narrow

Use this question as the project’s anchor:

> Which markets, products, or customers show the clearest order-fulfillment risk, and what should an operations team investigate first?

Use the video’s fictional business only as a scenario. In your documentation, say the case is based on tutorial-provided data and a fictional scenario unless you independently establish otherwise. Do not say a real company had the issue, that you interviewed real employees, or that a process change was implemented if none of that happened.

### Step 0.4: Complete the project brief

Edit `docs/project-brief.md`. Replace or resolve the open questions after you inspect the files. State:

- the business question;
- the dataset source and what it represents;
- the tools you actually plan to use;
- what is in scope and explicitly out of scope;
- what stakeholders are hypothetical personas versus real interviewees;
- what evidence is still missing.

Avoid setting numeric improvement targets before you have a baseline or a real stakeholder target. Mark the project **tutorial-data / simulated case study** if that is accurate.

**Checkpoint:** Someone unfamiliar with the project can read the brief and tell what question you will answer and what you will not claim.

## Phase 1 — Obtain, inventory, and profile the data

### Step 1.1: Save the untouched files locally

Create the folder if it does not exist:

```bash
mkdir -p data/raw
```

Download the files and place exact, untouched copies in `data/raw/`. Do not change column names or overwrite source values at this point. If you receive ZIP files, keep the original ZIP too, unless its reuse terms prohibit storing it.

### Step 1.2: Make a file inventory

For each file, write down the exact filename, file type, size, source, download date, and what you think one row represents. Then inspect the headers and rows. You can use Excel/LibreOffice or a text editor, but avoid opening a large CSV in a spreadsheet and re-saving it: spreadsheets may silently change IDs, dates, or leading zeroes.

For a quick Python inspection, run this from the repository root:

```bash
python --version
```

If the command is not found, try `python3 --version`. For a first look at every CSV using Python’s standard library, run:

```bash
python - <<'PY'
import csv
from pathlib import Path

for path in sorted(Path('data/raw').glob('*.csv')):
    print(f'\n=== {path.name} ===')
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        print('columns:', reader.fieldnames)
        for i, row in enumerate(reader):
            print(row)
            if i == 2:
                break
PY
```

If the CSV uses a different encoding or delimiter, note what you changed. Never quietly guess at the data. Record the file-level notes and field observations in `docs/data-dictionary.md`.

### Step 1.3: Establish the row grain and keys

For every CSV, answer in writing:

- What exactly does one row represent?
- What field or combination of fields should uniquely identify a row?
- Is that key actually unique?
- Which key links this file to another one?
- Are IDs numeric measurements or identifiers? Treat IDs as text unless there is a reason to do otherwise; an ID such as `000123` must not become `123`.
- Are dates order placement dates, promised delivery dates, shipped dates, or actual delivery dates? Similar-looking dates are not interchangeable.
- Are quantities ordered, shipped, or delivered? Do not assume they mean the same thing.
- Are prices in USD, INR, or another currency? Do not add unlike currencies.

A typical tutorial may have an order-header file (one row per order) and an order-line file (one row per order-product line), but verify this. If one order has several lines, joining headers to lines repeats header attributes. Always account for this when counting orders or summing order-level values.

### Step 1.4: Profile quality before loading

For each file, record:

- number of rows and columns;
- missing values by column;
- duplicate candidate keys;
- distinct counts for IDs and categories;
- invalid or unparsable dates;
- non-numeric quantities or prices;
- negative or zero quantities and whether they represent returns/corrections;
- unexpected currencies, countries, or status values;
- unmatched order, customer, or product IDs across files.

You can do these checks in Python, SQL, or a spreadsheet. Save the method and the actual result, not merely “data checked,” in `docs/data-dictionary.md`. If you clean anything, preserve the untouched raw file and document the rule in a new clean-data step.

**Checkpoint:** You can state the grain, key, date coverage, important fields, and main data-quality caveats for every source file.

## Phase 2 — Decide which metrics the files really support

### Step 2.1: Complete the KPI availability column

Open `docs/metric-definitions.md`. For every proposed metric, mark it **supported**, **not supported**, or **supported with a specific limitation** based on actual fields. Include exact source column names and normalized names.

The minimum useful project can still be good even if OTIF is not available. You can analyze order counts, order-line quantities, product mix, order value (only if defensible), or lead time (only if order and delivery dates exist). State what you can and cannot calculate.

### Step 2.2: Freeze the KPI rules before exploring segment results

For each metric you will use, write down:

- the unit of analysis (line, order, shipment, or customer);
- numerator and denominator;
- included and excluded statuses;
- how missing fields are treated;
- the measurement period and date field;
- whether the result is unit-weighted, line-weighted, or order-weighted;
- how split shipments and returns are handled.

Use these definitions only when fields exist:

- **Unit fill rate:** total delivered units ÷ total ordered units.
- **In-full order rate:** share of eligible orders for which each required line is delivered in full.
- **On-time order rate:** share of eligible orders delivered on or before the agreed promised date.
- **OTIF:** share of eligible orders that satisfy both the on-time and in-full conditions. Calculate at order level, not as a guess from separate rates.
- **Lead time:** actual delivery date minus order date. This measures elapsed time, not whether a promise was met.

An order date does not establish its promised date. If no promised date exists, do not call elapsed lead time an on-time rate. If no delivered quantity exists, do not infer fill rate from ordered quantity. If there is no on-hand inventory history, do not claim to measure stockouts, inventory turnover, safety stock, or reorder points.

### Step 2.3: Fix the analysis cohort

Decide which date defines the month for each analysis (order date, delivery date, or promised date) and why. Decide if incomplete or canceled records are excluded or reported separately. Make sure markets are compared over comparable periods and with the same denominator rules. Write this in the KPI definitions before you build charts.

**Checkpoint:** Each KPI in the proposed dashboard can be traced to fields that actually exist and a written calculation rule.

## Phase 3 — Design and create the database

### Step 3.1: Choose a simple environment

Use a PostgreSQL environment you can access safely. For a beginner, choose either a local PostgreSQL installation or a hosted PostgreSQL service. Keep this project’s development database separate from any personal or work database. Save connection credentials in the service’s credential manager or a local environment file that is excluded by `.gitignore`. Never paste a password into a SQL file, n8n export, Git commit, screenshot, or AI prompt.

If you choose a hosted database, check its current free-tier/retention/security terms yourself; they can change. Do not enable public access to the database just to make the demo work. Use a restricted password and the minimum privileges needed.

### Step 3.2: Create a database and staging tables

Create a database such as `supply_chain_portfolio`. Use separate staging tables that preserve source values as text where practical; typed clean views/tables can follow after validation. Add a `batch_id`, `source_file`, and `loaded_at` to trace each record to its import.

The exact staging columns must be based on the real files. Do not copy a guessed schema from a tutorial. Keep identifiers as `TEXT`. If you use PostgreSQL directly, inspect its `CREATE TABLE` and `COPY` capabilities and load files into staging, then check the counts. Alternatively, build the n8n workflow first and have it insert into the staging tables.

Create a load audit table with one row per input file/batch. At minimum store filename, batch ID, received/loaded timestamp, input row count, accepted row count, rejected row count, and status.

### Step 3.3: Create clean analytical tables or views

After staging data is profiled, standardize names and types in `sql/02_clean_views.sql` (or an equivalent clearly named file). Keep explicit grains:

- `orders`: one row per order, if the header contains one record per order.
- `order_lines`: one row per order-product line, if the file is actually at that grain.
- `customers`: one row per customer if a reference file exists.
- `products`: one row per product if a reference file exists.

If the source has shipment-level details, consider a separate `shipments` table instead of pretending the whole order shipped once. Add primary/foreign keys only after checking that the source supports them. Create a documented mapping from original column names to clean names.

### Step 3.4: Verify the model

Run checks before computing KPIs:

- staging row counts equal source-file row counts;
- each declared unique key is unique, or duplicates are documented;
- each order line joins to an order, or orphan rows are reported;
- each customer/product reference joins where expected;
- no join unexpectedly multiplies header-level order counts or values;
- date and quantity casts do not silently create nulls.

Keep the SQL checks in `sql/` so they can be re-run. Add actual results to the data-quality section in `docs/data-dictionary.md`.

**Checkpoint:** You can rebuild the clean layer from staging, and the row counts and joins reconcile.

## Phase 4 — Build the n8n workflow from a safe first version

The video demonstrates email attachments, but for a portfolio project begin with a manual or file-based trigger. This is easier to reproduce and avoids exposing a personal inbox. If you later want the email automation skill in the portfolio, add it as a separate version using a dedicated test inbox with dummy messages.

### Step 4.1: Create a workflow and name it clearly

In n8n, create a workflow named `Portfolio — Order CSV to PostgreSQL`. Record the n8n version/date if it matters for reproduction. Use the actual n8n interface and node labels available to your account; names may change over time.

### Step 4.2: Add nodes in a controlled sequence

Build the workflow with equivalent nodes for these jobs:

1. **Manual Trigger** — lets you test one known input repeatedly.
2. **Read File / Select File** — obtains one CSV file. If the workflow environment cannot access your local disk, use its supported upload/storage method; do not expose a filesystem path or database publicly.
3. **Set batch metadata** — add a generated batch ID, source filename, and ingestion timestamp.
4. **Switch / IF: identify file type** — route order header, order lines, and reference files to their own mappings. Stop with a clear error on an unknown filename/schema.
5. **Extract/parse CSV** — produce one structured item per row, preserving IDs as text where possible.
6. **Normalize fields** — trim strings, standardize names, parse dates in the documented format, and cast quantities only after validation.
7. **Validate** — check required columns, nonempty keys, valid dates, numeric ranges, allowed categories/currencies, and duplicate keys. Route invalid rows to a rejection branch; do not silently discard them.
8. **Insert to PostgreSQL staging** — use parameterized database operations or the supported PostgreSQL node; never concatenate untrusted CSV text into SQL strings.
9. **Write load audit** — record counts, batch ID, and success/failure. Ensure input rows reconcile to accepted plus rejected rows.
10. **Error branch** — preserve useful error details without logging credentials or private values.

Use one workflow per file type if that is simpler to understand than a complicated router. Use consistent batch IDs when several related files belong to one load.

### Step 4.3: Test failure and rerun behavior

Test at least these cases:

- one valid file;
- a file with a missing required column;
- one invalid date or quantity;
- a duplicate key;
- an unknown filename;
- the same file loaded twice;
- a database connection/load failure.

For each case, verify what the workflow accepts, rejects, records in the audit log, and displays as an error. Loading the same batch again must not silently double records. Use a file hash/batch identifier or a staging-and-merge design to make reruns safe.

### Step 4.4: Export safely

Save a workflow export under `n8n/` only after removing credentials, email addresses, private URLs/hostnames, and other sensitive settings. Re-open the exported JSON as text and search for terms such as `password`, `token`, `secret`, and your email address. Keep any actual n8n credentials in the n8n credential store, not in Git.

**Checkpoint:** You can show a valid run and a rejected/error run, with clear audit counts and no duplicate records after a deliberate rerun.

## Phase 5 — Write SQL and validate the numbers

### Step 5.1: Put all business logic in version control

Write the data cleaning, joins, and KPI logic as named SQL files under `sql/`. The dashboard or AI spreadsheet can use the SQL output, but should not be the only place the formulas exist. Add a short comment above each query stating its grain and assumptions.

### Step 5.2: Build order-level measures at order grain

If order-line data is joined to order-header data, first classify or aggregate line facts per order. Do not count a header once per line. Do not assess “in full” by comparing only total delivered units with total ordered units when a shortage on one SKU could be offset by an over-delivery on another. Prefer checking each line against its ordered quantity and then combining the line results at order level.

A conceptual order-level SQL pattern, **only if the normalized source really has these fields**, is:

```sql
-- clean_orders: one row per order, with market, promised_date, actual_delivery_date
-- clean_order_lines: one row per order-product line, with ordered_qty, delivered_qty
WITH line_status AS (
    SELECT
        order_id,
        product_id,
        ordered_qty,
        delivered_qty,
        CASE
            WHEN ordered_qty IS NOT NULL AND delivered_qty IS NOT NULL
             AND delivered_qty >= ordered_qty THEN TRUE
            ELSE FALSE
        END AS line_in_full
    FROM clean_order_lines
),
order_status AS (
    SELECT
        order_id,
        BOOL_AND(line_in_full) AS order_in_full
    FROM line_status
    GROUP BY order_id
),
orders_assessed AS (
    SELECT
        o.order_id,
        o.market,
        o.promised_date,
        o.actual_delivery_date,
        s.order_in_full,
        CASE
            WHEN o.promised_date IS NOT NULL
             AND o.actual_delivery_date IS NOT NULL
            THEN o.actual_delivery_date <= o.promised_date
            ELSE NULL
        END AS order_on_time
    FROM clean_orders AS o
    JOIN order_status AS s USING (order_id)
)
SELECT
    market,
    COUNT(*) FILTER (WHERE order_on_time IS NOT NULL AND order_in_full IS NOT NULL)
        AS assessable_orders,
    AVG(order_on_time::int) FILTER (
        WHERE order_on_time IS NOT NULL AND order_in_full IS NOT NULL
    ) AS on_time_rate,
    AVG(order_in_full::int) FILTER (
        WHERE order_on_time IS NOT NULL AND order_in_full IS NOT NULL
    ) AS in_full_rate,
    AVG((order_on_time AND order_in_full)::int) FILTER (
        WHERE order_on_time IS NOT NULL AND order_in_full IS NOT NULL
    ) AS otif_rate
FROM orders_assessed
GROUP BY market;
```

This is a pattern, not a drop-in query. Adapt names, exclusions, and the denominator to the dataset. Confirm that all lines for each order are present. If an order can ship in multiple shipments, the rule for actual delivery must reflect the agreed customer definition—often completion of the final required line, but only shipment-level records can establish that. Do not run this if promised date, actual delivery date, or delivered quantity is missing. Record OTIF as **not measurable from available fields** instead.

### Step 5.3: Produce at least three useful analyses

Choose based on the fields available:

1. **Trend:** supported service KPI by month and market.
2. **Segment drivers:** incomplete orders/units by product or customer, if the fields exist.
3. **Prioritization:** compare both rate and impact volume so a tiny denominator does not dominate the story.

For each query, save the SQL, result export or screenshot (without sensitive data), and one sentence describing what decision the result could inform. If the analysis has no delivery status, switch to supported descriptive questions rather than inventing a service KPI.

### Step 5.4: Independently verify

Choose several orders from different categories and trace them from raw records → clean records → SQL classification. Calculate their status manually in a spreadsheet or small Python snippet. Compare totals with a second query or independently grouped calculation. Investigate every disagreement.

Test the following invariants where relevant:

- percentages are between 0 and 1;
- OTIF cannot exceed on-time or in-full rates when calculated with the same assessable-order denominator;
- accepted plus rejected rows equal input rows;
- no order is counted multiple times because of line joins;
- unlike currencies are not combined;
- missing promise dates are not silently counted as on-time or late.

Keep the validation method and result in `tests/` or in the documentation. Never report a metric only because an AI tool produced a plausible-looking number.

**Checkpoint:** Every published KPI is reproducible from a version-controlled query and has at least one independent validation check.

## Phase 6 — Use AI as an auditable assistant

### Step 6.1: Use bounded prompts

Give the model a schema, the KPI definition, and a small task. Ask it to list missing fields and assumptions before generating code. Do not give it private credentials, customer personal data, private email contents, or unrestricted database access.

Example prompt:

> Use only the table and column names below. First identify missing fields needed for the requested KPI. If the KPI cannot be calculated, say so and do not invent substitutes. Draft SQL to calculate [supported metric] by [dimension] at [grain]. State the denominator and exclusions. Include a query that returns example rows so I can manually validate the classifications.

### Step 6.2: Keep the evidence

For each significant AI-assisted task, record in `docs/ai-usage-log.md`:

- date and tool;
- task and prompt summary;
- what output the tool produced;
- exactly what you changed;
- how you validated it;
- whether you accepted or rejected its suggestions;
- any privacy or data-use concern.

Save the final checked query/code in the repository. Don’t paste an entire model chat log if it contains secrets, private data, or irrelevant personal content.

### Step 6.3: Make AI contribution visible without overselling it

A strong portfolio example is: “AI drafted a query; I corrected the grain and exclusion logic, then checked it against a second calculation and manually reviewed sample orders.” Only say this if that is what you did. A prompt screenshot alone does not demonstrate that the result is correct.

**Checkpoint:** A reviewer can tell which parts AI assisted with, what decisions you made, and how you checked the output.

## Phase 7 — Build the dashboard and story

### Step 7.1: Sketch before building

On paper or in a simple wireframe, decide the audience and the first question the dashboard should answer. Keep it to two or three pages:

1. **Overview:** order count and supported KPIs, trend over time, market filter, and the period/data-coverage note.
2. **Where to investigate:** ranked products/customers/markets by failure count and affected volume, if supported.
3. **Data quality (optional):** missing/invalid rows, rejected rows, and KPI availability notes.

Do not create cards for metrics the data cannot support. If the dataset contains only order headers and no outcome fields, make an exploratory order profile rather than a fake fulfillment scorecard.

### Step 7.2: Design for clear interpretation

- Put metric names, units, period, and denominator near the visual.
- Label currencies and keep currencies separate.
- Show the number of eligible observations alongside a percentage.
- Avoid overemphasizing a segment with very few orders; provide a volume context.
- Use consistent date filters and label which date controls each trend.
- Put definitions in a tooltip, subtitle, or linked KPI page.
- Do not imply that association is proof of causation.

### Step 7.3: Reconcile dashboard totals

Compare every dashboard card to the SQL output for the same filters and period. Test slicers one at a time. Add the dashboard source file, screenshots, or safe share link under `dashboard/`; do not publish data or a link that reveals private database credentials.

**Checkpoint:** Dashboard totals reconcile to SQL, and a reader can understand each metric without relying on a verbal explanation.

## Phase 8 — Convert analysis into a recommendation

### Step 8.1: Keep a findings log

For every finding, record:

- finding ID;
- plain-language statement;
- exact query/KPI/chart that supports it;
- how large the affected group is;
- confidence and limitation;
- what action it suggests investigating.

Example structure (do not copy as a result): “During [period], [segment] had [measured result] across [N] eligible orders. This suggests [carefully stated operational question], but the available fields do not establish [cause].”

### Step 8.2: Make one prioritized recommendation

Choose an action that matches the evidence and can be tested. If a product appears frequently on incomplete orders, recommend reviewing stock/replenishment records for that product—not automatically increasing safety stock. If on-time performance is low but you lack shipment/carrier/supplier data, recommend investigating the missing process records rather than blaming the carrier.

For each recommendation, state owner role (proposed if fictional), next step, effort/risk if known, and a measure that could validate the intervention. Clearly distinguish a proposal from a measured business outcome.

### Step 8.3: Do not invent ROI

Only calculate potential savings if the dataset contains suitable cost data and you can show the assumptions and calculation. Otherwise mark cost/benefit or ROI **not estimated due to missing evidence**. Do not translate an improvement target into actual savings.

**Checkpoint:** Every recommendation points to a finding, and every finding points to evidence.

## Phase 9 — Finish the documentation pack

Complete the project documentation in this order:

1. `docs/data-dictionary.md`: provenance, files, grain, fields, keys, quality findings, reuse terms.
2. `docs/metric-definitions.md`: supported metrics, exact formulas, exclusions, denominator and limits.
3. `docs/project-brief.md`: final scope and actual tools/work completed.
4. `n8n/workflow-plan.md`: update with actual nodes, parameters at a high level, test results, and limitations; include a safe exported workflow if possible.
5. `sql/`: actual staging, cleaning, KPI, and validation queries, not only templates.
6. `docs/ai-usage-log.md`: actual AI-assisted tasks and validation details.
7. `docs/limitations.md`: create this file and list data gaps, sample-data status, scope boundaries, and work not completed.
8. Root `README.md`: write the final short version, including a dashboard image, 2–3 verified findings, setup steps, and links to technical documentation.

Do not leave unresolved `[TBD]` or `[placeholder]` fields in the public-facing sections. If something cannot be resolved, replace the placeholder with a clear statement such as “not available in the supplied files.”

## Phase 10 — Test, commit, and publish

### Step 10.1: Final privacy and accuracy check

Before pushing, review the staged changes and search for sensitive information:

```bash
git status --short
git diff --check
git diff --cached --stat
git grep -n -i -E 'password|token|secret|api_key|private key' -- ':!docs/reference/*.docx'
```

Also inspect the n8n JSON and screenshots manually. Check there are no real email contents, private customer details, credentials, database URLs with secrets, or raw files whose license disallows sharing. `.gitignore` excludes raw tutorial files by default; do not override it casually.

### Step 10.2: Commit in understandable units

From the repository root:

```bash
git add docs sql n8n src tests dashboard README.md
git status --short
git commit -m "Document order fulfillment analysis"
git push
```

Only run the commit after reviewing what is staged. Use later commits for meaningful milestones, such as `Add validated fulfillment KPI queries` or `Add dashboard and findings`.

### Step 10.3: Decide when to make the repository public

The repository starts private. Keep it private while it contains unfinished work or material with uncertain reuse permissions. Before making it public, inspect repository settings, licenses, file provenance, workflow exports, screenshots, commit history, and all project claims. Do not make it public merely because the dashboard is finished if you cannot redistribute the data.

## Phase 11 — Prepare the portfolio case study and interview explanation

Write the public summary only after the results are verified. A good case study tells this story in a few minutes:

1. **Context:** tutorial/simulated scenario and business question.
2. **Your approach:** profiling, data model, workflow, SQL, and dashboard.
3. **One or two validated findings:** include the denominator and timeframe.
4. **Your recommendation:** next investigation or pilot, not an unsupported promise.
5. **AI judgment:** what AI drafted, what you corrected, and how you validated it.
6. **Limitations:** fields unavailable and why this is fulfillment analysis rather than a proven inventory optimization.
7. **Reproduction:** where code and setup instructions live.

Resume bullet template—fill only with verified values:

> Built an AI-assisted order-fulfillment analysis using [actual tools], profiled [N] [orders/order lines] from tutorial-provided data, validated [supported KPI], and identified [specific measured pattern] for [proposed operational follow-up].

Do not write “[improved service by X%]” unless you implemented a change and measured the before/after result under a defensible evaluation design. For a portfolio analysis, say “identified,” “analyzed,” or “recommended,” not “delivered savings” or “optimized inventory.”

## Suggested build calendar

A realistic schedule for a focused project is:

- **Session 1:** clone repo, acquire files, document provenance and project scope.
- **Session 2:** profile files, establish grain/keys, complete the data dictionary.
- **Session 3:** set metric availability and definitions; create PostgreSQL staging/clean layer.
- **Session 4:** build n8n intake and test valid/invalid/duplicate files.
- **Session 5:** write SQL analyses and independently validate key totals.
- **Session 6:** build dashboard, write findings, decide a careful recommendation.
- **Session 7:** complete AI log, README, privacy review, demo recording, and final push.

The schedule is a planning aid, not a promise that each session will take a fixed number of hours. Data-access or field gaps may require a narrower analysis.

## Final completion checklist

- [ ] The project is accurately labeled as tutorial-data, simulated, academic, or real.
- [ ] Source provenance and file reuse terms are documented.
- [ ] The grain and keys of all files are explained.
- [ ] No KPI is reported without all necessary fields and a documented rule.
- [ ] Order-level calculations are not multiplied by line-level joins.
- [ ] Data-load counts reconcile; invalid and duplicate records are handled explicitly.
- [ ] AI-generated code and summaries were checked and the check is recorded.
- [ ] Dashboard values reconcile to SQL and show denominators/units.
- [ ] Findings link to evidence; recommendations do not claim unsupported causes.
- [ ] No unrealized savings, implementation, or service improvement is claimed.
- [ ] No credentials, private data, or prohibited raw files are committed.
- [ ] README and setup instructions let a reviewer understand the project.
