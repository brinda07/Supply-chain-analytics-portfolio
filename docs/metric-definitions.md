# Metric Definitions 

These measures are computable from the generated schema when implemented as specified. Any values produced describe **only generated records**. Do not use them as evidence of a real company’s performance.

| Metric | Grain | Definition | Eligibility / notes |
|---|---|---|---|
| Submitted orders | Order | Count distinct `order_id` across all orders. | Includes delivered and cancelled; state the period/filter. |
| Cancellation rate | Order | Cancelled orders ÷ all submitted orders. | Use `order_status = 'cancelled'`; display denominator. |
| On-time rate | Order | Delivered orders with `actual_delivery_date <= promised_delivery_date` ÷ delivered orders with both dates. | Exclude cancelled orders; dates are synthetic. |
| Line unit fill rate | Order line / units | Sum `delivered_qty` ÷ sum `ordered_qty` for delivered orders. | Exclude cancelled orders from this service calculation; state line/date filters. |
| In-full order rate | Order | Delivered orders where every line has `delivered_qty >= ordered_qty` ÷ delivered orders. | Compute line fulfillment first, then aggregate to order. |
| OTIF | Order | Delivered orders that are both on-time and in-full ÷ delivered assessable orders. | Calculate the joint condition directly at order grain. |
| Lead time | Order | `actual_delivery_date - order_date` in calendar days. | Only for delivered orders; descriptive, not equivalent to promised-date performance. |
| Ordered line value | Order line | `ordered_qty * unit_price_local`, grouped and reported by `currency_code`. | A demand-value measure based on fictional prices; do not combine USD and INR without a documented FX rate. |

## Calculation rules

- A cancelled order is counted in submitted orders and the cancellation numerator, but excluded from delivery/on-time/in-full/OTIF metrics.
- A delivered order is **in full** only if every order line meets or exceeds ordered quantity. Do not let over-delivery on one SKU offset a shortage on another.
- An order is **on time** when its order-level actual delivery date is on or before its promised delivery date.
- OTIF is the direct intersection of those two order-level flags; do not estimate it by multiplying separate overall rates.
- Show the number of eligible orders whenever a percentage is shown. Rates with different eligibility denominators are not directly comparable.
- Use the order date for cohort month unless the chart explicitly says otherwise. Do not mix order-month and delivery-month groupings.
- KPI calculations should use only the clean generated tables loaded from `data/synthetic/`.
