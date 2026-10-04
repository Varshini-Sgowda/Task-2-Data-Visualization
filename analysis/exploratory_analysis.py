"""
SUPERSCOPE - Exploratory Data Analysis & Business Intelligence Engine
Elevate Labs Data Analyst Internship - Task 2: Data Visualization and Storytelling
Author: Data Analyst Intern
"""

import pandas as pd
import numpy as np

def run_analysis():
    try:
        df = pd.read_csv('data/raw/Superstore.csv', encoding='utf-8')
    except Exception:
        df = pd.read_csv('data/raw/Superstore.csv', encoding='latin1')
    print("=" * 60)
    print("SUPERSCOPE: RAW DATA PROFILE")
    print("=" * 60)
    print(f"Total Rows: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")
    print(f"Missing Values: {df.isnull().sum().sum()}")
    print(f"Duplicate Rows: {df.duplicated().sum()}")
    
    # 2. Data Cleaning & Feature Engineering
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed')
    
    # Extract temporal dimensions
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order YearMonth'] = df['Order Date'].dt.to_period('M')
    df['Order Quarter'] = df['Order Date'].dt.to_period('Q')
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    
    # Financial metrics
    df['Profit Margin %'] = (df['Profit'] / df['Sales']) * 100
    df['Cost'] = df['Sales'] - df['Profit']
    
    # Save Cleaned Data
    df.to_csv('data/cleaned/Superstore_Cleaned.csv', index=False)
    print("\nCleaned dataset saved to 'data/cleaned/Superstore_Cleaned.csv'")
    
    # 3. Executive Snapshot Metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    total_items_sold = df['Quantity'].sum()
    overall_profit_margin = (total_profit / total_sales) * 100
    aov = total_sales / total_orders
    profit_per_order = total_profit / total_orders
    sales_per_customer = total_sales / total_customers
    avg_discount = df['Discount'].mean() * 100
    
    print("\n" + "=" * 60)
    print("EXECUTIVE SNAPSHOT METRICS")
    print("=" * 60)
    print(f"Date Range: {df['Order Date'].min().strftime('%b %d, %Y')} to {df['Order Date'].max().strftime('%b %d, %Y')}")
    print(f"Total Revenue (Sales):     ${total_sales:,.2f}")
    print(f"Total Net Profit:          ${total_profit:,.2f}")
    print(f"Overall Profit Margin:     {overall_profit_margin:.2f}%")
    print(f"Total Unique Orders:       {total_orders:,}")
    print(f"Total Unique Customers:    {total_customers:,}")
    print(f"Total Quantity Sold:       {total_items_sold:,} units")
    print(f"Average Order Value (AOV): ${aov:,.2f}")
    print(f"Average Profit Per Order:  ${profit_per_order:,.2f}")
    print(f"Average Customer Spend:    ${sales_per_customer:,.2f}")
    print(f"Average Order Discount:    {avg_discount:.2f}%")
    
    # 4. Yearly Growth & Trend
    yearly = df.groupby('Order Year').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Margin=('Profit', lambda x: (x.sum() / df.loc[x.index, 'Sales'].sum()) * 100)
    ).reset_index()
    yearly['Sales Growth %'] = yearly['Sales'].pct_change() * 100
    yearly['Profit Growth %'] = yearly['Profit'].pct_change() * 100
    
    print("\n" + "=" * 60)
    print("YEAR-OVER-YEAR PERFORMANCE")
    print("=" * 60)
    print(yearly.to_string(index=False))
    
    # 5. Category & Sub-Category Performance
    cat_summary = df.groupby('Category').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    cat_summary['Sales Share %'] = (cat_summary['Sales'] / total_sales) * 100
    cat_summary['Profit Margin %'] = (cat_summary['Profit'] / cat_summary['Sales']) * 100
    cat_summary = cat_summary.sort_values(by='Sales', ascending=False)
    
    print("\n" + "=" * 60)
    print("CATEGORY PERFORMANCE")
    print("=" * 60)
    print(cat_summary.to_string(index=False))
    
    subcat_summary = df.groupby(['Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', lambda x: x.mean() * 100)
    ).reset_index()
    subcat_summary['Profit Margin %'] = (subcat_summary['Profit'] / subcat_summary['Sales']) * 100
    subcat_summary = subcat_summary.sort_values(by='Profit', ascending=False)
    
    print("\n" + "=" * 60)
    print("SUB-CATEGORY PERFORMANCE (SORTED BY PROFIT)")
    print("=" * 60)
    print(subcat_summary.to_string(index=False))
    
    # 6. Regional & Geographic Performance
    region_summary = df.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Avg_Discount=('Discount', lambda x: x.mean() * 100)
    ).reset_index()
    region_summary['Sales Share %'] = (region_summary['Sales'] / total_sales) * 100
    region_summary['Profit Margin %'] = (region_summary['Profit'] / region_summary['Sales']) * 100
    region_summary = region_summary.sort_values(by='Sales', ascending=False)
    
    print("\n" + "=" * 60)
    print("REGIONAL PERFORMANCE")
    print("=" * 60)
    print(region_summary.to_string(index=False))
    
    # State Winners & Bleeders
    state_summary = df.groupby('State').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Avg_Discount=('Discount', lambda x: x.mean() * 100)
    ).reset_index()
    state_summary['Profit Margin %'] = (state_summary['Profit'] / state_summary['Sales']) * 100
    
    top_5_states_profit = state_summary.sort_values(by='Profit', ascending=False).head(5)
    bottom_5_states_profit = state_summary.sort_values(by='Profit', ascending=True).head(5)
    
    print("\nTop 5 Most Profitable States:")
    print(top_5_states_profit[['State', 'Sales', 'Profit', 'Profit Margin %', 'Avg_Discount']].to_string(index=False))
    print("\nBottom 5 Least Profitable (Loss-Making) States:")
    print(bottom_5_states_profit[['State', 'Sales', 'Profit', 'Profit Margin %', 'Avg_Discount']].to_string(index=False))
    
    # 7. Customer Deep Dive
    cust_summary = df.groupby(['Customer ID', 'Customer Name', 'Segment']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    cust_summary['Profit Margin %'] = (cust_summary['Profit'] / cust_summary['Sales']) * 100
    
    print("\nTop 5 Customers by Revenue:")
    print(cust_summary.sort_values(by='Sales', ascending=False).head(5).to_string(index=False))
    print("\nTop 5 Customers by Profit:")
    print(cust_summary.sort_values(by='Profit', ascending=False).head(5).to_string(index=False))
    print("\nTop 5 Customers with Largest Losses (Negative Profit):")
    print(cust_summary.sort_values(by='Profit', ascending=True).head(5).to_string(index=False))
    
    # 8. Product Opportunity & Bleeder Analysis
    prod_summary = df.groupby(['Product ID', 'Product Name', 'Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', lambda x: x.mean() * 100)
    ).reset_index()
    prod_summary['Profit Margin %'] = (prod_summary['Profit'] / prod_summary['Sales']) * 100
    
    print("\nTop 5 Most Profitable Products:")
    print(prod_summary.sort_values(by='Profit', ascending=False)[['Product Name', 'Category', 'Sales', 'Profit', 'Profit Margin %']].head(5).to_string(index=False))
    
    print("\nTop 5 Biggest Loss-Making Products:")
    print(prod_summary.sort_values(by='Profit', ascending=True)[['Product Name', 'Category', 'Sales', 'Profit', 'Profit Margin %', 'Avg_Discount']].head(5).to_string(index=False))

    # 9. Discount Impact Analysis (The Root Cause of Profit Destruction)
    df['Discount Bracket'] = pd.cut(
        df['Discount'],
        bins=[-0.01, 0.0, 0.15, 0.30, 0.50, 1.0],
        labels=['0% (No Discount)', '1-15% (Low)', '16-30% (Moderate)', '31-50% (High)', '51-80% (Deep)']
    )
    discount_impact = df.groupby('Discount Bracket', observed=False).agg(
        Orders=('Order ID', 'nunique'),
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    discount_impact['Profit Margin %'] = (discount_impact['Profit'] / discount_impact['Sales']) * 100
    print("\n" + "=" * 60)
    print("DISCOUNT IMPACT ON PROFIT MARGIN")
    print("=" * 60)
    print(discount_impact.to_string(index=False))

if __name__ == '__main__':
    run_analysis()
