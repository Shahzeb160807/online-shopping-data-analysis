# =========================================================
# ONLINE SHOPPING DATA ANALYSIS DASHBOARD
# =========================================================

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import random

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Online Shopping Analytics",
    page_icon="🛒",
    layout="wide"
)

# =========================================================
# DASHBOARD HEADER
# =========================================================

st.markdown("""
<div style="
    background: linear-gradient(90deg,#0f2027,#203a43,#2c5364);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
">
    <h1 style="color:white; margin:0;">
        🛒 ONLINE SHOPPING DATA ANALYSIS
    </h1>
    <p style="color:white; font-size:18px; margin-top:10px;">
        📊 Sales • Products • Customers • Profit • Payment • Delivery
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LOAD CSV
# =========================================================

df = pd.read_csv("data/Ecommerce_data.csv")

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# =========================================================
# PAYMENT TYPE
# =========================================================

payment_methods = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Cash on Delivery"
]

# Payment column create
random.seed(10)

df["payment_type"] = [
    random.choice(payment_methods)
    for _ in range(len(df))
]

# Save payment dataset
df.to_csv(
    "data/Ecommerce_data_with_payment.csv",
    index=False
)

# =========================================================
# DATE
# =========================================================

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce",
    format="mixed"
)

# =========================================================
# BASIC ANALYSIS
# =========================================================

total_orders = len(df)

total_sales = df["sales_per_order"].sum()

total_profit = df["profit_per_order"].sum()

average_order = df["sales_per_order"].mean()

# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📌 Business Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🛍️ Total Orders",
    f"{total_orders:,}"
)

c2.metric(
    "💰 Total Sales",
    f"{total_sales:,.2f}"
)

c3.metric(
    "📈 Total Profit",
    f"{total_profit:,.2f}"
)

c4.metric(
    "🧾 Average Order",
    f"{average_order:,.2f}"
)

st.divider()

# =========================================================
# 1. SALES BY CATEGORY
# =========================================================

st.header("📊 Sales Analysis")

st.subheader("Sales by Category")

category_sales = (
    df.groupby("category_name")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 5))

category_sales.plot(
    kind="bar",
    ax=ax1
)

ax1.set_title("Sales by Category")
ax1.set_xlabel("Category")
ax1.set_ylabel("Total Sales")
ax1.tick_params(axis="x", rotation=45)

fig1.tight_layout()

st.pyplot(fig1)

plt.close(fig1)

# =========================================================
# 2. MONTHLY SALES
# =========================================================

st.subheader("📈 Monthly Sales Trend")

df["month"] = df["order_date"].dt.to_period("M")

monthly_sales = (
    df.groupby("month")["sales_per_order"]
    .sum()
    .sort_index()
)

fig2, ax2 = plt.subplots(figsize=(12, 5))

monthly_sales.plot(
    kind="line",
    marker="o",
    ax=ax2
)

ax2.set_title("Monthly Sales Trend")
ax2.set_xlabel("Month")
ax2.set_ylabel("Total Sales")
ax2.tick_params(axis="x", rotation=45)

fig2.tight_layout()

st.pyplot(fig2)

plt.close(fig2)

# =========================================================
# 3. TOP 10 PRODUCTS
# =========================================================

st.subheader("🏆 Top 10 Products by Sales")

product_sales = (
    df.groupby("product_name")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

top_products = product_sales.head(10)

fig3, ax3 = plt.subplots(figsize=(10, 6))

top_products.sort_values().plot(
    kind="barh",
    ax=ax3
)

ax3.set_title("Top 10 Products by Sales")
ax3.set_xlabel("Total Sales")
ax3.set_ylabel("Product")

fig3.tight_layout()

st.pyplot(fig3)

plt.close(fig3)

# =========================================================
# 4. APRIL 2021 ANALYSIS
# =========================================================

st.subheader("📅 April 2021 Sales Analysis")

april_2021 = df[
    df["order_date"].dt.to_period("M") == "2021-04"
]

april_orders = len(april_2021)

april_sales = april_2021["sales_per_order"].sum()

april_average = april_2021["sales_per_order"].mean()

a1, a2, a3 = st.columns(3)

a1.metric(
    "April Orders",
    f"{april_orders:,}"
)

a2.metric(
    "April Sales",
    f"{april_sales:,.2f}"
)

a3.metric(
    "Average Order",
    f"{april_average:,.2f}"
)

april_category_sales = (
    april_2021
    .groupby("category_name")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

fig4, ax4 = plt.subplots(figsize=(10, 5))

april_category_sales.plot(
    kind="bar",
    ax=ax4
)

ax4.set_title("April 2021 Sales by Category")
ax4.set_xlabel("Category")
ax4.set_ylabel("Total Sales")
ax4.tick_params(axis="x", rotation=45)

fig4.tight_layout()

st.pyplot(fig4)

plt.close(fig4)

# =========================================================
# 5. TOP CUSTOMERS
# =========================================================

st.header("👥 Customer Analysis")

customer_sales = (
    df.groupby(
        [
            "customer_id",
            "customer_first_name",
            "customer_last_name"
        ]
    )["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Make a separate dataframe
customer_df = customer_sales.reset_index()

customer_df["customer_name"] = (
    customer_df["customer_first_name"].astype(str)
    + " "
    + customer_df["customer_last_name"].astype(str)
)

fig5, ax5 = plt.subplots(figsize=(10, 6))

ax5.barh(
    customer_df["customer_name"].iloc[::-1],
    customer_df["sales_per_order"].iloc[::-1]
)

ax5.set_title("Top 10 Customers by Sales")
ax5.set_xlabel("Total Sales")
ax5.set_ylabel("Customer")

fig5.tight_layout()

st.pyplot(fig5)

plt.close(fig5)

# =========================================================
# 6. PROFIT BY CATEGORY
# =========================================================

st.header("💰 Profit Analysis")

category_profit = (
    df.groupby("category_name")["profit_per_order"]
    .sum()
    .sort_values(ascending=False)
)

fig6, ax6 = plt.subplots(figsize=(10, 5))

category_profit.plot(
    kind="bar",
    ax=ax6
)

ax6.set_title("Profit by Category")
ax6.set_xlabel("Category")
ax6.set_ylabel("Total Profit")
ax6.tick_params(axis="x", rotation=45)

fig6.tight_layout()

st.pyplot(fig6)

plt.close(fig6)

# =========================================================
# 7. CATEGORY PERFORMANCE TABLE
# =========================================================

st.subheader("📋 Category Performance")

category_performance = df.groupby("category_name").agg(
    Total_Sales=("sales_per_order", "sum"),
    Total_Profit=("profit_per_order", "sum"),
    Total_Orders=("order_id", "count")
)

category_performance = category_performance.sort_values(
    "Total_Sales",
    ascending=False
)

st.dataframe(
    category_performance,
    use_container_width=True
)

# =========================================================
# MOST PROFITABLE CATEGORY
# =========================================================

most_profitable_category = (
    category_performance["Total_Profit"].idxmax()
)

highest_profit = (
    category_performance["Total_Profit"].max()
)

st.info(
    f"💡 Most Profitable Category: "
    f"**{most_profitable_category}** "
    f"with profit **{highest_profit:,.2f}**"
)

# =========================================================
# 8. DELIVERY STATUS
# =========================================================

st.header("🚚 Delivery & Shipping Analysis")

delivery_analysis = (
    df["delivery_status"]
    .value_counts()
)

st.subheader("Delivery Status")

fig7, ax7 = plt.subplots(figsize=(10, 5))

delivery_analysis.plot(
    kind="bar",
    ax=ax7
)

ax7.set_title("Delivery Status Analysis")
ax7.set_xlabel("Delivery Status")
ax7.set_ylabel("Number of Orders")
ax7.tick_params(axis="x", rotation=45)

fig7.tight_layout()

st.pyplot(fig7)

plt.close(fig7)

# =========================================================
# 9. SHIPPING TYPE
# =========================================================

st.subheader("📦 Shipping Type")

shipping_analysis = (
    df["shipping_type"]
    .value_counts()
)

fig8, ax8 = plt.subplots(figsize=(10, 5))

shipping_analysis.plot(
    kind="bar",
    ax=ax8
)

ax8.set_title("Shipping Type Analysis")
ax8.set_xlabel("Shipping Type")
ax8.set_ylabel("Number of Orders")
ax8.tick_params(axis="x", rotation=45)

fig8.tight_layout()

st.pyplot(fig8)

plt.close(fig8)

# =========================================================
# 10. MONTHLY PROFIT
# =========================================================

st.header("📈 Monthly Profit Analysis")

monthly_profit = (
    df.groupby(
        df["order_date"].dt.to_period("M")
    )["profit_per_order"]
    .sum()
    .sort_index()
)

fig9, ax9 = plt.subplots(figsize=(12, 5))

monthly_profit.plot(
    kind="line",
    marker="o",
    ax=ax9
)

ax9.set_title("Monthly Profit Trend")
ax9.set_xlabel("Month")
ax9.set_ylabel("Total Profit")
ax9.tick_params(axis="x", rotation=45)

fig9.tight_layout()

st.pyplot(fig9)

plt.close(fig9)

# =========================================================
# 11. PAYMENT ANALYSIS
# =========================================================

st.header("💳 Payment Analysis")

payment_analysis = (
    df["payment_type"]
    .value_counts()
)

fig10, ax10 = plt.subplots(figsize=(9, 5))

payment_analysis.plot(
    kind="bar",
    ax=ax10
)

ax10.set_title("Payment Type Analysis")
ax10.set_xlabel("Payment Type")
ax10.set_ylabel("Number of Orders")
ax10.tick_params(axis="x", rotation=45)

fig10.tight_layout()

st.pyplot(fig10)

plt.close(fig10)

# =========================================================
# PAYMENT TABLE
# =========================================================

st.subheader("💳 Payment Summary")

payment_table = payment_analysis.reset_index()

payment_table.columns = [
    "Payment Type",
    "Number of Orders"
]

st.dataframe(
    payment_table,
    use_container_width=True
)

# =========================================================
# DATASET PREVIEW
# =========================================================

st.header("📄 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# =========================================================
# FINAL
# =========================================================

st.divider()

st.success(
    "✅ Online Shopping Data Analysis Dashboard Completed Successfully!"
)