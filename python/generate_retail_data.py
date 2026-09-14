"""Generate a reproducible synthetic retail transaction dataset for RetailPulse.

The data is intentionally synthetic. It is designed to contain realistic
relationships (seasonality, category mix, discounts, regional variation and
customer behavior) without representing a real organization or person.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_TRANSACTIONS = 75_000
START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

PRODUCTS = [
    ("P001", "Laptop Pro 14", "Electronics", "Laptops", 72000, 54000),
    ("P002", "Laptop Air 13", "Electronics", "Laptops", 58000, 43000),
    ("P003", "Smartphone X", "Electronics", "Smartphones", 42000, 30000),
    ("P004", "Smartphone Lite", "Electronics", "Smartphones", 22000, 15500),
    ("P005", "Wireless Headphones", "Electronics", "Audio", 6500, 3900),
    ("P006", "Smart Watch", "Electronics", "Wearables", 9000, 5600),
    ("P007", "Office Chair", "Furniture", "Chairs", 12500, 7800),
    ("P008", "Study Desk", "Furniture", "Desks", 18000, 11200),
    ("P009", "Bookshelf", "Furniture", "Storage", 10500, 6700),
    ("P010", "Coffee Maker", "Home Appliances", "Kitchen", 7500, 4400),
    ("P011", "Air Fryer", "Home Appliances", "Kitchen", 9200, 5600),
    ("P012", "Mixer Grinder", "Home Appliances", "Kitchen", 6200, 3900),
    ("P013", "Running Shoes", "Fashion", "Footwear", 4800, 2700),
    ("P014", "Casual Sneakers", "Fashion", "Footwear", 4200, 2350),
    ("P015", "Backpack", "Fashion", "Bags", 2600, 1450),
    ("P016", "Cotton T-Shirt", "Fashion", "Apparel", 1100, 550),
    ("P017", "Skincare Kit", "Beauty", "Skincare", 2400, 1250),
    ("P018", "Hair Dryer", "Beauty", "Haircare", 3100, 1750),
    ("P019", "Yoga Mat", "Sports", "Fitness", 1800, 900),
    ("P020", "Dumbbell Set", "Sports", "Fitness", 5200, 3000),
]

LOCATIONS = [
    ("Jaipur", "Rajasthan", "North"), ("Delhi", "Delhi", "North"),
    ("Lucknow", "Uttar Pradesh", "North"), ("Mumbai", "Maharashtra", "West"),
    ("Ahmedabad", "Gujarat", "West"), ("Pune", "Maharashtra", "West"),
    ("Kolkata", "West Bengal", "East"), ("Bhubaneswar", "Odisha", "East"),
    ("Patna", "Bihar", "East"), ("Bengaluru", "Karnataka", "South"),
    ("Hyderabad", "Telangana", "South"), ("Chennai", "Tamil Nadu", "South"),
]

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]
CHANNELS = ["Store", "Website", "Mobile App"]


def main() -> None:
    rng = np.random.default_rng(SEED)
    dates = pd.date_range(START_DATE, END_DATE, freq="D")

    customer_ids = np.array([f"C{i:05d}" for i in range(1, 5001)])
    customer_names = np.array([f"Customer {i:05d}" for i in range(1, 5001)])
    customer_gender = rng.choice(["Female", "Male", "Other"], len(customer_ids), p=[0.47, 0.51, 0.02])
    customer_age = rng.integers(18, 66, len(customer_ids))
    location_idx = rng.integers(0, len(LOCATIONS), len(customer_ids))

    customer_weights = rng.pareto(1.7, len(customer_ids)) + 0.25
    customer_weights /= customer_weights.sum()
    customer_idx = rng.choice(len(customer_ids), N_TRANSACTIONS, p=customer_weights)

    date_idx = rng.integers(0, len(dates), N_TRANSACTIONS)
    order_dates = dates[date_idx]

    # The raw weights intentionally describe product mix; normalize them so
    # the generator remains robust if a weight is edited later.
    product_weights = np.array([
        0.08, 0.055, 0.075, 0.065, 0.055, 0.045, 0.055, 0.045, 0.035, 0.045,
        0.04, 0.035, 0.055, 0.045, 0.045, 0.06, 0.045, 0.035, 0.04, 0.03,
    ], dtype=float)
    product_weights /= product_weights.sum()
    product_idx = rng.choice(len(PRODUCTS), N_TRANSACTIONS, p=product_weights)

    month = order_dates.month.to_numpy()
    seasonality = np.where(np.isin(month, [10, 11, 12]), 1.18, 1.0)
    quantity = np.clip(rng.poisson(1.55 * seasonality) + 1, 1, 8)
    discount = np.clip(rng.normal(0.08, 0.045, N_TRANSACTIONS), 0, 0.30)

    channel = rng.choice(CHANNELS, N_TRANSACTIONS, p=[0.42, 0.34, 0.24])
    payment = rng.choice(PAYMENT_METHODS, N_TRANSACTIONS, p=[0.38, 0.23, 0.18, 0.14, 0.07])

    rows = []
    for i in range(N_TRANSACTIONS):
        ci, pi = customer_idx[i], product_idx[i]
        city, state, region = LOCATIONS[location_idx[ci]]
        product = PRODUCTS[pi]
        unit_price, unit_cost = product[4], product[5]
        revenue = quantity[i] * unit_price * (1 - discount[i])
        cost = quantity[i] * unit_cost
        rows.append([
            f"ORD{i + 1:07d}", order_dates[i].date(), customer_ids[ci], customer_names[ci],
            customer_gender[ci], int(customer_age[ci]), city, state, region, channel[i],
            product[0], product[1], product[2], product[3], int(quantity[i]), unit_price,
            round(float(discount[i] * 100), 2), round(float(revenue), 2), unit_cost,
            round(float(cost), 2), round(float(revenue - cost), 2), payment[i],
        ])

    columns = [
        "order_id", "order_date", "customer_id", "customer_name", "gender", "age",
        "city", "state", "region", "channel", "product_id", "product_name",
        "category", "subcategory", "quantity", "unit_price", "discount_pct",
        "revenue", "unit_cost", "cost", "profit", "payment_method",
    ]
    df = pd.DataFrame(rows, columns=columns)
    output_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "retail_transactions.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df):,} transaction rows")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()
