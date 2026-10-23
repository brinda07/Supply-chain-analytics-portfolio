-- Single-row-per-order view for dashboards. All values are synthetic.
CREATE OR REPLACE VIEW supply_chain.order_service AS
WITH line_summary AS (
    SELECT
        order_id,
        BOOL_AND(delivered_qty >= ordered_qty) AS order_in_full,
        SUM(ordered_qty) AS ordered_units,
        SUM(delivered_qty) AS delivered_units,
        SUM(ordered_qty * unit_price_local) AS ordered_value_local,
        MIN(currency_code) AS line_currency_code,
        COUNT(*) AS line_count
    FROM supply_chain.order_lines
    GROUP BY order_id
)
SELECT
    o.order_id,
    o.customer_id,
    o.carrier_id,
    o.market,
    o.order_date,
    DATE_TRUNC('month', o.order_date)::date AS order_month,
    o.promised_delivery_date,
    o.actual_delivery_date,
    o.order_status,
    o.currency_code,
    s.line_count,
    s.ordered_units,
    s.delivered_units,
    s.ordered_value_local,
    CASE
        WHEN o.order_status = 'delivered'
        THEN o.actual_delivery_date <= o.promised_delivery_date
        ELSE NULL
    END AS is_on_time,
    CASE
        WHEN o.order_status = 'delivered' THEN s.order_in_full
        ELSE NULL
    END AS is_in_full,
    CASE
        WHEN o.order_status = 'delivered'
        THEN (o.actual_delivery_date <= o.promised_delivery_date) AND s.order_in_full
        ELSE NULL
    END AS is_otif
FROM supply_chain.orders o
JOIN line_summary s USING (order_id);
