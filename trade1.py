import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("trades_orderbook_STUDENT_dirty.csv")

# Display first five rows
print(df.head())

# Display number of rows and columns
print("Dataset shape:", df.shape)

# Display column information
df.info()

# Display data types
print(df.dtypes)