# Project Limitations

## Data status

This project uses a deterministic, generated dataset. It contains no real retailer, employee, customer, supplier, carrier, order, price, or delivery event. The generator intentionally programs variation between fictional groups. Outputs demonstrate the implementation of data checks, SQL calculations, and dashboard communication; they are not empirical evidence, industry benchmarks, causal findings, or proof of business performance.

## What the dataset supports

Under the definitions in `metric-definitions.md`, the tables support demonstration of order counts, cancellations, order-level on-time/in-full/OTIF calculations, unit fill rate, and exploratory comparisons by market, order month, customer, product, and carrier.

## What it does not support

The data contains no real operational event history, inventory-on-hand, stock movements, purchase orders, supplier lead times, carrier tracking scans, contractual delivery windows, actual unit costs, chargebacks, or intervention outcomes. Therefore the project does not establish stockout causes, inventory optimization, safety stock, reorder points, real carrier or supplier performance, realized savings, or actual service improvement.

## Implementation boundary

The implemented workflow uses manual CSV imports into PostgreSQL. n8n and other workflow automation were not implemented. The `load_audit` table exists in the schema, but do not claim it was populated by an automation or used to monitor loads without separate evidence.

## Portfolio interpretation

Present this as a completed technical demonstration of synthetic-data generation, structural validation, relational modeling, manual PostgreSQL loading, SQL, KPI definitions, manual KPI verification, Power BI reporting, and AI-assisted development. Do not phrase segment differences as real-world discoveries. A real operational analysis would require authorized or openly redistributable real data and conclusions limited to that source.
