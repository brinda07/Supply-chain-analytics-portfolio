# Data Inventory and Dictionary

> Populate this from the files themselves. The video mentions example identifiers and quantities, but the field names, formats, meanings, and availability must be verified against the downloaded files.

## Source register

| File | Source / URL | Date obtained | License / reuse terms | Row grain | Rows | Notes |
|---|---|---|---|---|---:|---|
| TBD | Tutorial source, if available | TBD | TBD | TBD | TBD | Do not publish raw file until redistribution rights are clear. |

## File-level profile

For each source, record filename, encoding, delimiter, header row, date coverage, row count, duplicate-key count, and whether it contains personal or sensitive information.

## Field dictionary

| Source file | Actual column name | Normalized name | Meaning | Type / format | Nulls | Key / rule | KPI use |
|---|---|---|---|---|---:|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## Relationship map

- Order header ↔ order line: verify the actual order key and whether it is unique in the header file.
- Order line ↔ product: verify product key and referential integrity if a product file exists.
- Order header ↔ customer: verify customer key and referential integrity if a customer file exists.

## Data-quality results

| Check | Method | Result | Decision / limitation |
|---|---|---|---|
| Missing required fields | Null count by field | TBD | TBD |
| Duplicate keys | Count key duplicates at declared grain | TBD | TBD |
| Orphan order lines | Line order IDs without matching header | TBD | TBD |
| Invalid dates | Parse and range checks | TBD | TBD |
| Invalid quantities/prices | Type, sign, and range checks | TBD | TBD |
| Market/currency consistency | Check code values and units | TBD | TBD |
| Source-to-load reconciliation | Compare source, accepted, and rejected rows | TBD | TBD |
