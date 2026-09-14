"""Customer RFM segmentation for the RetailPulse case study."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "retail_sales_clean.csv"
OUTPUT = ROOT / "data" / "processed" / "customer_rfm_segments.csv"


def main():
    if not INPUT.exists():
        from python.prepare_data import main as prepare
        prepare()
    df = pd.read_csv(INPUT, parse_dates=["Order_Date"])
    df = df[df["Order_Status"] == "Completed"].copy()
    snapshot = df["Order_Date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("Customer_ID").agg(
        Recency=("Order_Date", lambda x: (snapshot - x.max()).days),
        Frequency=("Order_ID", "nunique"),
        Monetary=("Sales_Calculated", "sum"),
    ).reset_index()
    # Rank-based quintiles avoid failure when many values share the same boundary.
    rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"), 5, labels=[5,4,3,2,1]).astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    total = rfm.R_Score + rfm.F_Score + rfm.M_Score
    rfm["Segment"] = pd.cut(total, [-1,5,8,11,13,15], labels=["Needs Attention","At Risk","Potential Loyalist","Loyal Customer","Champion"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(OUTPUT, index=False)
    print(rfm["Segment"].value_counts().to_string())
    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()
