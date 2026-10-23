
import pandas as pd
from pathlib import Path

# 1. Project folder
folder = Path(__file__).parent

file1 = folder / "online_retail_II page 1.csv"
file2 = folder / "online_retail_II page 2.csv"

print("Loading IKEA Gifting dataset...")

# 2. Load both CSV files
df1 = pd.read_csv(file1, encoding="cp1252")
df2 = pd.read_csv(file2, encoding="cp1252")

# 3. Combine datasets
df = pd.concat([df1, df2], ignore_index=True)

print("\nOriginal dataset shape:", df.shape)

# 4. Remove exact duplicate rows
df = df.drop_duplicates()

# 5. Remove transactions without Customer ID
df = df.dropna(subset=["Customer ID"]).copy()

# 6. Remove missing product descriptions
df = df.dropna(subset=["Description"]).copy()

# 7. Convert columns to appropriate data types
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

df["Customer ID"] = pd.to_numeric(
    df["Customer ID"], errors="coerce"
)

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

df["Price"] = pd.to_numeric(
    df["Price"], errors="coerce"
)

# 8. Remove invalid values
df = df.dropna(
    subset=["InvoiceDate", "Customer ID", "Quantity", "Price"]
).copy()

# 9. Keep positive quantity and price
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)].copy()

# 10. Calculate transaction revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# 11. Save cleaned dataset
output_file = folder / "retail_cleaned.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nData cleaning completed!")
print("Cleaned rows:", len(df))
print("Cleaned columns:", len(df.columns))
print("Total revenue:", round(df["Revenue"].sum(), 2))
print("Unique customers:", df["Customer ID"].nunique())
print("Saved cleaned dataset:", output_file.name)

print("\nRemaining missing values:")
print(df.isnull().sum())
