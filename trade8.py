# Load libraries and data (each script runs in its own Python session)
import numpy as np
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# Convert fields used in the calculations to numbers; dirty entries become NaN.
numeric_cols = [
    "price", "bid_price_1", "ask_price_1", "bid_qty_1", "ask_qty_1"
]
for column in numeric_cols:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(r"[$,]", "", regex=True),
        errors="coerce"
    )
df = df.dropna(subset=numeric_cols).copy()

# Spread between best ask and best bid
df["spread"] = df["ask_price_1"] - df["bid_price_1"]

# Mid price
df["mid_price"] = (
    df["ask_price_1"] + df["bid_price_1"]
) / 2

# Order imbalance
total_qty = df["bid_qty_1"] + df["ask_qty_1"]

df["order_imbalance"] = np.where(
    total_qty > 0,
    (df["bid_qty_1"] - df["ask_qty_1"]) / total_qty,
    np.nan
)

# Price returns
df["returns"] = df["price"].pct_change()

# Rolling volatility over 10 observations
df["rolling_volatility"] = df["returns"].rolling(10).std()

# Moving average over 10 observations
df["moving_average"] = df["price"].rolling(10).mean()

print(df[[
    "price", "spread", "mid_price",
    "order_imbalance", "returns",
    "rolling_volatility", "moving_average"
]].head(15))
