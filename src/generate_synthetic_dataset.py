#!/usr/bin/env python3
"""Generate a deterministic, fully synthetic order-fulfillment dataset.

These records are fictional and are for practicing ingestion, SQL, validation,
and dashboard construction only. They are not empirical evidence about any
real company, market, customer, carrier, or supply chain.
"""
from __future__ import annotations

import csv
import json
import random
from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path

SEED = 20261023
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "synthetic"
FIXTURES = ROOT / "data" / "fixtures"

MARKETS = {
    "US": {
        "currency": "USD",
        "cities": ["Newark", "Boston", "Chicago", "Atlanta", "Seattle", "Austin"],
        "carriers": [
            ("CAR-US-01", "Fictional US Carrier A", 0.92),
            ("CAR-US-02", "Fictional US Carrier B", 0.84),
            ("CAR-US-03", "Fictional US Carrier C", 0.89),
        ],
        "partial_rate": 0.085,
    },
    "IN": {
        "currency": "INR",
        "cities": ["Ahmedabad", "Surat", "Mumbai", "Pune", "Jaipur", "Vadodara"],
        "carriers": [
            ("CAR-IN-01", "Fictional India Carrier A", 0.89),
            ("CAR-IN-02", "Fictional India Carrier B", 0.81),
            ("CAR-IN-03", "Fictional India Carrier C", 0.93),
        ],
        "partial_rate": 0.105,
    },
}

PRODUCT_TYPES = [
    ("Staples", ["Organic Lentils", "Brown Rice", "Chickpeas", "Quinoa", "Oats", "Millet"]),
    ("Spreads", ["Almond Butter", "Tahini", "Cashew Spread", "Peanut Butter", "Fruit Preserve", "Coconut Spread"]),
    ("Snacks", ["Seed Crackers", "Trail Mix", "Roasted Peas", "Rice Bites", "Granola Bar", "Dried Mango"]),
    ("Beverages", ["Oat Drink", "Coconut Water", "Herbal Tea", "Turmeric Latte", "Ginger Tonic", "Cacao Drink"]),
]


def month_starts(start_year: int, start_month: int, count: int) -> list[tuple[int, int]]:
    result = []
    year, month = start_year, start_month
    for _ in range(count):
        result.append((year, month))
        month += 1
        if month == 13:
            month = 1
            year += 1
    return result


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_dataset() -> dict[str, int]:
    rng = random.Random(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    FIXTURES.mkdir(parents=True, exist_ok=True)

    customers: list[dict] = []
    customers_by_market: dict[str, list[str]] = {market: [] for market in MARKETS}
    customer_index = 1
    segments = ["Regional supermarket", "Independent grocer", "Food-service buyer", "Specialty retailer"]
    for market, config in MARKETS.items():
        for local_number in range(1, 41):
            customer_id = f"CUS-{customer_index:04d}"
            customer_index += 1
            customers_by_market[market].append(customer_id)
            customers.append({
                "customer_id": customer_id,
                "customer_name": f"Fictional {market} Retailer {local_number:02d}",
                "market": market,
                "city": config["cities"][(local_number - 1) % len(config["cities"])],
                "customer_segment": segments[(local_number + (0 if market == "US" else 1)) % len(segments)],
            })

    products: list[dict] = []
    products_by_category: dict[str, list[str]] = {}
    sku_index = 1
    for category, names in PRODUCT_TYPES:
        products_by_category[category] = []
        for name in names:
            sku_id = f"SKU-{sku_index:03d}"
            sku_index += 1
            products_by_category[category].append(sku_id)
            shelf_life = {"Staples": 365, "Spreads": 270, "Snacks": 180, "Beverages": 150}[category]
            products.append({
                "sku_id": sku_id,
                "product_name": name,
                "category": category,
                "shelf_life_days": shelf_life + ((sku_index * 7) % 45),
                "unit_of_measure": "each",
            })

    carriers: list[dict] = []
    carrier_lookup: dict[str, list[tuple[str, float]]] = {}
    for market, config in MARKETS.items():
        carrier_lookup[market] = []
        for carrier_id, carrier_name, on_time_probability in config["carriers"]:
            carrier_lookup[market].append((carrier_id, on_time_probability))
            carriers.append({
                "carrier_id": carrier_id,
                "carrier_name": carrier_name,
                "market": market,
            })

    orders: list[dict] = []
    order_lines: list[dict] = []
    months = month_starts(2025, 1, 18)  # 2025-01 through 2026-06 inclusive
    order_number = 1
    line_number = 1
    qty_weights = [1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8]

    for year, month in months:
        days_in_month = monthrange(year, month)[1]
        for market, config in MARKETS.items():
            # Forty orders per market-month gives a predictable sample size.
            for _ in range(40):
                order_id = f"ORD-{order_number:06d}"
                order_number += 1
                order_date = date(year, month, rng.randint(1, days_in_month))
                customer_id = rng.choice(customers_by_market[market])
                carrier_id, carrier_on_time_probability = rng.choice(carrier_lookup[market])
                promised_days = rng.randint(2, 6)
                promised_date = order_date + timedelta(days=promised_days)
                is_cancelled = rng.random() < 0.025
                is_on_time = (not is_cancelled) and rng.random() < carrier_on_time_probability
                if is_cancelled:
                    order_status = "cancelled"
                    actual_delivery_date = ""
                else:
                    order_status = "delivered"
                    if is_on_time:
                        delivery_offset = rng.randint(-1, 0)
                    else:
                        delivery_offset = rng.randint(1, 5)
                    actual_delivery_date = (promised_date + timedelta(days=delivery_offset)).isoformat()

                currency = config["currency"]
                line_count = rng.randint(1, 4)
                selected_skus = rng.sample([p["sku_id"] for p in products], line_count)
                order_specs = []
                for sku_id in selected_skus:
                    product_number = int(sku_id.split("-")[1])
                    qty = rng.choice(qty_weights)
                    product = products[product_number - 1]
                    category_partial_bump = {"Staples": 0.00, "Spreads": 0.015, "Snacks": 0.025, "Beverages": 0.035}[product["category"]]
                    partial = (not is_cancelled) and rng.random() < (config["partial_rate"] + category_partial_bump)
                    if is_cancelled:
                        delivered_qty = 0
                    elif partial:
                        delivered_qty = max(0, qty - rng.randint(1, min(3, qty)))
                    else:
                        delivered_qty = qty
                    unit_price = (4.50 + product_number * 1.17 + rng.uniform(-0.4, 0.8)) if market == "US" else (280 + product_number * 73 + rng.uniform(-20, 35))
                    order_specs.append((sku_id, qty, delivered_qty, round(unit_price, 2)))

                orders.append({
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "carrier_id": carrier_id,
                    "market": market,
                    "order_date": order_date.isoformat(),
                    "promised_delivery_date": promised_date.isoformat(),
                    "actual_delivery_date": actual_delivery_date,
                    "order_status": order_status,
                    "currency_code": currency,
                })
                for line_index, (sku_id, ordered_qty, delivered_qty, unit_price) in enumerate(order_specs, start=1):
                    order_lines.append({
                        "line_id": f"LINE-{line_number:07d}",
                        "order_id": order_id,
                        "line_number": line_index,
                        "sku_id": sku_id,
                        "ordered_qty": ordered_qty,
                        "delivered_qty": delivered_qty,
                        "unit_price_local": f"{unit_price:.2f}",
                        "currency_code": currency,
                    })
                    line_number += 1

    write_csv(OUT / "orders.csv", orders, [
        "order_id", "customer_id", "carrier_id", "market", "order_date",
        "promised_delivery_date", "actual_delivery_date", "order_status", "currency_code",
    ])
    write_csv(OUT / "order_lines.csv", order_lines, [
        "line_id", "order_id", "line_number", "sku_id", "ordered_qty",
        "delivered_qty", "unit_price_local", "currency_code",
    ])
    write_csv(OUT / "customers.csv", customers, [
        "customer_id", "customer_name", "market", "city", "customer_segment",
    ])
    write_csv(OUT / "products.csv", products, [
        "sku_id", "product_name", "category", "shelf_life_days", "unit_of_measure",
    ])
    write_csv(OUT / "carriers.csv", carriers, ["carrier_id", "carrier_name", "market"])

    counts = {
        "orders": len(orders),
        "order_lines": len(order_lines),
        "customers": len(customers),
        "products": len(products),
        "carriers": len(carriers),
    }
    manifest = {
        "dataset_name": "Synthetic Retail Order Fulfillment Dataset",
        "dataset_type": "fully synthetic, deterministic, fictional records",
        "generated_by": "src/generate_synthetic_dataset.py",
        "random_seed": SEED,
        "generation_date": "2026-10-23",
        "coverage_start": "2025-01-01",
        "coverage_end": "2026-06-30",
        "markets": ["US", "IN"],
        "currency_codes": ["USD", "INR"],
        "tables": {
            "orders.csv": {"grain": "one row per order", "rows": counts["orders"]},
            "order_lines.csv": {"grain": "one row per order-product line", "rows": counts["order_lines"]},
            "customers.csv": {"grain": "one row per fictional customer", "rows": counts["customers"]},
            "products.csv": {"grain": "one row per fictional SKU", "rows": counts["products"]},
            "carriers.csv": {"grain": "one row per fictional carrier", "rows": counts["carriers"]},
        },
        "limitations": [
            "No real people, company, retailer, carrier, or transaction is represented.",
            "The data is created for practicing data ingestion, SQL, validation, and visualization only.",
            "Any patterns are consequences of the generator's design, not empirical supply-chain findings.",
            "Synthetic prices are market-local; do not aggregate USD and INR without a separate documented FX basis.",
            "No inventory-on-hand, stock movement, purchase-order, or actual supplier lead-time data is included.",
        ],
    }
    (OUT / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # Deliberately invalid examples are isolated from the clean analysis tables.
    order_headers = [
        "order_id", "customer_id", "carrier_id", "market", "order_date",
        "promised_delivery_date", "actual_delivery_date", "order_status", "currency_code",
    ]
    bad_orders = [
        {"order_id": "TEST-001", "customer_id": "CUS-0001", "carrier_id": "CAR-US-01", "market": "US", "order_date": "2026-01-03", "promised_delivery_date": "2026-01-06", "actual_delivery_date": "2026-01-05", "order_status": "delivered", "currency_code": "USD"},
        {"order_id": "TEST-001", "customer_id": "CUS-0001", "carrier_id": "CAR-US-01", "market": "US", "order_date": "2026-01-03", "promised_delivery_date": "2026-01-06", "actual_delivery_date": "2026-01-05", "order_status": "delivered", "currency_code": "USD"},
        {"order_id": "TEST-002", "customer_id": "CUS-0002", "carrier_id": "CAR-US-02", "market": "US", "order_date": "not-a-date", "promised_delivery_date": "2026-01-07", "actual_delivery_date": "2026-01-08", "order_status": "delivered", "currency_code": "USD"},
        {"order_id": "TEST-003", "customer_id": "CUS-0003", "carrier_id": "CAR-US-01", "market": "MARS", "order_date": "2026-01-04", "promised_delivery_date": "2026-01-08", "actual_delivery_date": "2026-01-07", "order_status": "delivered", "currency_code": "XYZ"},
        {"order_id": "", "customer_id": "CUS-0004", "carrier_id": "CAR-US-01", "market": "US", "order_date": "2026-01-05", "promised_delivery_date": "2026-01-09", "actual_delivery_date": "2026-01-08", "order_status": "delivered", "currency_code": "USD"},
    ]
    write_csv(FIXTURES / "orders_validation_fixture.csv", bad_orders, order_headers)
    line_headers = ["line_id", "order_id", "line_number", "sku_id", "ordered_qty", "delivered_qty", "unit_price_local", "currency_code"]
    bad_lines = [
        {"line_id": "TEST-L1", "order_id": "TEST-001", "line_number": 1, "sku_id": "SKU-001", "ordered_qty": 4, "delivered_qty": 4, "unit_price_local": "12.00", "currency_code": "USD"},
        {"line_id": "TEST-L1", "order_id": "TEST-001", "line_number": 1, "sku_id": "SKU-001", "ordered_qty": 4, "delivered_qty": 4, "unit_price_local": "12.00", "currency_code": "USD"},
        {"line_id": "TEST-L2", "order_id": "NO-SUCH-ORDER", "line_number": 1, "sku_id": "SKU-002", "ordered_qty": 3, "delivered_qty": 2, "unit_price_local": "8.00", "currency_code": "USD"},
        {"line_id": "TEST-L3", "order_id": "TEST-002", "line_number": 1, "sku_id": "SKU-003", "ordered_qty": -2, "delivered_qty": 1, "unit_price_local": "7.00", "currency_code": "USD"},
        {"line_id": "TEST-L4", "order_id": "TEST-003", "line_number": 1, "sku_id": "SKU-004", "ordered_qty": "three", "delivered_qty": 2, "unit_price_local": "9.00", "currency_code": "USD"},
    ]
    write_csv(FIXTURES / "order_lines_validation_fixture.csv", bad_lines, line_headers)

    return counts


if __name__ == "__main__":
    counts = build_dataset()
    print("Generated deterministic synthetic files (not empirical data):")
    for table, count in counts.items():
        print(f"  {table}: {count} rows")
    print(f"Files: {OUT}")
    print(f"Test fixtures: {FIXTURES}")
