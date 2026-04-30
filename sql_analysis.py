import pandas as pd
import sqlite3
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def run_sql_analysis():
    print("Connecting to SQLite database...")
    conn = sqlite3.connect('retail_sales.db')
    cursor = conn.cursor()
    
    print("Loading cleaned data into database...")
    df = pd.read_csv('cleaned_retail_data.csv')
    df.to_sql('retail_sales', conn, if_exists='replace', index=False)
    
    print("\n--- Executing Analysis Queries ---\n")
    
    with open('analysis_queries.sql', 'r') as file:
        sql_script = file.read()
        
    queries = sql_script.split(';')
    
    query_names = [
        "1. Monthly Revenue",
        "2. Top 5 Products by Revenue",
        "3. Customer Segment Performance",
        "4. Payment Method Popularity"
    ]
    
    for i, query in enumerate(queries):
        if query.strip():
            print(f"{query_names[i]}:")
            result_df = pd.read_sql_query(query, conn)
            print(result_df)
            print("-" * 50)
            
    conn.close()
    print("SQL Analysis completed.")

if __name__ == "__main__":
    if not os.path.exists('cleaned_retail_data.csv'):
        print("Please run data_cleaning_eda.py first to generate the cleaned dataset.")
    else:
        run_sql_analysis()
