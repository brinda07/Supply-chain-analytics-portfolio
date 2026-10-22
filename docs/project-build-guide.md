# Supply Chain Analyst Portfolio Project: Fulfillment Performance & AI-Assisted Analysis

## Is this a good video to use?

**Yes—as a starting template, not as the finished portfolio project.** It gives you a coherent business scenario, a simple end-to-end data flow (CSV/email → n8n → PostgreSQL → AI-assisted spreadsheet), and supply-chain questions such as monthly service performance and customer fulfillment. It is useful for demonstrating workflow automation and AI-assisted analysis.

If you reproduce it step for step, however, the portfolio may look like a tutorial copy. The stronger version shows that you can define metrics correctly, inspect messy data, validate AI-generated work, and turn results into a careful operational recommendation. Treat AI as a copilot, not the source of truth. The video itself stresses that supply-chain and analysis fundamentals still matter. It covers order-level and order-line data for two markets and illustrates monthly performance and customer comparisons. [1]

## Project brief

**Title:** *Can We Fulfill Orders Reliably as We Expand? An AI-Assisted Supply Chain Analysis*

**Business scenario:** A small food retailer has grown into two markets. Operations leaders want to know where customer orders are not being fulfilled reliably before expanding further.

**Primary question:** Which market, product, customer, or month shows the clearest fulfillment risk, and what should the operations team investigate first?

**Scope:** Analyze the tutorial’s order-header and order-line files, plus product/customer reference files if they are supplied. Clearly label the files as tutorial-provided data. Do not describe the results as real company performance unless the data source establishes that.

**Important scope check:** An order file is not automatically an inventory dataset. If it lacks inventory-on-hand snapshots, stockout events, replenishment quantities, or supplier lead times, you can analyze order fulfillment but you cannot calculate a defensible reorder point or prove that inventory caused a shortfall. Make that limitation visible rather than filling it with assumptions.

## Choose a focused tool stack

Use the video’s stack where it helps, but keep the number of tools manageable:

- **n8n** for repeatable file intake and load logging.
- **PostgreSQL** for staging, clean tables, and KPI queries.
- **Python** for data-quality checks and a small independent calculation check; pandas is enough.
- **One dashboard tool**—Power BI, Tableau, or Metabase—for the final visuals. Quadratic can be your AI-assisted spreadsheet layer if you want to follow the video closely, but do not make it the only place where KPI logic lives.
- **An AI assistant** to draft SQL/Python, suggest checks, and summarize results. Record what it generated and how you verified it.

n8n has a CSV-to-PostgreSQL example that illustrates the basic import pattern. Adapt it to your actual files and add the validation, deduplication, and logging below; the template is a starting point, not a complete production ingestion design. [2]

## Build it in this order

### 1. Download and inspect the files

Get the sample files from the video description if they remain available. Save untouched files under `data/raw/`. Do not rename or edit the originals. Create `data/README.md` with the file names, where you obtained them, the date you downloaded them, and any reuse restrictions you can establish.

For each file, record:

- What one row represents (for example, one order or one order line).
- The columns, data types, null count, and distinct count.
- The likely primary key and the fields used to join it to other files.
- Whether dates, quantities, prices, and currencies are present.

Use a short Python inspection script or notebook. Check duplicate keys, missing IDs, invalid dates, negative quantities, unexpected currency codes, and whether every order line has a matching order header. Do not assume a column exists because a tutorial narrator mentioned it—verify it in the downloaded file.

### 2. Write down your metric rules before analysis

Make a `docs/metric_definitions.md` and decide the denominator and exclusions for every KPI. Recommended definitions:

- **Orders:** distinct valid order IDs, excluding cancelled orders only if a cancellation status is available and you state the rule.
- **Unit fill rate:** total delivered units ÷ total ordered units. Use only if both ordered and delivered quantities are present and comparable.
- **In-full order rate:** valid orders where delivered quantity is at least ordered quantity for every order line ÷ valid orders with delivery data.
- **On-time order rate:** orders delivered on or before the promised date ÷ valid orders with both promised and actual delivery dates.
- **OTIF:** orders that meet both the on-time and in-full conditions ÷ valid orders with the fields needed to assess both conditions. Calculate the share of orders satisfying both conditions directly. OTIF combines timeliness and completeness; a late complete order and an on-time incomplete order both fail OTIF. [3]
- **Order value:** calculate only if unit price and currency are available. Show India and US values separately unless you specify and document a valid currency conversion method. Never add INR and USD as if they were the same unit.

If the files do not support one of these measures, mark it **not measurable from the available fields**. In particular, order date by itself is not a promised delivery date; an order date is not enough to claim an on-time rate.

### 3. Design a small, understandable database

Create raw landing tables first. Keep the source data intact so that you can audit how it entered the project. Then build clean tables or views whose grain is explicit:

- `orders`: one row per order; market, customer ID, order date, and any promised/actual delivery or status fields that truly exist.
- `order_lines`: one row per order-product line; order ID, product ID, ordered quantity, delivered quantity if supplied, unit price if supplied, and currency if supplied.
- `customers`: one row per customer, if the sample includes customer attributes.
- `products`: one row per product, if the sample includes product attributes.
- `load_audit`: file name, batch ID, received/loaded timestamp, row counts, rejected-row count, and load status.

Document primary keys and foreign keys. Keep order-level calculations at order grain. Do not join an order header to several order lines and then sum header-level order value or order counts; that duplicates header values. Aggregate line data to order level first when you need to combine the grains.

### 4. Build the n8n intake workflow

For a first version, use a manual trigger and select or place the sample CSVs in a known folder. That makes your demo reproducible and avoids connecting a personal mailbox. If you want to demonstrate the video’s email-triggered flow, use a dedicated test inbox, not your personal inbox, and do not include credentials or private mail in your portfolio.

Create a workflow with these stages:

1. **Trigger:** manual run for the portfolio demo; optionally add a dedicated-inbox email trigger as a second workflow version.
2. **Identify files:** route order headers, order lines, and reference files by filename or an explicit mapping. Fail clearly on an unknown file.
3. **Parse CSV:** read the header row and convert each record into structured fields.
4. **Normalize:** trim whitespace; standardize column names; parse dates and numeric quantities; attach market, source filename, batch ID, and ingestion time.
5. **Validate:** check required columns, valid dates, numeric quantities, duplicate keys, and allowed currency codes. Send invalid rows to a rejected-record output rather than silently dropping them.
6. **Load safely:** insert into staging tables. Make reruns idempotent by recording a file hash/batch ID and preventing duplicate inserts for the same source batch.
7. **Log and alert:** write input rows, accepted rows, rejected rows, and status to `load_audit`; make a failed run visibly fail rather than report success.

Export the n8n workflow JSON for the repository only after removing credentials, personal email addresses, and private connection details. Put connection instructions in the README; never commit passwords, tokens, or `.env` files.

### 5. Create a clean analytical layer

Write SQL views or scripts in `sql/` to standardize types, expose understandable names, and join facts to dimensions. Keep staging separate from clean data. Save all KPI logic in version-controlled SQL even if you also recreate a calculation in Quadratic or another AI spreadsheet.

For OTIF, create one row per order before calculating the percentage. In outline:

```sql
WITH order_level AS (
  SELECT
    order_id,
    market,
    MIN(promised_date) AS promised_date,
    MAX(actual_delivery_date) AS actual_delivery_date,
    SUM(ordered_qty) AS ordered_units,
    SUM(delivered_qty) AS delivered_units
  FROM clean_order_lines
  GROUP BY order_id, market
)
SELECT
  market,
  COUNT(*) AS assessable_orders,
  AVG(CASE WHEN actual_delivery_date <= promised_date
           THEN 1.0 ELSE 0.0 END) AS on_time_rate,
  AVG(CASE WHEN delivered_units >= ordered_units
           THEN 1.0 ELSE 0.0 END) AS in_full_rate,
  AVG(CASE WHEN actual_delivery_date <= promised_date
                AND delivered_units >= ordered_units
           THEN 1.0 ELSE 0.0 END) AS otif_rate
FROM order_level
WHERE promised_date IS NOT NULL
  AND actual_delivery_date IS NOT NULL
GROUP BY market;
```

This is a **template, not drop-in SQL**: replace names to match the files and confirm that delivery dates and quantities have the right meaning. If orders can ship in multiple shipments, a single `MAX(actual_delivery_date)` and a total delivered quantity may not represent the customer’s agreed delivery rule; document the rule or use shipment-level data. Add the required `in_full` field to the filter or calculate it separately if delivered quantity is missing. Never turn missing dates into on-time failures without declaring that treatment.

### 6. Answer three questions, then make one recommendation

Keep the analysis small enough to explain clearly:

1. **Where is service weakest?** Compare monthly on-time, in-full, and OTIF results by market, using consistent definitions and denominators.
2. **Which products or customers contribute most to incomplete orders?** Rank by incomplete order count and affected units, not only by the lowest percentage; a low-volume product may have a dramatic rate but little operational impact.
3. **Is the pattern changing?** Look for a persistent trend or a specific month/market/product combination that merits follow-up. Do not claim a cause that the data does not contain.

Then write one recommendation that is proportional to the evidence. For example: “Prioritize a review of product X in market Y because it appears repeatedly on incomplete orders; check stock and replenishment records before changing safety stock.” Avoid saying “increase inventory” unless you have inventory and replenishment evidence to support it.

### 7. Add AI in a way you can defend in an interview

Demonstrate AI use in a short, auditable loop:

1. Give the AI a schema and your written KPI definitions. Ask it to draft one SQL query or Python check for a specific question.
2. Review the generated query. Confirm joins, filters, aggregation grain, date logic, denominators, and currency handling.
3. Run it against your clean tables. Compare the result with a second, independently written calculation (for example, a separate SQL query or a small Python check).
4. Manually verify several orders from raw rows through to the KPI classification. Record one error or ambiguity you found and how you fixed it.
5. Use AI to draft a plain-language summary from the validated results. Edit it so every statement is supported by a chart or query and the caveats are clear.

Example prompt to save in `docs/ai_prompt_log.md`:

> You are helping with an order-fulfillment analysis. Use only the schema and metric definitions below. Draft a SQL query that calculates OTIF by market and month at one row per order. Do not invent columns. List assumptions and missing fields before writing the query. OTIF means the order is both delivered on or before its promised date and delivered in full. Include a short validation query that lets me inspect individual order classifications. Do not claim inventory caused a failure unless the data contains inventory evidence.

Keep the prompt, generated draft, final query, and validation notes together. This is stronger evidence of AI skill than a screenshot of a prompt: it shows you can constrain the model, evaluate its output, and catch errors.

### 8. Build a focused dashboard

Use three pages at most:

- **Overview:** KPI cards for order count and the supported service metrics; monthly trend; market filter; note on data coverage.
- **Fulfillment drivers:** incomplete-order count and affected units by product/customer; ranked bars or a Pareto-style view; market and month filters.
- **Data quality:** file-load history, accepted/rejected rows, missing/invalid fields, and a note showing which KPIs are unavailable if required fields are absent.

Label chart units and denominators. Avoid decorative visuals, unexplained red/green thresholds, and mixing currencies. Put a short definition tooltip or subtitle beside OTIF and fill rate so a reviewer can understand your calculation without guessing.

### 9. Test it before you publish

Make a `tests/` checklist or small test script. At minimum, verify:

- Every clean order line maps to an order; duplicate keys are reported.
- Total rows in staging reconcile to accepted plus rejected rows in the load log.
- Ordered and delivered units are nonnegative, unless a return/credit convention is documented.
- KPI percentages are between 0 and 1 (or 0% and 100%).
- OTIF never exceeds either on-time rate or in-full rate for the same denominator.
- A small set of manually checked orders matches the SQL classification.
- Rerunning the same file does not double the loaded records.
- The market and currency filters do not combine unlike monetary units.

Save the results of the tests or include how to run them in the README.

## Suggested repository layout

```text
supply-chain-otif-project/
├── README.md
├── data/
│   ├── README.md              # provenance and reuse notes; no private data
│   └── raw/                   # tutorial sample files, only if redistribution is permitted
├── docs/
│   ├── business_brief.md
│   ├── data_dictionary.md
│   ├── metric_definitions.md
│   ├── ai_prompt_log.md
│   └── limitations.md
├── n8n/
│   └── csv_to_postgres_redacted.json
├── sql/
│   ├── 01_create_staging.sql
│   ├── 02_clean_views.sql
│   └── 03_kpis.sql
├── src/
│   └── validate_data.py
├── tests/
│   └── test_kpis.py
└── dashboard/
    └── screenshots/           # or a link to the published dashboard
```

If the tutorial data cannot be redistributed, do not upload it. Keep instructions for obtaining it, provide schema/sample rows that you are permitted to share, and make the code reproducible when a reviewer supplies the files.

## What to publish

Your README should open with the business question, include a dashboard image, summarize two or three **real findings from your run**, explain the pipeline, define the KPIs, list setup steps, and state limitations. Add an architecture diagram showing file intake → validation/staging → clean SQL layer → analysis/dashboard, with the AI assistant marked as a copilot rather than an authoritative data source.

Record a 2–3 minute screen demo: explain the business question, show one validated KPI and the segment that matters, demonstrate one AI-generated query and the check you used, then show how a bad file or repeated file is handled. A reviewer should be able to understand your project without watching the original tutorial.

## One-week build schedule

- **Day 1:** Download/inspect files, create the brief, data dictionary, and metric definitions.
- **Day 2:** Create PostgreSQL staging and clean tables; load the files once manually and reconcile row counts.
- **Day 3:** Build and test the n8n workflow, including bad-file and duplicate-file behavior.
- **Day 4:** Write KPI SQL and independently verify it with Python or hand-checked orders.
- **Day 5:** Build the dashboard and investigate the three questions.
- **Day 6:** Add AI prompt/evaluation evidence, finish the recommendation and limitations.
- **Day 7:** Write the README, record the demo, remove secrets, and check that setup instructions work from a clean environment.

## Résumé wording

Use a result-based bullet only after you have run the analysis. For example:

> Built an AI-assisted supply-chain fulfillment analysis using n8n, PostgreSQL, Python, and **[dashboard tool]**; validated **[N]** tutorial-provided orders and identified **[specific, measured pattern]** by market/product using **[supported KPI]**.

Replace every bracket with a verified result. If the data cannot support OTIF, say “order fulfillment analysis” and name the measures it does support instead.

## References

[1]: https://www.youtube.com/watch?v=PglKAYgRdJ4 "Video supplied by the user: AI-assisted supply-chain analytics workflow"
[2]: https://n8n.io/workflows/2926-import-csv-files-from-filesystem-into-postgres/ "n8n community example for importing CSV files into PostgreSQL"
[3]: https://www.doss.com/resources/glossary/on-time-in-full-otif "DOSS glossary: On-Time In-Full definition and calculation"
