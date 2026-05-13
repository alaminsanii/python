import pandas as pd

# Create data using a dictionary
data = {
    'Date': ['2025-01-05', '2025-01-10', '2025-02-12', '2025-02-15', '2025-03-01', '2025-03-05'],
    'Product': ['Laptop', 'Phone', 'Laptop', 'Tablet', 'Phone', 'Laptop'],
    'Region': ['North', 'South', 'East', 'West', 'North', 'South'],
    'Sales': [1200, 800, 1500, 700, 900, 1600],
    'Quantity': [2, 5, 3, 1, 4, 2]
}

# Create pandas DataFrame
df = pd.DataFrame(data)

# Preview the data
print("Original DataFrame:")
print(df)

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Create 'Month' column
df['Month'] = df['Date'].dt.to_period('M')

# 1. Monthly total sales
monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()
print("\nMonthly Sales:")
print(monthly_sales)

# 2. Top products by total sales
top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
print("\nTop Products by Sales:")
print(top_products)

# 3. Sales by Region
region_sales = df.groupby('Region')['Sales'].sum()
print("\nSales by Region: ")
print(region_sales)

# 4. Average quantity sold per product
avg_quantity = df.groupby('Product')['Quantity'].mean()
print("\nAverage Quantity per Product:")
print(avg_quantity)

# 5. Total sales per product per month
product_month_sales = df.groupby(['Product', 'Month'])['Sales'].sum()
print("\nSales per Product per Month:")
print(product_month_sales)
