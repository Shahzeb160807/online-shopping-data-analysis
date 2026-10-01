# pandas for data read and data analyze.
import pandas as pd
import matplotlib.pyplot as plt
#csv load
df = pd.read_csv("data/Ecommerce_data.csv")    #pandas will read that file and execute .
#payment type add 
import pandas as pd
import random

# CSV load
df = pd.read_csv("data/Ecommerce_data.csv")

# Payment Type add
payment_methods = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery"]

df["payment_type"] = [
    random.choice(payment_methods)
    for _ in range(len(df))
]

# New CSV save
df.to_csv("data/Ecommerce_data_with_payment.csv", index=False)

print("Payment column added successfully!")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())

print(df.head())
print(df.shape)
print(df.columns.tolist())
product_sales = (
    df.groupby("product_name")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Products by Sales:")
print(product_sales.head(10))
print(df.info())
print(df.isnull().sum())   #for checking missing value .
print("Duplicate rows:", df.duplicated().sum())
df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    errors="coerce"
)
print(df["order_date"].head())
print("Total Sales:")
print(df["sales_per_order"].sum())  #sales on per order.
category_sales = (
    df.groupby("category_name")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Category:")
print(category_sales)
print("\nTotal Orders:")
print(len(df))
print("\nAverage Sales per Order:")
print(df["sales_per_order"].mean())
print("\nHighest Order Sales:")
print(df["sales_per_order"].max())
print("\nLowest Order Sales:")
print(df["sales_per_order"].min())
df["month"] = df["order_date"].dt.to_period("M")

monthly_sales = (
    df.groupby("month")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

print("\nMonthly Sales:")
print(monthly_sales)
plt.figure(figsize=(10, 5))

category_sales.plot(kind="bar")

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 6))

monthly_sales.sort_index().plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
top_products = product_sales.head(10)

plt.figure(figsize=(10, 6))

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product")

plt.tight_layout()
plt.show()
april_2021 = df[
    df["order_date"].dt.to_period("M") == "2021-04"
]

print("\nApril 2021 Analysis:")
print("Total Orders:", len(april_2021))
print("Total Sales:", april_2021["sales_per_order"].sum())
print("Average Order Value:", april_2021["sales_per_order"].mean())
april_category_sales = (
    april_2021.groupby("category_name")["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

print("\nApril 2021 Sales by Category:")
print(april_category_sales)
plt.figure(figsize=(10, 5))

april_category_sales.plot(kind="bar")

plt.title("April 2021 Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
print(df.columns.tolist())
customer_sales = (
    df.groupby(
        ["customer_id", "customer_first_name", "customer_last_name"]
    )["sales_per_order"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Customers by Sales:")
print(customer_sales.head(10))
top_customers = customer_sales.head(10)

# Customer names ko readable format mein convert karna
top_customers.index = [
    first + " " + last
    for customer_id, first, last in top_customers.index
]
plt.figure(figsize=(10, 6))

top_customers.sort_values().plot(kind="barh")

plt.title("Top 10 Customers by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Customer")

plt.tight_layout()
plt.show()
category_profit = (
    df.groupby("category_name")["profit_per_order"]
    .sum()
    .sort_values(ascending=False)
)

print("\nProfit by Category:")
print(category_profit)
category_performance = df.groupby("category_name").agg(
    Total_Sales=("sales_per_order", "sum"),
    Total_Profit=("profit_per_order", "sum"),
    Total_Orders=("order_id", "count")
)

category_performance = category_performance.sort_values(
    "Total_Sales",
    ascending=False
)

print("\nCategory Performance:")
print(category_performance)
most_profitable_category = category_performance["Total_Profit"].idxmax()
highest_profit = category_performance["Total_Profit"].max()

print("\nMost Profitable Category:", most_profitable_category)
print("Highest Profit:", highest_profit)
delivery_analysis = df["delivery_status"].value_counts()

print("\nDelivery Status:")
print(delivery_analysis)
plt.figure(figsize=(10, 5))

delivery_analysis.plot(kind="bar")

plt.title("Delivery Status Analysis")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
shipping_analysis = df["shipping_type"].value_counts()

print("\nShipping Type:")
print(shipping_analysis)
# Shipping Type Analysis

shipping_analysis = df["shipping_type"].value_counts()

print("\nShipping Type Analysis:")
print(shipping_analysis)

plt.figure(figsize=(10, 6))
shipping_analysis.plot(kind="bar")

plt.title("Shipping Type Analysis")
plt.xlabel("Shipping Type")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#costumer analysis
customer_sales = df.groupby(
    ["customer_id", "customer_first_name", "customer_last_name"]
)["sales_per_order"].sum().sort_values(ascending=False).head(10)

print("Top 10 Customers by Sales:")
print(customer_sales)
print(df.columns.tolist())
# Profit Analysis

total_profit = df["profit_per_order"].sum()

print("\nTotal Profit:")
print(total_profit)

monthly_profit = df.groupby(
    df["order_date"].dt.to_period("M")
)["profit_per_order"].sum()

print("\nMonthly Profit:")
print(monthly_profit)

plt.figure(figsize=(10, 6))
monthly_profit.plot(kind="line", marker="o")

plt.title("Monthly Profit Trend")
plt.xlabel("Month")
plt.ylabel("Total Profit")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Payment Analysis
payment_analysis = df["payment_type"].value_counts()

print("\nPayment Type Analysis:")
print(payment_analysis)

plt.figure(figsize=(8, 5))
payment_analysis.plot(kind="bar")

plt.title("Payment Type Analysis")
plt.xlabel("Payment Type")
plt.ylabel("Number of Orders")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()