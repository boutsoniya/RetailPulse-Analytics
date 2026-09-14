"""Baseline monthly revenue forecasting for RetailPulse.

This module intentionally uses a transparent time-series baseline (linear trend
with month-of-year features) so the methodology can be explained in a viva.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "retail_transactions.csv"
OUTPUT_DIR = ROOT / "data" / "processed"


def main() -> None:
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    monthly = (
        df.set_index("order_date")["revenue"]
        .resample("MS")
        .sum()
        .rename("revenue")
        .reset_index()
    )

    monthly["t"] = np.arange(len(monthly))
    monthly["month"] = monthly["order_date"].dt.month
    X = pd.get_dummies(monthly[["t", "month"]], columns=["month"], dtype=float)
    y = monthly["revenue"]

    model = LinearRegression().fit(X, y)
    monthly["fitted_revenue"] = model.predict(X).round(2)

    future_dates = pd.date_range(
        monthly["order_date"].max() + pd.offsets.MonthBegin(1), periods=3, freq="MS"
    )
    future = pd.DataFrame({"order_date": future_dates})
    future["t"] = np.arange(len(monthly), len(monthly) + len(future))
    future["month"] = future["order_date"].dt.month
    future_X = pd.get_dummies(future[["t", "month"]], columns=["month"], dtype=float)
    future_X = future_X.reindex(columns=X.columns, fill_value=0)
    future["forecast_revenue"] = model.predict(future_X).round(2)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    monthly[["order_date", "revenue", "fitted_revenue"]].to_csv(
        OUTPUT_DIR / "monthly_revenue_forecast_history.csv", index=False
    )
    future.to_csv(OUTPUT_DIR / "revenue_forecast_next_3_months.csv", index=False)

    print("Next 3 months revenue forecast:")
    print(future[["order_date", "forecast_revenue"]].to_string(index=False))


if __name__ == "__main__":
    main()
