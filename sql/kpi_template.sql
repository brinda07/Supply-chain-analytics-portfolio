-- TEMPLATE ONLY: adapt after inspecting the source schema.
-- Required normalized fields: order_id, market, promised_date,
-- actual_delivery_date, ordered_qty, delivered_qty.
-- Validate split shipment, cancellation, return, date-window, and missing-data rules.
-- Do not execute/report this KPI if required source fields are absent.

WITH order_level AS (
    SELECT
        order_id,
        market,
        MIN(promised_date) AS promised_date,
        MAX(actual_delivery_date) AS actual_delivery_date,
        SUM(ordered_qty) AS ordered_units,
        SUM(delivered_qty) AS delivered_units
    FROM clean_order_lines
    GROUP BY order_id, market
),
classified AS (
    SELECT
        *,
        actual_delivery_date <= promised_date AS is_on_time,
        delivered_units >= ordered_units AS is_in_full
    FROM order_level
    WHERE promised_date IS NOT NULL
      AND actual_delivery_date IS NOT NULL
      AND ordered_units IS NOT NULL
      AND delivered_units IS NOT NULL
)
SELECT
    market,
    COUNT(*) AS assessable_orders,
    AVG(is_on_time::int)::numeric(8,4) AS on_time_rate,
    AVG(is_in_full::int)::numeric(8,4) AS in_full_rate,
    AVG((is_on_time AND is_in_full)::int)::numeric(8,4) AS otif_rate
FROM classified
GROUP BY market
ORDER BY market;
