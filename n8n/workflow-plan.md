# n8n Workflow Plan — Synthetic Dataset

The input is generated locally by `src/generate_synthetic_dataset.py`. Use the clean files in `data/synthetic/` for the normal successful load. Use `data/fixtures/` only to test rejection and error handling. Do not use the original tutorial’s non-redistributable files.

## Tables and load order

Load dimensions before facts to respect the SQL foreign keys:

1. `customers.csv` → `supply_chain.customers`
2. `products.csv` → `supply_chain.products`
3. `carriers.csv` → `supply_chain.carriers`
4. `orders.csv` → `supply_chain.orders`
5. `order_lines.csv` → `supply_chain.order_lines`

Use a manual trigger and one test file per run. A folder-trigger version is optional. n8n Cloud may not be able to read a path on your laptop; use a supported upload/cloud-storage route or run a local/self-hosted n8n instance with a permitted shared folder. Do not expose a local database or filesystem to the public internet to make a demo work.

## Node responsibilities

1. **Manual Trigger** — run one known file.
2. **Read/upload file** — obtain the CSV in the n8n runtime.
3. **Set metadata** — record `batch_id`, `source_file`, and load start time.
4. **Route by expected filename** — map the five known files to their exact destination table. Stop on unknown file/table combinations.
5. **Extract/parse CSV** — create structured row items without converting identifier strings to numbers.
6. **Validate** — required headers, nonblank primary key, allowed market/currency, valid ISO date, valid integer quantities, valid foreign keys, and unique keys. The validation fixtures are designed to exercise common failures.
7. **Insert into PostgreSQL** — use parameterized values and the schema in `sql/01_create_tables.sql`. Do not build SQL by concatenating raw CSV text.
8. **Write `load_audit`** — record input/accepted/rejected counts and final status; preserve an error summary if a load fails.
9. **Error path** — route rejected rows to a diagnostic output. Do not silently drop them or claim a failed load succeeded.

## Idempotency and order of operation

Use a unique batch ID and define duplicate-file behavior. For this small project, either reject a batch whose source hash has already succeeded, or load into staging and merge with conflict handling. Document the chosen rule. Do not simply re-run inserts into primary-key tables and hide conflicts.

## Test plan

- Load all clean data files in the order above and reconcile accepted rows with the CSV counts.
- Run the same file twice and show that it does not duplicate records.
- Run `orders_validation_fixture.csv` and confirm duplicate ID, blank ID, malformed date, unsupported market, and unsupported currency are rejected.
- Run `order_lines_validation_fixture.csv` and confirm duplicate line, orphan order, negative quantity, and non-integer quantity are rejected.
- Test a database connection failure and make the workflow display failure.

Export a credential-redacted workflow after implementation. Check the JSON and screenshots for passwords, tokens, email addresses, database URLs, and personal data before committing. This workflow demonstrates ETL reliability on synthetic data; it is not a real production supply-chain integration.
