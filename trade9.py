# Load and prepare the data (each script runs in its own Python session)
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")
df["price"] = pd.to_numeric(
    df["price"].astype(str).str.replace(r"[$,]", "", regex=True),
    errors="coerce"
)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

def parse_timestamp(value):
    value = str(value).strip()
    if value.isdigit():
        if len(value) >= 13:
            return pd.to_datetime(int(value), unit="ms", errors="coerce")
        if len(value) == 10:
            return pd.to_datetime(int(value), unit="s", errors="coerce")
    return pd.to_datetime(value, errors="coerce", dayfirst=True)

df["timestamp"] = df["timestamp"].apply(parse_timestamp)
df = df.dropna(subset=["timestamp", "price", "quantity"])

# Set timestamp as index
df = df.sort_values("timestamp")
df = df.set_index("timestamp")

# Create 1-minute candles
candles = df.resample("1min").agg(
    open=("price", "first"),
    high=("price", "max"),
    low=("price", "min"),
    close=("price", "last"),
    volume=("quantity", "sum")
)

# Remove empty minutes
candles = candles.dropna(subset=["open", "high", "low", "close"])

print(candles.head())

# Save candles
candles.to_csv("trading_1minute_candles.csv")
