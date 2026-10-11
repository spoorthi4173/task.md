# Load the dataset (each script runs in its own Python session)
import pandas as pd

df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")
df["price"] = pd.to_numeric(
    df["price"].astype(str).str.replace(r"[$,]", "", regex=True),
    errors="coerce"
)
df = df.dropna(subset=["price"])

# Calculate IQR
Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Display outlier count
outliers = df[
    (df["price"] < lower_limit) |
    (df["price"] > upper_limit)
]

print("Number of price outliers:", len(outliers))

# Remove extreme price outliers
df = df[
    (df["price"] >= lower_limit) &
    (df["price"] <= upper_limit)
].copy()

print("Rows after outlier removal:", len(df))
