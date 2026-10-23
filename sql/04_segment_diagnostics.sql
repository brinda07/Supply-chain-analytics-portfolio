-- Demonstration cuts of the synthetic records only. These are not real-world findings.

-- Delivered-order service by carrier and market.
WITH order_lines AS (
    SELECT order_id, BOOL_AND(delivered_qty >= ordered_qty) AS in_full
    FROM supply_chain.order_lines
    GROUP BY order_id
), order_flags AS (
    SELECT
        o.order_id, o.market, o.carrier_id, o.order_status,
        (o.actual_delivery_date <= o.promised_delivery_date) AS on_time,
        ol.in_full
    FROM supply_chain.orders o
    JOIN order_lines ol USING (order_id)
)
SELECT
    market,
    carrier_id,
    COUNT(*) AS delivered_orders,
    AVG(on_time::int)::numeric(8,4) AS on_time_rate,
    AVG(in_full::int)::numeric(8,4) AS in_full_rate,
    AVG((on_time AND in_full)::int)::numeric(8,4) AS otif_rate
FROM order_flags
WHERE order_status = 'delivered'
GROUP BY market, carrier_id
ORDER BY market, carrier_id;

-- Incomplete-line counts and units by product category.
SELECT
    p.category,
    p.sku_id,
    p.product_name,
    COUNT(*) FILTER (WHERE l.delivered_qty < l.ordered_qty) AS incomplete_lines,
    SUM(l.ordered_qty - l.delivered_qty) AS undelivered_units,
    COUNT(DISTINCT l.order_id) FILTER (WHERE l.delivered_qty < l.ordered_qty) AS affected_orders
FROM supply_chain.order_lines l
JOIN supply_chain.orders o USING (order_id)
JOIN supply_chain.products p USING (sku_id)
WHERE o.order_status = 'delivered'
GROUP BY p.category, p.sku_id, p.product_name
ORDER BY affected_orders DESC, undelivered_units DESC;

-- Service by fictional customer segment. Include volume to avoid overreading small groups.
WITH order_lines AS (
    SELECT order_id, BOOL_AND(delivered_qty >= ordered_qty) AS in_full
    FROM supply_chain.order_lines
    GROUP BY order_id
), order_flags AS (
    SELECT
        o.order_id, o.customer_id, o.market, o.order_status,
        (o.actual_delivery_date <= o.promised_delivery_date) AS on_time,
        ol.in_full
    FROM supply_chain.orders o
    JOIN order_lines ol USING (order_id)
)
SELECT
    c.market,
    c.customer_segment,
    COUNT(*) AS delivered_orders,
    AVG(on_time::int)::numeric(8,4) AS on_time_rate,
    AVG(in_full::int)::numeric(8,4) AS in_full_rate,
    AVG((on_time AND in_full)::int)::numeric(8,4) AS otif_rate
FROM order_flags f
JOIN supply_chain.customers c USING (customer_id)
WHERE f.order_status = 'delivered'
GROUP BY c.market, c.customer_segment
ORDER BY c.market, c.customer_segment;
