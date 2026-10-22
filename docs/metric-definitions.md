# Metric Definitions and Field Requirements

Complete the **availability** and **business-rule** columns after inspecting the actual files. These are proposed definitions, not findings.

| Metric | Proposed definition | Required fields | Availability / caveat |
|---|---|---|---|
| Order count | Count of distinct eligible order IDs. | Order ID; status if canceled orders can be excluded. | TBD; define cancellation treatment. |
| Unit fill rate | Sum of delivered units ÷ sum of ordered units. | Ordered quantity and delivered quantity at line level. | TBD; do not infer delivered quantity from ordered quantity. |
| In-full order rate | Eligible orders for which every line is delivered in full ÷ eligible orders with delivery data. | Order ID, product/line identity, ordered and delivered quantities. | TBD; confirm partial and split-shipment rules. |
| On-time order rate | Eligible orders delivered by the agreed promised date ÷ eligible assessable orders. | Promised date and actual delivery date, with order-level rule. | TBD; order date alone is not a promise date. |
| OTIF | Share of eligible orders meeting both the on-time and in-full conditions. Calculate the intersection directly at order level. | Promised date, actual delivery date, ordered and delivered quantities. | TBD; document date window, split shipments, exclusions, and missing data. |
| Lead time | Actual delivery date minus order date; specify calendar or business days. | Order date and actual delivery date. | Descriptive elapsed time; not necessarily a delivery-promise measure. |
| Order value | Sum of line quantity × unit price, under a documented order-value rule. | Quantity, price, currency, and any adjustments/discounts. | TBD; never sum amounts across currencies without a documented conversion basis. |

## Rules to record for every KPI

- Unit of analysis and data grain.
- Numerator and denominator.
- Time period and timezone/date boundary.
- Filters and treatment of canceled, returned, incomplete, or undelivered orders.
- Treatment of missing/invalid dates and quantities.
- Whether percentages are weighted by units, lines, or orders.
- Data source and validation query.

For OTIF, do not use a product of the overall on-time rate and in-full rate as a substitute for the direct share of orders meeting both conditions unless the project explicitly justifies and labels that approximation. A partially delivered order may count as not in full even if some lines were fulfilled.
