# Database Setup

## Environment

- PostgreSQL 18
- pgAdmin 4

## Database

Database Name:

```text
supply_chain_portfolio
```

Schema:

```text
supply_chain
```

## Setup Steps

1. Generated synthetic datasets using:

```bash
python src/generate_synthetic_dataset.py
```

2. Validated generated datasets using:

```bash
python src/validate_synthetic_dataset.py
```

3. Created PostgreSQL database:

```text
supply_chain_portfolio
```

4. Executed:

```text
sql/01_create_tables.sql
```

5. Imported CSV files:

- customers.csv
- products.csv
- carriers.csv
- orders.csv
- order_lines.csv

6. Executed:

```text
sql/02_quality_checks.sql
```

## Table Load Order

1. customers
2. products
3. carriers
4. orders
5. order_lines

## Validation

Quality checks completed successfully after data import.

## Credentials

Database credentials are stored locally and are not committed to the repository.

Passwords, connection strings, .env files, and private connection URLs are excluded from source control.
