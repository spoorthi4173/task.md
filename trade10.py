# Load the data (each script runs in its own Python session)
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")
df["price"] = pd.to_numeric(
    df["price"].astype(str).str.replace(r"[$,]", "", regex=True),
    errors="coerce"
)

def parse_timestamp(value):
    value = str(value).strip()
    if value.isdigit():
        if len(value) >= 13:
            return pd.to_datetime(int(value), unit="ms", errors="coerce")
        if len(value) == 10:
            return pd.to_datetime(int(value), unit="s", errors="coerce")
    return pd.to_datetime(value, errors="coerce", dayfirst=True)

df["timestamp"] = df["timestamp"].apply(parse_timestamp)
df = df.dropna(subset=["timestamp", "price"])
df = df.sort_values("timestamp").set_index("timestamp")

df["price"].plot(figsize=(10, 4), title="Price Line Chart")
plt.xlabel("Time")
plt.ylabel("Price")
plt.show()
