# Each script runs independently, so load pandas and the dataset here.
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# Missing values
print("Missing values:\n", df.isnull().sum())

# Duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# Duplicate trade IDs
print("Duplicate trade IDs:", df["trade_id"].duplicated().sum())

# Negative or zero prices and quantities
print("Negative prices:", (pd.to_numeric(
    df["price"].astype(str).str.replace(
        r"[$,]", "", regex=True
    ), errors="coerce") < 0).sum())

print("Zero quantities:", (pd.to_numeric(
    df["quantity"], errors="coerce") == 0).sum())

print("Negative quantities:", (pd.to_numeric(
    df["quantity"], errors="coerce") < 0).sum())
