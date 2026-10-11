# Load the dataset (each script has its own Python session)
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# The CSV has dirty values, so convert these fields to numbers and treat
# non-numeric entries as missing before calculating statistics.
for column in ["price", "quantity"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Statistical summary
print(df.describe(include="all"))

# Count buy and sell trades
print(df["side"].value_counts(dropna=False))

# Count symbols
print(df["symbol"].value_counts(dropna=False))

# Price statistics
print("Price minimum:", df["price"].min())
print("Price maximum:", df["price"].max())
print("Price mean:", df["price"].mean())
print("Price median:", df["price"].median())

# Quantity statistics
print("Quantity minimum:", df["quantity"].min())
print("Quantity maximum:", df["quantity"].max())
print("Quantity mean:", df["quantity"].mean())
print("Quantity median:", df["quantity"].median())
