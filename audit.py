import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('dirty_financial_transactions.csv')
df.info()
print(df.head(20))
print(df.describe())
print(df.isnull().sum())

# Handle missing values for each column
print(f"\nOriginal rows: {len(df)}")

df['Quantity'] = df['Quantity'].abs()
df['Quantity'] = df['Quantity'].fillna(1)

df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Price'] = df['Price'].abs()
df['Price'] = df['Price'].fillna(df['Price'].mean())

df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
df['Transaction_Date'] = df['Transaction_Date'].ffill()

df = df.dropna(subset=['Transaction_ID', 'Customer_ID'])
df['Transaction_Status'] = df['Transaction_Status'].fillna('unknown')
print(df.isnull().sum())

## string cleaning
df['Payment_Method'] = df['Payment_Method'].str.strip().str.lower().str.replace(' ', '')
df['Transaction_Status'] = df['Transaction_Status'].str.strip().str.lower().str.replace(' ', '')
df['Transaction_Status'] = df['Transaction_Status'].replace('complete', 'completed')
df['Product_Name'] = df['Product_Name'].str.strip()
# Create a Total column
df['Total_Amount'] = df['Price'] * df['Quantity']

print("\n--- REVENUE BY PAYMENT METHOD ---")
print(df.groupby('Payment_Method')['Total_Amount'].sum())

print("\n--- CLEANED DATA SUMMARY ---")
print(df.describe())

# Create a mapping dictionary for the broken product names
product_map = {
    'Tabl': 'Tablet', 'Ta': 'Tablet', 'T': 'Tablet', 'Table': 'Tablet',
    'La': 'Laptop', 'Lapt': 'Laptop'
}

# Apply the mapping (Keep the original if it's not in the map)
df['Product_Name'] = df['Product_Name'].replace(product_map)

# Verify the fix
print("\n--- CLEANED TOP PRODUCTS ---")
print(df.groupby('Product_Name')['Total_Amount'].sum().sort_values(ascending=False))
