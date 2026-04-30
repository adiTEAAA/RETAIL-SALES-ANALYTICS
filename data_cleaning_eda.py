import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def run_cleaning_and_eda():
    print("Loading data...")
    df = pd.read_csv('retail_transactions.csv')
    
    print("Initial Data Shape:", df.shape)
    
    # 1. DATA CLEANING
    print("\n--- Data Cleaning ---")
    # Remove duplicates
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    print(f"Removed {initial_rows - len(df)} duplicate rows.")
    
    # Handle missing values
    missing_before = df.isnull().sum()
    print("Missing values before cleaning:\n", missing_before[missing_before > 0])
    
    # For UnitPrice and TotalAmount, we can drop them or impute. We'll drop rows with missing UnitPrice.
    df.dropna(subset=['UnitPrice'], inplace=True)
    
    # Fix negative quantities (assuming they were errors and should be positive)
    df['Quantity'] = df['Quantity'].apply(lambda x: abs(x) if x < 0 else x)
    
    # Recalculate TotalAmount to fix any missing/wrong values based on cleaned quantity and price
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    print("Final Data Shape:", df.shape)
    
    # Save cleaned data
    df.to_csv('cleaned_retail_data.csv', index=False)
    print("\nCleaned data saved to 'cleaned_retail_data.csv'.")
    
    # 2. EXPLORATORY DATA ANALYSIS (EDA)
    print("\n--- Exploratory Data Analysis ---")
    
    # Create an 'images' directory for EDA plots
    os.makedirs('images', exist_ok=True)
    
    # Set plot style
    sns.set_theme(style="whitegrid")
    
    # A. Revenue over time (Monthly)
    print("Generating Monthly Revenue plot...")
    df['MonthYear'] = df['Date'].dt.to_period('M')
    monthly_revenue = df.groupby('MonthYear')['TotalAmount'].sum().reset_index()
    monthly_revenue['MonthYear'] = monthly_revenue['MonthYear'].astype(str)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_revenue, x='MonthYear', y='TotalAmount', marker='o', color='b')
    plt.title('Monthly Revenue Trend')
    plt.xticks(rotation=45)
    plt.ylabel('Total Revenue ($)')
    plt.tight_layout()
    plt.savefig('images/monthly_revenue_trend.png')
    plt.close()
    
    # B. Sales by Category
    print("Generating Category Sales plot...")
    category_sales = df.groupby('Category')['TotalAmount'].sum().reset_index().sort_values('TotalAmount', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=category_sales, x='Category', y='TotalAmount', palette='viridis')
    plt.title('Total Revenue by Category')
    plt.ylabel('Total Revenue ($)')
    plt.tight_layout()
    plt.savefig('images/revenue_by_category.png')
    plt.close()
    
    # C. Customer Segments Distribution
    print("Generating Customer Segment plot...")
    segment_counts = df['CustomerSegment'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title('Transactions by Customer Segment')
    plt.tight_layout()
    plt.savefig('images/customer_segments.png')
    plt.close()
    
    print("EDA plots saved in 'images' directory.")

if __name__ == "__main__":
    run_cleaning_and_eda()
