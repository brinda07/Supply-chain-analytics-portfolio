#!/usr/bin/env python3
"""Structural checks for the synthetic files; does not calculate KPI findings."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic"
EXPECTED = {
    "orders.csv": {"order_id", "customer_id", "carrier_id", "market", "order_date", "promised_delivery_date", "actual_delivery_date", "order_status", "currency_code"},
    "order_lines.csv": {"line_id", "order_id", "line_number", "sku_id", "ordered_qty", "delivered_qty", "unit_price_local", "currency_code"},
    "customers.csv": {"customer_id", "customer_name", "market", "city", "customer_segment"},
    "products.csv": {"sku_id", "product_name", "category", "shelf_life_days", "unit_of_measure"},
    "carriers.csv": {"carrier_id", "carrier_name", "market"},
}


def load(name: str) -> list[dict[str, str]]:
    path = DATA / name
    if not path.exists():
        raise SystemExit(f"Missing file: {path}")
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
        missing = EXPECTED[name] - fields
        if missing:
            raise SystemExit(f"{name}: missing columns {sorted(missing)}")
        return list(reader)


def unique(rows: list[dict[str, str]], field: str, table: str) -> set[str]:
    values = [row[field] for row in rows]
    if len(values) != len(set(values)):
        raise SystemExit(f"{table}: duplicate {field}")
    if any(not value for value in values):
        raise SystemExit(f"{table}: blank {field}")
    return set(values)


def iso_date(value: str, field: str, order_id: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"orders.csv: invalid {field} for {order_id}: {value!r}") from exc


def main() -> None:
    tables = {name: load(name) for name in EXPECTED}
    orders = tables["orders.csv"]
    lines = tables["order_lines.csv"]
    customers = tables["customers.csv"]
    products = tables["products.csv"]
    carriers = tables["carriers.csv"]

    order_ids = unique(orders, "order_id", "orders")
    line_ids = unique(lines, "line_id", "order_lines")
    customer_ids = unique(customers, "customer_id", "customers")
    sku_ids = unique(products, "sku_id", "products")
    carrier_ids = unique(carriers, "carrier_id", "carriers")
    del line_ids  # uniqueness is the check; no further use

    customer_by_id = {r["customer_id"]: r for r in customers}
    carrier_by_id = {r["carrier_id"]: r for r in carriers}
    order_by_id = {r["order_id"]: r for r in orders}
    line_key_set = set()
    line_counts: dict[str, int] = {}

    for order in orders:
        oid = order["order_id"]
        if order["customer_id"] not in customer_ids or order["carrier_id"] not in carrier_ids:
            raise SystemExit(f"orders.csv: missing customer or carrier reference for {oid}")
        if order["market"] not in {"US", "IN"}:
            raise SystemExit(f"orders.csv: invalid market for {oid}")
        if customer_by_id[order["customer_id"]]["market"] != order["market"]:
            raise SystemExit(f"orders.csv: customer market mismatch for {oid}")
        if carrier_by_id[order["carrier_id"]]["market"] != order["market"]:
            raise SystemExit(f"orders.csv: carrier market mismatch for {oid}")
        expected_currency = {"US": "USD", "IN": "INR"}[order["market"]]
        if order["currency_code"] != expected_currency:
            raise SystemExit(f"orders.csv: currency mismatch for {oid}")
        od = iso_date(order["order_date"], "order_date", oid)
        pd = iso_date(order["promised_delivery_date"], "promised_delivery_date", oid)
        if pd < od:
            raise SystemExit(f"orders.csv: promise precedes order for {oid}")
        if order["order_status"] == "delivered":
            actual = iso_date(order["actual_delivery_date"], "actual_delivery_date", oid)
            if actual < od:
                raise SystemExit(f"orders.csv: delivery precedes order for {oid}")
        elif order["order_status"] == "cancelled":
            if order["actual_delivery_date"]:
                raise SystemExit(f"orders.csv: cancelled order has delivery date: {oid}")
        else:
            raise SystemExit(f"orders.csv: unsupported status for {oid}: {order['order_status']}")

    for line in lines:
        if line["order_id"] not in order_ids:
            raise SystemExit(f"order_lines.csv: orphan order {line['order_id']}")
        if line["sku_id"] not in sku_ids:
            raise SystemExit(f"order_lines.csv: unknown SKU {line['sku_id']}")
        pair = (line["order_id"], line["line_number"])
        if pair in line_key_set:
            raise SystemExit(f"order_lines.csv: duplicate order_id + line_number {pair}")
        line_key_set.add(pair)
        line_counts[line["order_id"]] = line_counts.get(line["order_id"], 0) + 1
        try:
            ordered = int(line["ordered_qty"])
            delivered = int(line["delivered_qty"])
            price = float(line["unit_price_local"])
        except ValueError as exc:
            raise SystemExit(f"order_lines.csv: invalid numeric value on {line['line_id']}") from exc
        if ordered <= 0 or delivered < 0 or delivered > ordered or price <= 0:
            raise SystemExit(f"order_lines.csv: invalid quantity/price on {line['line_id']}")
        order = order_by_id[line["order_id"]]
        if line["currency_code"] != order["currency_code"]:
            raise SystemExit(f"order_lines.csv: currency mismatch on {line['line_id']}")
        if order["order_status"] == "cancelled" and delivered != 0:
            raise SystemExit(f"order_lines.csv: cancelled order has delivered quantity on {line['line_id']}")

    missing_lines = order_ids - set(line_counts)
    if missing_lines:
        raise SystemExit(f"orders without lines: {len(missing_lines)}")

    print("Structural validation passed. No service KPI was calculated.")
    for filename, rows in tables.items():
        print(f"{filename}: {len(rows)} data rows")
    print("Foreign keys, row keys, market/currency, date, and quantity rules passed.")


if __name__ == "__main__":
    main()
