#!/usr/bin/env python3
"""Initialize database with Amazon sales data."""

import pandas as pd
import sqlite3
from pathlib import Path

# Find the CSV file
db_dir = Path("database")
csv_files = ["amazon_sales_clean.csv", "amazon sales.csv", "sales_data.csv"]

csv_file = None
for f in csv_files:
    path = db_dir / f
    if path.exists():
        csv_file = path
        print(f"✓ Found: {path}")
        break

if not csv_file:
    print("✗ No CSV file found")
    exit(1)

# Load CSV
df = pd.read_csv(csv_file)
print(f"✓ Loaded {len(df)} rows from CSV")
print(f"Columns: {list(df.columns)}")

# Create SQLite database
db_path = "backend/bi_dashboard.db"
conn = sqlite3.connect(db_path)

# Drop existing table if it exists
conn.execute("DROP TABLE IF EXISTS sales")

# Create and populate table
df.to_sql("sales", conn, index=False, if_exists="replace")
conn.commit()
conn.close()

print(f"✓ Database created at: {db_path}")

# Verify
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]
conn.close()

print(f"✓ Database contains {count} records")
print("✓ Setup complete!")
