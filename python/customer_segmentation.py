"""RFM-style customer segmentation for RetailPulse."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "retail_transactions.csv"
OUTPUT_DIR = ROOT / "data" / "processed"


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)

    rfm = (
        df.groupby("customer_id")
        .agg(
            recency=("order_date", lambda x: (snapshot_date - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("revenue", "sum"),
        )
        .reset_index()
    )

    # Rank into five quantiles where possible; duplicate edges are handled safely.
    rfm["R_score"] = pd.qcut(rfm["recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["M_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm["RFM_score"] = rfm[["R_score", "F_score", "M_score"]].sum(axis=1)

    def segment(score: int) -> str:
        if score >= 13:
            return "Champions"
        if score >= 10:
            return "Loyal Customers"
        if score >= 7:
            return "Potential Loyalists"
        if score >= 5:
            return "At Risk"
        return "Needs Attention"

    rfm["segment"] = rfm["RFM_score"].map(segment)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(OUTPUT_DIR / "customer_rfm_segments.csv", index=False)

    print("Customer segments:")
    print(rfm["segment"].value_counts())


if __name__ == "__main__":
    main()
