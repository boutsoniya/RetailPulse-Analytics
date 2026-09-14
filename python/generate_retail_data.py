"""Generate the reproducible synthetic retail dataset used by RetailPulse.

The dataset is synthetic and is NOT WSA confidential data. It is intentionally
small enough for an academic 45-day internship project while containing the
business dimensions required by the report: sales, customer segments,
regions, categories, discounts, costs and order status.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N_TRANSACTIONS = 1500
START_DATE = "2025-01-01"
END_DATE = "2026-06-20"

PRODUCTS = [
    ("P001", "Laptop Pro 14", "Electronics", 72000, 54000),
    ("P002", "Laptop Air 13", "Electronics", 58000, 43000),
    ("P003", "Smartphone X", "Electronics", 42000, 30000),
    ("P004", "Smartphone Lite", "Electronics", 22000, 15500),
    ("P005", "Wireless Headphones", "Electronics", 6500, 3900),
    ("P006", "Smart Watch", "Electronics", 9000, 5600),
    ("P007", "Office Chair", "Furniture", 12500, 7800),
    ("P008", "Study Desk", "Furniture", 18000, 11200),
    ("P009", "Bookshelf", "Furniture", 10500, 6700),
    ("P010", "Coffee Maker", "Office Supplies", 7500, 4400),
    ("P011", "Air Fryer", "Office Supplies", 9200, 5600),
    ("P012", "Mixer Grinder", "Office Supplies", 6200, 3900),
    ("P013", "Running Shoes", "Accessories", 4800, 2700),
    ("P014", "Casual Sneakers", "Accessories", 4200, 2350),
    ("P015", "Backpack", "Accessories", 2600, 1450),
    ("P016", "Cotton T-Shirt", "Accessories", 1100, 550),
    ("P017", "Skincare Kit", "Accessories", 2400, 1250),
    ("P018", "Hair Dryer", "Accessories", 3100, 1750),
]
LOCATIONS = [
    ("Jaipur", "Rajasthan", "North"), ("Delhi", "Delhi", "North"),
    ("Lucknow", "Uttar Pradesh", "North"), ("Mumbai", "Maharashtra", "West"),
    ("Ahmedabad", "Gujarat", "West"), ("Pune", "Maharashtra", "West"),
    ("Kolkata", "West Bengal", "East"), ("Bhubaneswar", "Odisha", "East"),
    ("Patna", "Bihar", "East"), ("Bengaluru", "Karnataka", "South"),
    ("Hyderabad", "Telangana", "South"), ("Chennai", "Tamil Nadu", "South"),
]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]
CHANNELS = ["Store", "Website", "Mobile App"]
PAYMENTS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"]
STATUS = ["Completed", "Returned", "Cancelled"]


def main() -> None:
    rng = np.random.default_rng(SEED)
    dates = pd.date_range(START_DATE, END_DATE, freq="D")
    customers = np.array([f"C{i:04d}" for i in range(1, 501)])
    customer_segment = rng.choice(SEGMENTS, len(customers), p=[0.58, 0.25, 0.17])
    customer_city_idx = rng.integers(0, len(LOCATIONS), len(customers))
    customer_weights = rng.pareto(2.0, len(customers)) + 0.35
    customer_weights /= customer_weights.sum()

    customer_idx = rng.choice(len(customers), N_TRANSACTIONS, p=customer_weights)
    order_dates = dates[rng.integers(0, len(dates), N_TRANSACTIONS)]
    product_weights = np.array([0.08,0.06,0.07,0.07,0.06,0.05,0.06,0.05,0.04,0.05,0.05,0.04,0.08,0.07,0.06,0.06,0.04,0.03], dtype=float)
    product_weights /= product_weights.sum()
    product_idx = rng.choice(len(PRODUCTS), N_TRANSACTIONS, p=product_weights)
    month = order_dates.month.to_numpy()
    seasonality = np.where(np.isin(month, [10, 11, 12]), 1.18, 1.0)
    quantity = np.clip(rng.poisson(1.4 * seasonality) + 1, 1, 8)
    discount = np.clip(rng.normal(0.08, 0.045, N_TRANSACTIONS), 0, 0.30)
    channel = rng.choice(CHANNELS, N_TRANSACTIONS, p=[0.42, 0.34, 0.24])
    payment = rng.choice(PAYMENTS, N_TRANSACTIONS, p=[0.38, 0.23, 0.18, 0.14, 0.07])
    status = rng.choice(STATUS, N_TRANSACTIONS, p=[0.88, 0.075, 0.045])

    rows = []
    for i in range(N_TRANSACTIONS):
        ci, pi = customer_idx[i], product_idx[i]
        city, state, region = LOCATIONS[customer_city_idx[ci]]
        product = PRODUCTS[pi]
        unit_price, unit_cost = product[3], product[4]
        sales = quantity[i] * unit_price * (1 - discount[i])
        cost = quantity[i] * unit_cost
        # Returned/cancelled orders remain in the raw source but are excluded
        # from realized-sales KPIs during preparation.
        rows.append([
            f"ORD{i + 1:04d}", order_dates[i].date(), customers[ci], region,
            customer_segment[ci], product[0], product[1], product[2], int(quantity[i]),
            unit_price, round(float(discount[i]), 4), round(float(sales), 2),
            round(float(cost), 2), round(float(sales - cost), 2), status[i],
            city, state, channel[i], payment[i]
        ])

    columns = [
        "Order_ID", "Order_Date", "Customer_ID", "Region", "Customer_Segment",
        "Product_ID", "Product", "Category", "Quantity", "Unit_Price",
        "Discount_Pct", "Sales", "Cost", "Profit", "Order_Status", "City",
        "State", "Channel", "Payment_Method"
    ]
    df = pd.DataFrame(rows, columns=columns)

    # Controlled quality issues make the cleaning stage demonstrable.
    df.loc[7, "Category"] = None
    df.loc[31, "Region"] = " west "
    df.loc[52, "Discount_Pct"] = 0.55
    df.loc[73, "Quantity"] = -1
    df.loc[91, "Order_Date"] = "not-a-date"
    df = pd.concat([df, df.iloc[[15]].copy()], ignore_index=True)

    output_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "retail_sales_synthetic.csv"
    df.to_csv(path, index=False)
    print(f"Generated {len(df):,} raw rows at {path}")


if __name__ == "__main__":
    main()
