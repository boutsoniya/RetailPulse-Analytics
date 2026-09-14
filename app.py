from pathlib import Path

from flask import Flask, jsonify, render_template
import pandas as pd

from python.generate_retail_data import main as generate_data

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "retail_transactions.csv"

app = Flask(__name__)


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        generate_data()
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    numeric = ["quantity", "unit_price", "discount_pct", "revenue", "unit_cost", "cost", "profit"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df


def records(frame: pd.DataFrame) -> list[dict]:
    """Return JSON-safe native Python values (never numpy scalar values)."""
    clean = frame.replace([float("inf"), float("-inf")], 0).fillna(0)
    output = []
    for row in clean.to_dict(orient="records"):
        output.append({
            key: (value.item() if hasattr(value, "item") else value)
            for key, value in row.items()
        })
    return output


@app.get("/")
def dashboard():
    return render_template("index.html")


@app.get("/api/summary")
def summary():
    df = load_data()
    revenue = float(df["revenue"].sum())
    profit = float(df["profit"].sum())
    orders = int(df["order_id"].nunique())
    customers = int(df["customer_id"].nunique())
    return jsonify({
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "orders": orders,
        "customers": customers,
        "aov": round(revenue / orders, 2) if orders else 0,
        "margin": round(profit / revenue * 100, 2) if revenue else 0,
    })


@app.get("/api/charts")
def charts():
    df = load_data()
    monthly = (
        df.assign(month=df["order_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    )
    category = df.groupby("category", as_index=False).agg(
        revenue=("revenue", "sum"), profit=("profit", "sum")
    ).sort_values("revenue", ascending=False)
    region = df.groupby("region", as_index=False).agg(
        revenue=("revenue", "sum"), profit=("profit", "sum")
    ).sort_values("revenue", ascending=False)
    top_products = df.groupby("product_name", as_index=False).agg(
        revenue=("revenue", "sum"), profit=("profit", "sum")
    ).sort_values("revenue", ascending=False).head(8)
    channel = df.groupby("channel", as_index=False).agg(revenue=("revenue", "sum")).sort_values(
        "revenue", ascending=False
    )
    return jsonify({
        "monthly": records(monthly.round(2)),
        "category": records(category.round(2)),
        "region": records(region.round(2)),
        "products": records(top_products.round(2)),
        "channel": records(channel.round(2)),
    })


@app.get("/health")
def health():
    return {"status": "ok", "service": "RetailPulse Analytics"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
