# Load data and required libraries (each script runs in its own session)
import numpy as np
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# Convert fields used for feature engineering to numeric values.
numeric_cols = [
    "price", "quantity", "bid_price_1", "ask_price_1",
    "bid_qty_1", "ask_qty_1"
]
for column in numeric_cols:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce"
    )
df = df.dropna(subset=numeric_cols).copy()

# Add the market features calculated in trade8.py.
df["spread"] = df["ask_price_1"] - df["bid_price_1"]
df["mid_price"] = (df["ask_price_1"] + df["bid_price_1"]) / 2
total_qty = df["bid_qty_1"] + df["ask_qty_1"]
df["order_imbalance"] = np.where(
    total_qty > 0,
    (df["bid_qty_1"] - df["ask_qty_1"]) / total_qty,
    np.nan
)
df["returns"] = df["price"].pct_change()
df["rolling_volatility"] = df["returns"].rolling(10).std()
df["moving_average"] = df["price"].rolling(10).mean()

# Save the cleaned data with engineered features
df.to_csv("trading_data_cleaned.csv")

print("Cleaned dataset saved successfully!")
