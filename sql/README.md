# SQL Layer

Build SQL only after mapping actual CSV fields in `docs/data-dictionary.md`. Keep raw/staging tables separate from clean views. State the grain of every table/view and use stable, documented keys.

Before reporting order-level values from joined data, aggregate order lines to order grain to avoid multiplying header-level metrics. Use exact final metric rules from `docs/metric-definitions.md`.

`kpi_template.sql` assumes a clean line-level view with order ID, market, promised date, actual delivery date, ordered quantity, and delivered quantity. It will not run until those fields are verified and mapped; it is a reference, not proof the dataset supports OTIF.
