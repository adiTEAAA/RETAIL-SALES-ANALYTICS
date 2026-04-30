import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

def generate_retail_data(num_records=10500):
    print(f"Generating {num_records} synthetic transactions...")
    
    # Define product categories and some sample products
    categories = {
        'Electronics': [('Laptop', 800, 1500), ('Smartphone', 500, 1000), ('Headphones', 50, 200), ('Monitor', 150, 400)],
        'Clothing': [('T-Shirt', 15, 30), ('Jeans', 40, 80), ('Jacket', 60, 150), ('Sneakers', 50, 120)],
        'Home & Garden': [('Blender', 30, 80), ('Coffee Maker', 40, 100), ('Plant Pot', 10, 25), ('Lamp', 20, 60)],
        'Sports': [('Yoga Mat', 15, 35), ('Dumbbells', 20, 60), ('Tennis Racket', 50, 150), ('Water Bottle', 10, 25)]
    }
    
    # Generate customers
    num_customers = 1500
    customers = [fake.unique.random_int(min=10000, max=99999) for _ in range(num_customers)]
    customer_segments = ['New', 'Regular', 'VIP']
    customer_mapping = {c: random.choices(customer_segments, weights=[0.4, 0.5, 0.1])[0] for c in customers}
    
    # Date range (last 12 months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    data = []
    
    for i in range(num_records):
        # Transaction ID
        transaction_id = f"TRX-{fake.unique.random_int(min=100000, max=999999)}"
        
        # Date (bias towards weekends and holidays)
        date = fake.date_time_between(start_date=start_date, end_date=end_date)
        
        # Customer
        customer_id = random.choice(customers)
        segment = customer_mapping[customer_id]
        
        # Product
        category = random.choice(list(categories.keys()))
        product_info = random.choice(categories[category])
        product_name = product_info[0]
        
        # Price (base price with some variation)
        base_price = random.uniform(product_info[1], product_info[2])
        unit_price = round(base_price, 2)
        
        # Quantity (VIPs tend to buy more)
        if segment == 'VIP':
            quantity = random.choices([1, 2, 3, 4, 5], weights=[0.2, 0.3, 0.2, 0.2, 0.1])[0]
        else:
            quantity = random.choices([1, 2, 3, 4], weights=[0.6, 0.2, 0.1, 0.1])[0]
            
        # Introduce some missing values and anomalies for cleaning later
        if random.random() < 0.01:
            unit_price = np.nan # Missing price
        elif random.random() < 0.005:
            quantity = -1 # Negative quantity (error)
            
        total_amount = round(unit_price * quantity, 2) if not pd.isna(unit_price) and quantity > 0 else np.nan

        # Payment Method
        payment_method = random.choices(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], weights=[0.5, 0.3, 0.15, 0.05])[0]

        data.append({
            'TransactionID': transaction_id,
            'Date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'CustomerID': customer_id,
            'CustomerSegment': segment,
            'Category': category,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'TotalAmount': total_amount,
            'PaymentMethod': payment_method
        })
        
    df = pd.DataFrame(data)
    
    # Introduce some duplicates
    if random.random() > 0.5:
        duplicates = df.sample(n=50)
        df = pd.concat([df, duplicates], ignore_index=True)
        
    # Shuffle
    df = df.sample(frac=1).reset_index(drop=True)
    
    output_file = 'retail_transactions.csv'
    df.to_csv(output_file, index=False)
    print(f"Dataset generated successfully and saved to {output_file}.")
    print(f"Total Rows: {len(df)}")

if __name__ == "__main__":
    generate_retail_data()
