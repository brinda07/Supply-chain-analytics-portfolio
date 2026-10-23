-- Synthetic-data demonstration only. Results describe generated records, not a real business.
-- Calendar month is defined by order_date. Cancelled orders are excluded from
-- delivery-service denominators and should be reported separately.

WITH line_status AS (
    SELECT
        l.order_id,
        l.line_id,
        l.sku_id,
        l.ordered_qty,
        l.delivered_qty,
        l.delivered_qty >= l.ordered_qty AS line_in_full
    FROM supply_chain.order_lines l
),
order_line_summary AS (
    SELECT
        order_id,
        BOOL_AND(line_in_full) AS order_in_full,
        SUM(ordered_qty) AS ordered_units,
        SUM(delivered_qty) AS delivered_units
    FROM line_status
    GROUP BY order_id
),
order_service AS (
    SELECT
        o.order_id,
        o.market,
        o.carrier_id,
        o.customer_id,
        o.order_date,
        o.promised_delivery_date,
        o.actual_delivery_date,
        o.order_status,
        s.order_in_full,
        s.ordered_units,
        s.delivered_units,
        (o.actual_delivery_date <= o.promised_delivery_date) AS order_on_time
    FROM supply_chain.orders o
    JOIN order_line_summary s USING (order_id)
)
SELECT
    market,
    DATE_TRUNC('month', order_date)::date AS order_month,
    COUNT(*) FILTER (WHERE order_status = 'delivered') AS delivered_orders,
    COUNT(*) FILTER (WHERE order_status = 'cancelled') AS cancelled_orders,
    COUNT(*) FILTER (WHERE order_status = 'delivered' AND order_on_time) AS on_time_orders,
    COUNT(*) FILTER (WHERE order_status = 'delivered' AND order_in_full) AS in_full_orders,
    COUNT(*) FILTER (WHERE order_status = 'delivered' AND order_on_time AND order_in_full) AS otif_orders,
    ROUND(
        COUNT(*) FILTER (WHERE order_status = 'delivered' AND order_on_time)::numeric
        / NULLIF(COUNT(*) FILTER (WHERE order_status = 'delivered'), 0), 4
    ) AS on_time_rate,
    ROUND(
        COUNT(*) FILTER (WHERE order_status = 'delivered' AND order_in_full)::numeric
        / NULLIF(COUNT(*) FILTER (WHERE order_status = 'delivered'), 0), 4
    ) AS in_full_order_rate,
    ROUND(
        COUNT(*) FILTER (WHERE order_status = 'delivered' AND order_on_time AND order_in_full)::numeric
        / NULLIF(COUNT(*) FILTER (WHERE order_status = 'delivered'), 0), 4
    ) AS otif_rate
FROM order_service
GROUP BY market, DATE_TRUNC('month', order_date)::date
ORDER BY market, order_month;

-- Unit fill rate by market/month (delivered orders only).
SELECT
    o.market,
    DATE_TRUNC('month', o.order_date)::date AS order_month,
    SUM(l.delivered_qty)::numeric / NULLIF(SUM(l.ordered_qty), 0) AS unit_fill_rate,
    SUM(l.ordered_qty) AS ordered_units,
    SUM(l.delivered_qty) AS delivered_units
FROM supply_chain.orders o
JOIN supply_chain.order_lines l USING (order_id)
WHERE o.order_status = 'delivered'
GROUP BY o.market, DATE_TRUNC('month', o.order_date)::date
ORDER BY o.market, order_month;

-- Cancellation rate by market/month, denominator includes all submitted orders.
SELECT
    market,
    DATE_TRUNC('month', order_date)::date AS order_month,
    COUNT(*) AS submitted_orders,
    COUNT(*) FILTER (WHERE order_status = 'cancelled') AS cancelled_orders,
    COUNT(*) FILTER (WHERE order_status = 'cancelled')::numeric / NULLIF(COUNT(*), 0) AS cancellation_rate
FROM supply_chain.orders
GROUP BY market, DATE_TRUNC('month', order_date)::date
ORDER BY market, order_month;
