"""Run the first reproducible analytical checks on RetailPulse data."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "retail_transactions.csv"
OUTPUT_DIR = ROOT / "data" / "processed"


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "Raw dataset not found. Run `python python/generate_retail_data.py` first."
        )

    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df = df.drop_duplicates().copy()
    df["profit_margin_pct"] = (df["profit"] / df["revenue"] * 100).round(2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    processed_path = OUTPUT_DIR / "retail_transactions_processed.csv"
    df.to_csv(processed_path, index=False)

    print("RetailPulse analytical checks")
    print("=" * 32)
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Date range: {df['order_date'].min().date()} to {df['order_date'].max().date()}")
    print(f"Revenue: ₹{df['revenue'].sum():,.2f}")
    print(f"Profit: ₹{df['profit'].sum():,.2f}")
    print(f"Orders: {df['order_id'].nunique():,}")
    print(f"Customers: {df['customer_id'].nunique():,}")
    print(f"Missing cells: {int(df.isna().sum().sum()):,}")
    print("\nTop categories by revenue:")
    print(df.groupby("category")["revenue"].sum().sort_values(ascending=False).head(5).round(2))


if __name__ == "__main__":
    main()
