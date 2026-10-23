# IKEA Gifting: Customer Analytics and RFM Segmentation

An end-to-end data analytics project using Python, Pandas, and Streamlit to analyse retail transactions, segment customers, and identify customers at risk of churn.

## Project Overview

This project analyses retail transaction data from the Online Retail II dataset. The goal is to understand customer purchasing behaviour, identify valuable customer segments, measure customer inactivity, and present business insights through an interactive dashboard.

The project uses Python for data cleaning, RFM analysis, customer segmentation, and churn analysis. Streamlit and Plotly are used to create an interactive dashboard with key performance indicators, charts, filters, and customer-level details.

**Note:** IKEA Gifting is a fictional project name used for educational purposes. This project is not affiliated with or endorsed by the real IKEA company.

## Business Problem

Retail businesses need to understand their customers to improve retention and increase revenue. Without customer segmentation, it can be difficult to identify high-value customers and customers who may stop purchasing.

This project uses transaction data to answer important business questions and support data-driven decisions.

## Business Questions

* Who are the most valuable customers?
* How frequently do customers purchase products?
* Which customer segments generate the highest average spending?
* Which customers have been inactive for more than 90 days?
* How does revenue change over time?
* How can businesses use customer segmentation to improve retention?

## Dataset

The project uses the Online Retail II transactional dataset.

The dataset contains approximately 1.07 million transaction records across two CSV files.

**Input files:**

* `online_retail_II page 1.csv`
* `online_retail_II page 2.csv`

The dataset includes invoice numbers, product codes, product descriptions, quantities, invoice dates, prices, customer IDs, and countries.

## Tech Stack

| Technology | Purpose                                        |
| ---------- | ---------------------------------------------- |
| Python     | Data processing and analysis                   |
| Pandas     | Data cleaning, transformation, and aggregation |
| NumPy      | Numerical operations                           |
| Plotly     | Interactive charts                             |
| Streamlit  | Interactive analytics dashboard                |
| CSV        | Data storage and exchange                      |
| VS Code    | Development environment                        |

## Project Workflow

### Step 1: Data Loading

Loaded both CSV files using Pandas and combined them into a single dataset.

The original dataset contains 1,067,371 rows and 8 columns.

### Step 2: Data Cleaning

Performed initial data cleaning using Python.

The process includes:

* Removing exact duplicate rows.
* Removing records with missing customer IDs.
* Removing records with missing product descriptions.
* Converting date and numerical columns to appropriate data types.
* Removing records with invalid dates or missing numerical values.
* Excluding transactions with non-positive quantities or prices.
* Calculating transaction revenue using quantity multiplied by price.

The cleaned dataset is saved as `retail_cleaned.csv`.

**Important:** These are the current Python cleaning rules. The original repository describes a separate SQL Server cleaning workflow, which has not yet been reproduced in this implementation.

### Step 3: RFM Analysis

RFM analysis is used to understand customer value through three metrics:

* **Recency:** Number of days since the customer's most recent purchase.
* **Frequency:** Number of distinct invoices associated with the customer.
* **Monetary:** Total transaction revenue associated with the customer.

Each customer receives a score from 1 to 5 for Recency, Frequency, and Monetary value.

The scores are combined to create an RFM score and assign customers to segments.

### Step 4: Customer Segmentation

Customers are grouped into six segments:

| Segment         | Description                                                       |
| --------------- | ----------------------------------------------------------------- |
| Champions       | Recent and frequent customers                                     |
| Loyal           | Customers with relatively high purchase frequency                 |
| At Risk         | Customers with lower recency scores and relatively high frequency |
| New             | Recently active customers with lower purchase frequency           |
| Needs Attention | Customers who may require additional engagement                   |
| Lost            | Customers with low recency and frequency scores                   |

The segmentation rules used in this implementation are initial analytical rules and may differ from the original repository's rules.

The output is saved as `rfm_customer_segments.csv`.

### Step 5: Churn Analysis

A customer is flagged as churned when the number of days since their last purchase exceeds 90 days.

This is an analytical inactivity definition, not a confirmed prediction that a customer will never return.

The dashboard displays the number and percentage of customers exceeding this threshold.

### Step 6: Interactive Dashboard

The dashboard is built using Streamlit and Plotly.

It includes:

* Total customers.
* Total revenue.
* Churned customer count.
* Churn rate.
* Customer distribution by segment.
* Average customer spending by segment.
* Monthly revenue trends.
* Active versus churned customer distribution.
* Country and customer-segment filters.
* Customer-level RFM details.
* CSV download for the filtered RFM report.

## Current Analysis Results

The current Python implementation produced the following results:

| Metric                                       |       Result |
| -------------------------------------------- | -----------: |
| Original transaction rows                    |    1,067,371 |
| Cleaned transaction rows                     |      316,481 |
| Customers in the cleaned dataset             |        4,277 |
| Churned customers using the 90-day threshold |        3,163 |
| Calculated churn rate                        |       73.95% |
| Calculated transaction revenue               | 7,239,050.62 |

Revenue is expressed in the dataset's currency, British pounds.

These figures reflect the current cleaning and segmentation implementation. They have not been validated against the original project's reported results.

## Project Structure

```text
data-analyst-project/
│
├── dashboard.py
├── ikea_analysis.py
├── rfm_analysis.py
│
├── online_retail_II page 1.csv
├── online_retail_II page 2.csv
│
├── retail_cleaned.csv
├── rfm_customer_segments.csv
│
├── IKEA Gifting BRD.docx
├── IKEA Project Theme.json
├── IKEA Dashboard as PDF.pdf
├── IKEA Home Page.png
├── IKEA Overview Page.png
├── IKEA RFM.png
│
└── README.md
```

## How to Run the Project

### 1. Install Python

Install Python and verify the installation:

```bash
python --version
```

### 2. Install the required libraries

Open a terminal in the project directory and run:

```bash
python -m pip install pandas numpy matplotlib seaborn jupyter streamlit plotly openpyxl
```

### 3. Run the data cleaning script

```bash
python ikea_analysis.py
```

This generates the cleaned dataset:

`retail_cleaned.csv`

### 4. Run RFM analysis

```bash
python rfm_analysis.py
```

This generates the customer segmentation file:

`rfm_customer_segments.csv`

### 5. Launch the dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in the terminal, typically:

`http://localhost:8501`

The dashboard requires the cleaned dataset and RFM output file to be available in the project directory.

## Future Improvements

* Reproduce the original SQL Server data-cleaning workflow.
* Validate the cleaned customer count against the original project.
* Refine RFM segmentation rules to match documented business definitions.
* Validate churn calculations against the original project methodology.
* Add quarterly and yearly revenue analysis.
* Improve dashboard design and business recommendations.
* Reproduce the original three-page Power BI dashboard.
* Add automated data-quality checks and analysis reports.

## Disclaimer

This is an educational data analytics implementation based on anonymized retail transaction data. The IKEA Gifting name and visual theme are used for portfolio and learning purposes only. This project is not affiliated with the real IKEA company.
