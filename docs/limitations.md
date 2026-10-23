# Project Limitations

## Data status

This project uses a deterministic, generated dataset. It contains no real retailer, employee, customer, supplier, carrier, order, price, or delivery event. The generator intentionally programs variation between fictional groups. Outputs are useful to demonstrate code and calculation logic, but they are not empirical evidence, industry benchmarks, causal findings, or proof of business performance.

## What the dataset supports

The generated tables support demonstration of order counts, cancellations, order-level on-time/in-full/OTIF calculations, unit fill rate, and exploratory comparisons by market, order month, customer, product, and carrier—under the definitions in `metric-definitions.md`.

## What it does not support

The data contains no real operational event history, inventory-on-hand, stock movements, purchase orders, supplier lead times, carrier tracking scans, contractual delivery windows, actual unit costs, chargebacks, or intervention outcomes. Therefore the project does not establish stockout causes, inventory optimization, safety stock, reorder points, real carrier or supplier performance, realized savings, or actual service improvement.

## Portfolio interpretation

Present this work as a technical demonstration of data modeling, ETL, SQL, KPI definitions, AI validation, and dashboard communication on synthetic records. Do not phrase segment differences as real-world discoveries. For actual operational insight, a separate analysis would require a publicly redistributable real dataset or authorized non-sensitive data, and conclusions would remain limited to that source.
