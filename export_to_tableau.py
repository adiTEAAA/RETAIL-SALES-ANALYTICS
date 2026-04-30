import pandas as pd
import sqlite3
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def export_for_tableau():
    print("Connecting to SQLite database...")
    if not os.path.exists('retail_sales.db'):
        print("Database not found! Run sql_analysis.py first.")
        return
        
    conn = sqlite3.connect('retail_sales.db')
    
    # We will export the main cleaned table and aggregated views
    print("Exporting datasets for Tableau...")
    
    # 1. Main Table (Detailed Data for Drill-downs)
    main_df = pd.read_sql_query("SELECT * FROM retail_sales", conn)
    main_df.to_csv('tableau_retail_sales.csv', index=False)
    print("- Created tableau_retail_sales.csv")
    
    # 2. Monthly Revenue
    monthly_df = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', Date) AS MonthYear,
            SUM(TotalAmount) AS TotalRevenue,
            COUNT(TransactionID) AS TotalTransactions
        FROM retail_sales
        GROUP BY MonthYear
    """, conn)
    monthly_df.to_csv('tableau_monthly_revenue.csv', index=False)
    print("- Created tableau_monthly_revenue.csv")
    
    # 3. Product Performance
    product_df = pd.read_sql_query("""
        SELECT 
            ProductName,
            Category,
            SUM(TotalAmount) AS TotalRevenue,
            SUM(Quantity) AS TotalUnitsSold
        FROM retail_sales
        GROUP BY ProductName, Category
    """, conn)
    product_df.to_csv('tableau_product_performance.csv', index=False)
    print("- Created tableau_product_performance.csv")
    
    # 4. Customer Segments
    segment_df = pd.read_sql_query("""
        SELECT 
            CustomerSegment,
            COUNT(DISTINCT CustomerID) AS UniqueCustomers,
            SUM(TotalAmount) AS TotalRevenue
        FROM retail_sales
        GROUP BY CustomerSegment
    """, conn)
    segment_df.to_csv('tableau_customer_segments.csv', index=False)
    print("- Created tableau_customer_segments.csv")

    conn.close()
    print("\nExport complete! You can now load these CSVs into Tableau.")

if __name__ == "__main__":
    export_for_tableau()
