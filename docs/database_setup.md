# Database and Power BI Implementation Record

This file records the implementation record and provides a reproducibility reference. Do not commit database passwords or connection strings.

## Environment

- PostgreSQL 18
- pgAdmin 4
- Power BI Desktop

## Database

- **Database:** `supply_chain_portfolio`
- **Schema:** `supply_chain`


## Completed data and SQL workflow

1. Generated the synthetic tables:

   ```bash
   python3 src/generate_synthetic_dataset.py
   ```

2. Ran structural validation:

   ```bash
   python3 src/validate_synthetic_dataset.py
   ```

3. Created the database and ran `sql/01_create_tables.sql`.
4. Imported the CSVs manually in foreign-key order:
   - `customers.csv`
   - `products.csv`
   - `carriers.csv`
   - `orders.csv`
   - `order_lines.csv`
5. Executed the remaining SQL files:
   - `sql/02_quality_checks.sql`
   - `sql/03_fulfillment_kpis.sql`
   - `sql/04_segment_diagnostics.sql`
   - `sql/05_dashboard_views.sql`
6. Created the five analytical tables (`customers`, `products`, `carriers`, `orders`, `order_lines`), the `load_audit` support table, and the `order_service` view.
7. Manually validated `ORD-000001` and `ORD-000036` for on-time, in-full, OTIF, and cancellation treatment. See [`../tests/manual-kpi-validation.md`](../tests/manual-kpi-validation.md).

### CSV load order

1. `customers`
2. `products`
3. `carriers`
4. `orders`
5. `order_lines`

The first three tables are referenced by later order records; order lines depend on both orders and products.

## Completed Power BI work

The author connected Power BI to PostgreSQL and imported:

- `supply_chain.order_service`
- `supply_chain.order_lines`
- `supply_chain.customers`
- `supply_chain.products`
- `supply_chain.carriers`

The author built the relationship model, these measures—Submitted Orders, Delivered Orders, On-Time Rate, In-Full Order Rate, OTIF Rate, Cancellation Rate, and Unit Fill Rate—and three pages: Fulfillment Overview, Diagnostic Segments, and Data & Methodology.

The `.pbix` file and screenshots have not yet been added to this repository. See [`../dashboard/README.md`](../dashboard/README.md) for the exact filenames and publication checks.

## Important implementation boundary

CSV loading was manual. n8n and other automation were not implemented. The `load_audit` table exists in the schema, but its existence does not mean an automated workflow populated it or monitored loads.

## Credentials

Database credentials are stored locally and are not committed to the repository. Passwords, connection strings, `.env` files, and private connection URLs must remain outside source control.
