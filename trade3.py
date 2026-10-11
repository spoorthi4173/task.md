# Load pandas and the dataset (this script runs in its own Python session)
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# Remove $ and commas, then convert price to numbers
df["price"] = pd.to_numeric(
    df["price"].astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False),
    errors="coerce"
)

# Convert quantity to numbers
df["quantity"] = pd.to_numeric(
    df["quantity"], errors="coerce"
)

# Show the cleaned columns and their resulting data types
print(df[["price", "quantity"]].head())
print("\nCleaned column data types:")
print(df[["price", "quantity"]].dtypes)
