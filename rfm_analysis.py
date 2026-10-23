
import pandas as pd
from pathlib import Path

# Load cleaned dataset
folder = Path(__file__).parent
file_path = folder / "retail_cleaned.csv"

df = pd.read_csv(file_path, parse_dates=["InvoiceDate"])

print("Starting RFM Analysis...")

# Calculate transaction revenue if needed
if "Revenue" not in df.columns:
    df["Revenue"] = df["Quantity"] * df["Price"]

# Set analysis date one day after the last transaction
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df.groupby("Customer ID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("Invoice", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

# Create RFM scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combined RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

# Assign customer segments
def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]

    if r >= 4 and f >= 4:
        return "Champions"
    elif r >= 3 and f >= 4:
        return "Loyal"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r >= 4 and f <= 2:
        return "New"
    elif r <= 2 and f <= 2:
        return "Lost"
    else:
        return "Needs Attention"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# Save customer-level RFM results
output_file = folder / "rfm_customer_segments.csv"
rfm.to_csv(output_file, index=False, encoding="utf-8-sig")

# Display results
print("\nRFM Analysis Completed!")
print("Total customers:", len(rfm))

print("\nCustomer segments:")
print(rfm["Segment"].value_counts())

print("\nAverage monetary value by segment:")
print(
    rfm.groupby("Segment")["Monetary"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\nSaved file:", output_file.name)
print("\nFirst five customer records:")
print(rfm.head())
# Churn Analysis: 90 days inactivity threshold
rfm["Churned"] = (rfm["Recency"] > 90).astype(int)

churned_customers = rfm["Churned"].sum()
total_customers = len(rfm)
churn_rate = (churned_customers / total_customers) * 100

print("\n--- Churn Analysis ---")
print("Total customers:", total_customers)
print("Churned customers:", churned_customers)
print("Churn rate:", round(churn_rate, 2), "%")

# Save updated RFM dataset
output_file = folder / "rfm_customer_segments.csv"
rfm.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\nUpdated RFM dataset saved successfully!")