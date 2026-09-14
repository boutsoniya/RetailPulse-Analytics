"""Clean, validate and enrich the raw RetailPulse dataset.

Run with: python -m python.prepare_data
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "retail_sales_synthetic.csv"
OUT_DIR = ROOT / "data" / "processed"
OUT = OUT_DIR / "retail_sales_clean.csv"
QUALITY = OUT_DIR / "data_quality_report.csv"


def main() -> None:
    if not RAW.exists():
        from python.generate_retail_data import main as generate
        generate()

    df = pd.read_csv(RAW)
    before = len(df)
    checks = []

    def check(name, count, treatment):
        checks.append({"check": name, "issues_found": int(count), "treatment": treatment})

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    bad_dates = df["Order_Date"].isna().sum()
    check("Invalid dates", bad_dates, "Rows removed after date validation")
    df = df.dropna(subset=["Order_Date"])

    df["Region"] = df["Region"].astype("string").str.strip().str.title()
    region_map = {"West": "West", "East": "East", "North": "North", "South": "South"}
    df["Region"] = df["Region"].map(region_map)

    # Product is the authoritative lookup for missing category values.
    product_category = df.groupby("Product")["Category"].agg(lambda s: s.dropna().mode().iat[0] if not s.dropna().empty else "Unknown")
    missing_category = df["Category"].isna().sum()
    df["Category"] = df["Category"].fillna(df["Product"].map(product_category)).fillna("Unknown")
    check("Missing category", missing_category, "Repaired from product mapping")

    duplicates = df.duplicated(subset=["Order_ID"]).sum()
    df = df.drop_duplicates(subset=["Order_ID"], keep="first")
    check("Duplicate Order_ID", duplicates, "Removed duplicate ingestion rows")

    for col in ["Quantity", "Unit_Price", "Discount_Pct", "Sales", "Cost", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    invalid_qty = (df["Quantity"] <= 0).sum()
    df = df[df["Quantity"] > 0].copy()
    check("Non-positive quantity", invalid_qty, "Excluded invalid transactions")

    invalid_discount = (~df["Discount_Pct"].between(0, 0.50)).sum()
    df = df[df["Discount_Pct"].between(0, 0.50)].copy()
    check("Discount outside 0-50%", invalid_discount, "Excluded invalid discount values")

    # Recalculate financial measures rather than trusting source calculations.
    df["Sales_Calculated"] = (df["Quantity"] * df["Unit_Price"] * (1 - df["Discount_Pct"])).round(2)
    df["Cost_Calculated"] = (df["Quantity"] * (df["Cost"] / df["Quantity"])).round(2)
    df["Profit_Calculated"] = (df["Sales_Calculated"] - df["Cost_Calculated"]).round(2)
    df["Profit_Margin_Pct"] = (df["Profit_Calculated"] / df["Sales_Calculated"] * 100).round(2)
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)

    # Realized business KPIs use completed orders. Status is retained for operations analysis.
    df["Realized_Sales"] = df["Sales_Calculated"].where(df["Order_Status"].eq("Completed"), 0.0)
    df["Realized_Profit"] = df["Profit_Calculated"].where(df["Order_Status"].eq("Completed"), 0.0)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    check("Raw row count", before, f"Cleaned dataset contains {len(df)} rows")
    pd.DataFrame(checks).to_csv(QUALITY, index=False)

    print(f"Raw rows: {before:,}")
    print(f"Clean rows: {len(df):,}")
    print(f"Completed orders: {int(df['Order_Status'].eq('Completed').sum()):,}")
    print(f"Revenue: ₹{df['Realized_Sales'].sum():,.2f}")
    print(f"Profit: ₹{df['Realized_Profit'].sum():,.2f}")
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
