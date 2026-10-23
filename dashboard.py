
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="IKEA Gifting Analytics",
    page_icon="📊",
    layout="wide"
)

folder = Path(__file__).parent

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    transactions = pd.read_csv(
        folder / "retail_cleaned.csv",
        parse_dates=["InvoiceDate"]
    )

    rfm = pd.read_csv(folder / "rfm_customer_segments.csv")

    transactions["Customer ID"] = (
        pd.to_numeric(transactions["Customer ID"], errors="coerce")
    )

    rfm["Customer ID"] = (
        pd.to_numeric(rfm["Customer ID"], errors="coerce")
    )

    transactions["Revenue"] = (
        transactions["Quantity"] * transactions["Price"]
    )

    transactions["InvoiceDate"] = pd.to_datetime(
        transactions["InvoiceDate"], errors="coerce"
    )

    rfm["Segment"] = rfm["Segment"].str.strip()

    return transactions, rfm


transactions, rfm = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("IKEA Gifting")
st.subheader("Customer Analytics & RFM Segmentation")
st.caption("Explore customer value, purchasing behaviour and inactivity.")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Dashboard Filters")

countries = sorted(transactions["Country"].dropna().unique())

selected_countries = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=["United Kingdom"] if "United Kingdom" in countries else countries[:1]
)

segments = sorted(rfm["Segment"].dropna().unique())

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    segments,
    default=segments
)

filtered_transactions = transactions[
    transactions["Country"].isin(selected_countries)
].copy()

country_customers = filtered_transactions["Customer ID"].dropna().unique()

filtered_rfm = rfm[
    (rfm["Customer ID"].isin(country_customers))
    & (rfm["Segment"].isin(selected_segments))
].copy()

# -----------------------------
# KPI CARDS
# -----------------------------
total_customers = filtered_rfm["Customer ID"].nunique()

total_revenue = filtered_transactions["Revenue"].sum()

churned_customers = (
    filtered_rfm["Recency"] > 90
).sum()

churn_rate = (
    churned_customers / len(filtered_rfm) * 100
    if len(filtered_rfm) > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Revenue", f"£{total_revenue:,.2f}")
col3.metric("Churned Customers", f"{churned_customers:,}")
col4.metric("Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# -----------------------------
# CUSTOMER DISTRIBUTION
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("Customer Distribution")

    segment_counts = (
        filtered_rfm["Segment"]
        .value_counts()
        .rename_axis("Segment")
        .reset_index(name="Customers")
    )

    fig1 = px.bar(
        segment_counts,
        x="Segment",
        y="Customers",
        color="Segment",
        title="Customers by Segment"
    )

    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.subheader("Average Spend by Segment")

    segment_value = (
        filtered_rfm.groupby("Segment", as_index=False)["Monetary"]
        .mean()
        .sort_values("Monetary", ascending=False)
    )

    fig2 = px.bar(
        segment_value,
        x="Segment",
        y="Monetary",
        color="Segment",
        title="Average Customer Value"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# MONTHLY REVENUE TRENDS
# -----------------------------
st.divider()
st.subheader("Monthly Revenue Trends")

if not filtered_transactions.empty:
    filtered_transactions["Month"] = (
        filtered_transactions["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_revenue = (
        filtered_transactions.groupby("Month", as_index=False)["Revenue"]
        .sum()
    )

    fig3 = px.line(
        monthly_revenue,
        x="Month",
        y="Revenue",
        markers=True,
        title="Revenue by Month"
    )

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No transactions available for the selected country.")

# -----------------------------
# CHURN ANALYSIS
# -----------------------------
st.divider()
st.subheader("Customer Churn Analysis")

if not filtered_rfm.empty:
    churn_data = filtered_rfm.copy()

    churn_data["Status"] = churn_data["Recency"].apply(
        lambda days: "Churned" if days > 90 else "Active"
    )

    churn_summary = (
        churn_data["Status"]
        .value_counts()
        .rename_axis("Status")
        .reset_index(name="Customers")
    )

    fig4 = px.pie(
        churn_summary,
        names="Status",
        values="Customers",
        hole=0.45,
        title="Active vs Churned Customers"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.caption(
        "Churn definition used here: more than 90 days since last purchase."
    )
else:
    st.info("No customers available for the selected filters.")

# -----------------------------
# CUSTOMER RFM TABLE
# -----------------------------
st.divider()
st.subheader("Customer RFM Details")

columns = [
    "Customer ID",
    "Recency",
    "Frequency",
    "Monetary",
    "R_Score",
    "F_Score",
    "M_Score",
    "Segment"
]

st.dataframe(
    filtered_rfm[columns],
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# DOWNLOAD REPORT
# -----------------------------
csv_data = filtered_rfm.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="Download Customer RFM Report",
    data=csv_data,
    file_name="ikea_customer_rfm_report.csv",
    mime="text/csv"
)
