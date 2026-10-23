-- Tables for the deterministic synthetic dataset. Values in the two
-- currency codes are local and are not directly comparable.
CREATE SCHEMA IF NOT EXISTS supply_chain;

CREATE TABLE IF NOT EXISTS supply_chain.customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    market TEXT NOT NULL CHECK (market IN ('US', 'IN')),
    city TEXT NOT NULL,
    customer_segment TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supply_chain.products (
    sku_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    shelf_life_days INTEGER NOT NULL CHECK (shelf_life_days > 0),
    unit_of_measure TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supply_chain.carriers (
    carrier_id TEXT PRIMARY KEY,
    carrier_name TEXT NOT NULL,
    market TEXT NOT NULL CHECK (market IN ('US', 'IN'))
);

CREATE TABLE IF NOT EXISTS supply_chain.orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES supply_chain.customers(customer_id),
    carrier_id TEXT NOT NULL REFERENCES supply_chain.carriers(carrier_id),
    market TEXT NOT NULL CHECK (market IN ('US', 'IN')),
    order_date DATE NOT NULL,
    promised_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    order_status TEXT NOT NULL CHECK (order_status IN ('delivered', 'cancelled')),
    currency_code TEXT NOT NULL CHECK (currency_code IN ('USD', 'INR')),
    CHECK (order_status <> 'cancelled' OR actual_delivery_date IS NULL),
    CHECK (actual_delivery_date IS NULL OR actual_delivery_date >= order_date)
);

CREATE TABLE IF NOT EXISTS supply_chain.order_lines (
    line_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES supply_chain.orders(order_id),
    line_number INTEGER NOT NULL CHECK (line_number > 0),
    sku_id TEXT NOT NULL REFERENCES supply_chain.products(sku_id),
    ordered_qty INTEGER NOT NULL CHECK (ordered_qty > 0),
    delivered_qty INTEGER NOT NULL CHECK (delivered_qty >= 0),
    unit_price_local NUMERIC(10,2) NOT NULL CHECK (unit_price_local > 0),
    currency_code TEXT NOT NULL CHECK (currency_code IN ('USD', 'INR')),
    UNIQUE (order_id, line_number)
);

CREATE TABLE IF NOT EXISTS supply_chain.load_audit (
    batch_id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    input_rows INTEGER NOT NULL DEFAULT 0,
    accepted_rows INTEGER NOT NULL DEFAULT 0,
    rejected_rows INTEGER NOT NULL DEFAULT 0,
    load_status TEXT NOT NULL CHECK (load_status IN ('started', 'succeeded', 'failed')),
    error_summary TEXT
);
