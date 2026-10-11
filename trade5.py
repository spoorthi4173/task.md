# Load the libraries and dataset (each script runs in its own Python session)
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# Work on a copy
df = df.copy()

# Remove duplicate trade IDs
df = df.drop_duplicates(subset="trade_id", keep="first")

# Standardize side labels
df["side"] = df["side"].astype("string").str.strip().str.lower()
df["side"] = df["side"].replace({
    "buy": "buy",
    "sell": "sell"
})

# Standardize symbol names
df["symbol"] = (
    df["symbol"].astype("string").str.strip().str.upper()
    .str.replace("/", "", regex=False)
    .str.replace("-", "", regex=False)
)

# Convert price text to numeric
df["price"] = pd.to_numeric(
    df["price"].astype(str).str.replace(
        r"[$,]", "", regex=True
    ),
    errors="coerce"
)

# Convert quantity and order book columns to numeric
numeric_cols = [
    "quantity", "bid_price_1", "bid_qty_1",
    "bid_price_2", "bid_qty_2", "bid_price_3", "bid_qty_3",
    "ask_price_1", "ask_qty_1",
    "ask_price_2", "ask_qty_2", "ask_price_3", "ask_qty_3"
]

df[numeric_cols] = df[numeric_cols].apply(
    pd.to_numeric, errors="coerce"
)

# Convert different timestamp formats
def parse_timestamp(value):
    value = str(value).strip()

    if value.isdigit():
        if len(value) >= 13:
            return pd.to_datetime(
                int(value), unit="ms", errors="coerce"
            )
        elif len(value) == 10:
            return pd.to_datetime(
                int(value), unit="s", errors="coerce"
            )

    return pd.to_datetime(value, errors="coerce", dayfirst=True)

df["timestamp"] = df["timestamp"].apply(parse_timestamp)

# Remove rows with missing essential values
required = [
    "trade_id", "timestamp", "symbol", "side", "price",
    "quantity", "bid_price_1", "ask_price_1",
    "bid_qty_1", "ask_qty_1"
]

df = df.dropna(subset=required)

# Keep valid trade sides
df = df[df["side"].isin(["buy", "sell"])]

# Remove negative or zero trade prices and quantities
df = df[(df["price"] > 0) & (df["quantity"] > 0)]

# Remove invalid top-of-book prices and negative quantities
book_prices = [
    "bid_price_1", "bid_price_2", "bid_price_3",
    "ask_price_1", "ask_price_2", "ask_price_3"
]
book_qty = [
    "bid_qty_1", "bid_qty_2", "bid_qty_3",
    "ask_qty_1", "ask_qty_2", "ask_qty_3"
]

df = df[(df[book_prices] > 0).all(axis=1)]
df = df[(df[book_qty] >= 0).all(axis=1)]

# Remove crossed order books: best bid above best ask
df = df[df["bid_price_1"] <= df["ask_price_1"]]

# Sort by timestamp
df = df.sort_values("timestamp").reset_index(drop=True)

print("Rows after cleaning:", len(df))
print("Missing values:\n", df.isnull().sum())
