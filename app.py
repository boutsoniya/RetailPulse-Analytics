from pathlib import Path
from flask import Flask, jsonify, render_template, request
import pandas as pd

from python.generate_retail_data import main as generate_data
from python.prepare_data import main as prepare_data

ROOT = Path(__file__).resolve().parent
RAW_PATH = ROOT / "data" / "raw" / "retail_sales_synthetic.csv"
CLEAN_PATH = ROOT / "data" / "processed" / "retail_sales_clean.csv"
app = Flask(__name__)
_CACHE = None


def load_data() -> pd.DataFrame:
    global _CACHE
    if _CACHE is not None:
        return _CACHE.copy()
    if not CLEAN_PATH.exists():
        if not RAW_PATH.exists():
            generate_data()
        prepare_data()
    df = pd.read_csv(CLEAN_PATH, parse_dates=["Order_Date"])
    _CACHE = df
    return df.copy()


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    region = request.args.get("region")
    category = request.args.get("category")
    segment = request.args.get("segment")
    channel = request.args.get("channel")
    if region and region != "All": df = df[df["Region"] == region]
    if category and category != "All": df = df[df["Category"] == category]
    if segment and segment != "All": df = df[df["Customer_Segment"] == segment]
    if channel and channel != "All": df = df[df["Channel"] == channel]
    return df


def records(frame: pd.DataFrame) -> list[dict]:
    clean = frame.replace([float("inf"), float("-inf")], 0).fillna(0)
    return [{k: (v.item() if hasattr(v, "item") else v) for k, v in row.items()}
            for row in clean.to_dict(orient="records")]


def completed(df):
    return df[df["Order_Status"] == "Completed"].copy()


@app.get("/")
def dashboard():
    return render_template("index.html")


@app.get("/api/filters")
def filters():
    df = load_data()
    return jsonify({
        "regions": ["All"] + sorted(df.Region.dropna().unique().tolist()),
        "categories": ["All"] + sorted(df.Category.dropna().unique().tolist()),
        "segments": ["All"] + sorted(df.Customer_Segment.dropna().unique().tolist()),
        "channels": ["All"] + sorted(df.Channel.dropna().unique().tolist()),
    })


@app.get("/api/summary")
def summary():
    df = apply_filters(load_data())
    sales = completed(df)
    revenue = float(sales["Sales_Calculated"].sum())
    profit = float(sales["Profit_Calculated"].sum())
    orders = int(sales["Order_ID"].nunique())
    customers = int(sales["Customer_ID"].nunique())
    return jsonify({
        "revenue": round(revenue, 2), "profit": round(profit, 2),
        "orders": orders, "customers": customers,
        "aov": round(revenue / orders, 2) if orders else 0,
        "margin": round(profit / revenue * 100, 2) if revenue else 0,
        "returns": int((df.Order_Status == "Returned").sum()),
        "cancellations": int((df.Order_Status == "Cancelled").sum()),
    })


@app.get("/api/charts")
def charts():
    df = apply_filters(load_data())
    sales = completed(df)
    monthly = sales.assign(Month=sales.Order_Date.dt.to_period("M").astype(str)).groupby("Month", as_index=False).agg(
        revenue=("Sales_Calculated", "sum"), profit=("Profit_Calculated", "sum"), orders=("Order_ID", "nunique"))
    category = sales.groupby("Category", as_index=False).agg(revenue=("Sales_Calculated", "sum"), profit=("Profit_Calculated", "sum"), orders=("Order_ID", "nunique"))
    category["margin"] = category["profit"] / category["revenue"] * 100
    region = sales.groupby("Region", as_index=False).agg(revenue=("Sales_Calculated", "sum"), profit=("Profit_Calculated", "sum"), orders=("Order_ID", "nunique"))
    region["margin"] = region["profit"] / region["revenue"] * 100
    segment = sales.groupby("Customer_Segment", as_index=False).agg(revenue=("Sales_Calculated", "sum"), profit=("Profit_Calculated", "sum"), orders=("Order_ID", "nunique"), customers=("Customer_ID", "nunique"))
    segment["aov"] = segment["revenue"] / segment["orders"]
    product = sales.groupby(["Product", "Category"], as_index=False).agg(revenue=("Sales_Calculated", "sum"), profit=("Profit_Calculated", "sum"), units=("Quantity", "sum"))
    product["margin"] = product["profit"] / product["revenue"] * 100
    product = product.sort_values("revenue", ascending=False).head(10)
    channel = sales.groupby("Channel", as_index=False).agg(revenue=("Sales_Calculated", "sum"), orders=("Order_ID", "nunique"))
    discount = sales.assign(discount_band=pd.cut(sales.Discount_Pct, [-.001,.05,.10,.15,.30], labels=["<5%","5–10%","10–15%","15%+"])).groupby("discount_band", observed=False, as_index=False).agg(revenue=("Sales_Calculated","sum"), profit=("Profit_Calculated","sum"), orders=("Order_ID","nunique"))
    discount["margin"] = discount["profit"] / discount["revenue"] * 100
    status = df.groupby("Order_Status", as_index=False).agg(orders=("Order_ID","nunique"), gross_value=("Sales_Calculated","sum"))
    return jsonify({"monthly": records(monthly), "category": records(category.sort_values("revenue", ascending=False)), "region": records(region.sort_values("revenue", ascending=False)), "segment": records(segment.sort_values("revenue", ascending=False)), "products": records(product), "channel": records(channel.sort_values("revenue", ascending=False)), "discount": records(discount), "status": records(status)})


@app.get("/api/insights")
def insights():
    df = apply_filters(load_data()); sales = completed(df)
    if sales.empty: return jsonify({"items": []})
    category = sales.groupby("Category").agg(revenue=("Sales_Calculated","sum"), profit=("Profit_Calculated","sum"))
    category["margin"] = category.profit / category.revenue * 100
    region = sales.groupby("Region").agg(revenue=("Sales_Calculated","sum"), profit=("Profit_Calculated","sum"))
    region["margin"] = region.profit / region.revenue * 100
    segment = sales.groupby("Customer_Segment").agg(revenue=("Sales_Calculated","sum"), orders=("Order_ID","nunique"))
    segment["aov"] = segment.revenue / segment.orders
    best_cat, best_reg = category.revenue.idxmax(), region.revenue.idxmax()
    items = [
        {"type":"Category", "title":f"{best_cat} leads revenue", "text":f"{best_cat} contributes ₹{category.loc[best_cat,'revenue']:,.0f} with a {category.loc[best_cat,'margin']:.1f}% margin."},
        {"type":"Region", "title":f"{best_reg} is the strongest region", "text":f"{best_reg} generates ₹{region.loc[best_reg,'revenue']:,.0f} and ₹{region.loc[best_reg,'profit']:,.0f} profit."},
        {"type":"Customer", "title":f"{segment.aov.idxmax()} has the highest AOV", "text":f"Average order value is ₹{segment.aov.max():,.0f}, making this segment worth closer basket-size analysis."},
    ]
    return jsonify({"items": items})


@app.get("/health")
def health():
    return {"status":"ok", "service":"RetailPulse Analytics"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
