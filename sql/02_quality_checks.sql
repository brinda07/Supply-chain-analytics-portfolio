-- Run after loading the synthetic files. These are checks, not performance findings.

-- Table row counts.
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM supply_chain.orders
UNION ALL SELECT 'order_lines', COUNT(*) FROM supply_chain.order_lines
UNION ALL SELECT 'customers', COUNT(*) FROM supply_chain.customers
UNION ALL SELECT 'products', COUNT(*) FROM supply_chain.products
UNION ALL SELECT 'carriers', COUNT(*) FROM supply_chain.carriers;

-- Parent/child and market consistency.
SELECT COUNT(*) AS lines_without_order
FROM supply_chain.order_lines l
LEFT JOIN supply_chain.orders o USING (order_id)
WHERE o.order_id IS NULL;

SELECT COUNT(*) AS orders_without_customer
FROM supply_chain.orders o
LEFT JOIN supply_chain.customers c USING (customer_id)
WHERE c.customer_id IS NULL;

SELECT COUNT(*) AS orders_without_carrier
FROM supply_chain.orders o
LEFT JOIN supply_chain.carriers c USING (carrier_id)
WHERE c.carrier_id IS NULL;

SELECT COUNT(*) AS market_currency_mismatches
FROM supply_chain.orders
WHERE (market = 'US' AND currency_code <> 'USD')
   OR (market = 'IN' AND currency_code <> 'INR');

-- Date and quantity logic checks.
SELECT COUNT(*) AS invalid_order_dates
FROM supply_chain.orders
WHERE promised_delivery_date < order_date
   OR (actual_delivery_date IS NOT NULL AND actual_delivery_date < order_date);

SELECT COUNT(*) AS delivered_orders_without_actual_date
FROM supply_chain.orders
WHERE order_status = 'delivered' AND actual_delivery_date IS NULL;

SELECT COUNT(*) AS cancelled_orders_with_actual_date
FROM supply_chain.orders
WHERE order_status = 'cancelled' AND actual_delivery_date IS NOT NULL;

SELECT COUNT(*) AS quantities_overdelivered
FROM supply_chain.order_lines
WHERE delivered_qty > ordered_qty;

-- Load only the clean synthetic files into the analytical schema.
-- Testing an n8n rejection branch is optional and separate from this SQL flow.
