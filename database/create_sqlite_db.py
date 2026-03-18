"""
Script to create SQLite database with e-commerce sales data
Run: python create_sqlite_db.py
"""

import sqlite3
import pandas as pd
from pathlib import Path

def create_sqlite_database():
    """Create SQLite database with ecommerce sales data."""
    
    # Database path
    db_path = Path(__file__).parent / "sales.db"
    
    # Connect to SQLite database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            order_id INTEGER PRIMARY KEY,
            order_date TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            product_category TEXT NOT NULL,
            price REAL NOT NULL,
            discount_percent INTEGER NOT NULL,
            quantity_sold INTEGER NOT NULL,
            customer_region TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            rating REAL NOT NULL,
            review_count INTEGER NOT NULL,
            discounted_price REAL NOT NULL,
            total_revenue REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_product_category ON sales(product_category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_customer_region ON sales(customer_region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_payment_method ON sales(payment_method)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sales_product_id ON sales(product_id)")
    
    # Read CSV data
    csv_path = Path(__file__).parent / "sales_data.csv"
    df = pd.read_csv(csv_path)
    
    # Insert data into SQLite
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    # Commit and close
    conn.commit()
    
    # Display confirmation
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    print(f"✓ SQLite database created successfully at: {db_path}")
    print(f"✓ Total records inserted: {count}")
    
    # Show sample data
    print("\nSample data:")
    df_sample = pd.read_sql_query("SELECT * FROM sales LIMIT 5", conn)
    print(df_sample.to_string())
    
    conn.close()

if __name__ == "__main__":
    create_sqlite_database()
