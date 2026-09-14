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
    return pd.read_csv(DATA_PATH, parse_dates=["order_date"])


@app.get("/")
def dashboard():
    return render_template("index.html")


@app.get("/api/summary")
def summary():
    df = load_data()
    return jsonify({
        "revenue": round(float(df["revenue"].sum()), 2),
        "profit": round(float(df["profit"].sum()), 2),
        "orders": int(df["order_id"].nunique()),
        "customers": int(df["customer_id"].nunique()),
        "aov": round(float(df["revenue"].sum() / df["order_id"].nunique()), 2),
        "margin": round(float(df["profit"].sum() / df["revenue"].sum() * 100), 2),
    })


@app.get("/api/charts")
def charts():
    df = load_data()
    monthly = df.assign(month=df["order_date"].dt.to_period("M").astype(str)).groupby("month").agg(
        revenue=("revenue", "sum"), profit=("profit", "sum")
    ).reset_index()
    category = df.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    region = df.groupby("region").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    top_products = df.groupby("product_name").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index().sort_values("revenue", ascending=False).head(8)
    channel = df.groupby("channel")["revenue"].sum().reset_index()
    return jsonify({
        "monthly": monthly.round(2).to_dict(orient="records"),
        "category": category.round(2).sort_values("revenue", ascending=False).to_dict(orient="records"),
        "region": region.round(2).sort_values("revenue", ascending=False).to_dict(orient="records"),
        "products": top_products.round(2).to_dict(orient="records"),
        "channel": channel.round(2).sort_values("revenue", ascending=False).to_dict(orient="records"),
    })


@app.get("/health")
def health():
    return {"status": "ok", "service": "RetailPulse Analytics"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
