"""
Pandas Data Analysis — Sales Dataset
======================================
Demonstrates beginner-level data analysis workflows:
  1. Load data
  2. Clean data (missing values, duplicates, data types)
  3. Explore data (shape, dtypes, summary statistics)
  4. Analyse patterns and trends
  5. Visualise key insights (saved as PNG files)
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (no display required)
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATA_FILE = os.path.join("data", "sales_data.csv")

# ---------------------------------------------------------------------------
# 1. Load Data
# ---------------------------------------------------------------------------
print("=" * 60)
print("1. LOADING DATA")
print("=" * 60)

df = pd.read_csv(DATA_FILE, parse_dates=["date"])
print(f"Dataset loaded: {DATA_FILE}")
print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n")

# ---------------------------------------------------------------------------
# 2. Data Cleaning
# ---------------------------------------------------------------------------
print("=" * 60)
print("2. DATA CLEANING")
print("=" * 60)

# 2a. Inspect missing values
print("Missing values per column:")
print(df.isnull().sum())

missing_count = df.isnull().sum().sum()
print(f"\nTotal missing values: {missing_count}")

# 2b. Fill missing quantity with median (robust to outliers)
median_qty = df["quantity"].median()
df["quantity"] = df["quantity"].fillna(median_qty)
print(f"\nFilled {missing_count} missing 'quantity' value(s) with median ({median_qty})")

# 2c. Remove duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates()
print(f"Duplicate rows removed: {duplicates}")

# 2d. Derive revenue column
df["revenue"] = df["quantity"] * df["unit_price"]
print("\nDerived column 'revenue' = quantity × unit_price")

# 2e. Extract month label for time-series analysis
df["month"] = df["date"].dt.to_period("M").astype(str)
print("Derived column 'month' from 'date'\n")

# ---------------------------------------------------------------------------
# 3. Data Exploration
# ---------------------------------------------------------------------------
print("=" * 60)
print("3. DATA EXPLORATION")
print("=" * 60)

print("\nColumn data types:")
print(df.dtypes)

print("\nSummary statistics (numeric columns):")
print(df[["quantity", "unit_price", "revenue", "customer_age"]].describe().round(2))

print("\nUnique values per categorical column:")
for col in ["product", "category", "region", "customer_gender"]:
    print(f"  {col}: {df[col].nunique()} unique — {df[col].unique().tolist()}")

# ---------------------------------------------------------------------------
# 4. Analysis — Patterns & Trends
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("4. ANALYSIS — PATTERNS & TRENDS")
print("=" * 60)

# 4a. Revenue by category
print("\nRevenue by category:")
rev_by_cat = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
rev_by_cat.columns = ["category", "total_revenue"]
print(rev_by_cat.to_string(index=False))

# 4b. Top 5 products by revenue
print("\nTop 5 products by total revenue:")
top_products = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)
top_products.columns = ["product", "total_revenue"]
print(top_products.to_string(index=False))

# 4c. Monthly revenue trend
print("\nMonthly revenue:")
monthly = (
    df.groupby("month")["revenue"]
    .sum()
    .reset_index()
)
monthly.columns = ["month", "total_revenue"]
print(monthly.to_string(index=False))

# 4d. Revenue by region
print("\nRevenue by region:")
rev_by_region = (
    df.groupby("region")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
rev_by_region.columns = ["region", "total_revenue"]
print(rev_by_region.to_string(index=False))

# 4e. Average order revenue by customer gender
print("\nAverage revenue per transaction by gender:")
avg_rev_gender = df.groupby("customer_gender")["revenue"].mean().reset_index()
avg_rev_gender.columns = ["gender", "avg_revenue"]
print(avg_rev_gender.to_string(index=False))

# 4f. Correlation between customer age and revenue
corr = df["customer_age"].corr(df["revenue"])
print(f"\nCorrelation — customer_age vs revenue: {corr:.3f}")

# ---------------------------------------------------------------------------
# 5. Visualisations
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("5. VISUALISATIONS")
print("=" * 60)

# Helper to save and announce each figure
def save_fig(name: str) -> None:
    path = os.path.join(OUTPUT_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"  Saved: {path}")


# 5a. Bar chart — Revenue by category
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(rev_by_cat["category"], rev_by_cat["total_revenue"], color="steelblue")
ax.set_title("Total Revenue by Category")
ax.set_xlabel("Category")
ax.set_ylabel("Revenue ($)")
save_fig("revenue_by_category.png")

# 5b. Horizontal bar chart — Top products
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(top_products["product"][::-1], top_products["total_revenue"][::-1], color="darkorange")
ax.set_title("Top 5 Products by Revenue")
ax.set_xlabel("Revenue ($)")
save_fig("top_products.png")

# 5c. Line chart — Monthly revenue trend
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["total_revenue"], marker="o", color="seagreen", linewidth=2)
ax.set_title("Monthly Revenue Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.tick_params(axis="x", rotation=30)
save_fig("monthly_revenue_trend.png")

# 5d. Bar chart — Revenue by region
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(rev_by_region["region"], rev_by_region["total_revenue"], color="mediumpurple")
ax.set_title("Total Revenue by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Revenue ($)")
save_fig("revenue_by_region.png")

# 5e. Histogram — Customer age distribution
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df["customer_age"], bins=10, color="tomato", edgecolor="white")
ax.set_title("Customer Age Distribution")
ax.set_xlabel("Age")
ax.set_ylabel("Number of Transactions")
save_fig("customer_age_distribution.png")

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
total_revenue = df["revenue"].sum()
total_orders = len(df)
best_category = rev_by_cat.iloc[0]["category"]
best_product = top_products.iloc[0]["product"]
best_region = rev_by_region.iloc[0]["region"]

print(f"  Total transactions analysed : {total_orders}")
print(f"  Total revenue               : ${total_revenue:,.2f}")
print(f"  Best-performing category    : {best_category}")
print(f"  Best-selling product        : {best_product}")
print(f"  Top revenue region          : {best_region}")
print("\nAnalysis complete. Charts saved to the 'output/' directory.")
