"""
Data loader for Amazon e-commerce sales dataset
Supports CSV, SQLite, and PostgreSQL

Usage:
    # Load from CSV
    loader = DataLoader(source='csv')
    df = loader.load()
    
    # Load from SQLite
    loader = DataLoader(source='sqlite')
    df = loader.load()
    
    # Load from PostgreSQL
    loader = DataLoader(source='postgresql', connection_string='postgresql://user:password@localhost/ecommerce')
    df = loader.load()
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Optional, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load e-commerce sales data from various sources."""
    
    def __init__(
        self,
        source: str = 'csv',
        csv_path: Optional[str] = None,
        sqlite_path: Optional[str] = None,
        connection_string: Optional[str] = None
    ):
        """
        Initialize data loader.
        
        Args:
            source: 'csv', 'sqlite', or 'postgresql'
            csv_path: Path to CSV file (default: database/sales_data.csv)
            sqlite_path: Path to SQLite DB (default: database/sales.db)
            connection_string: PostgreSQL connection string
        """
        self.source = source.lower()
        self.csv_path = csv_path or Path(__file__).parent / 'sales_data.csv'
        self.sqlite_path = sqlite_path or Path(__file__).parent / 'sales.db'
        self.connection_string = connection_string
        
        logger.info(f"DataLoader initialized for {source}")
    
    def load(self, query: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """
        Load data from specified source.
        
        Args:
            query: SQL query (for database sources)
            **kwargs: Additional parameters (e.g., limit=100)
        
        Returns:
            DataFrame with sales data
        """
        if self.source == 'csv':
            return self._load_csv(**kwargs)
        elif self.source == 'sqlite':
            return self._load_sqlite(query, **kwargs)
        elif self.source == 'postgresql':
            return self._load_postgresql(query, **kwargs)
        else:
            raise ValueError(f"Unknown source: {self.source}")
    
    def _load_csv(self, **kwargs) -> pd.DataFrame:
        """Load data from CSV."""
        try:
            df = pd.read_csv(self.csv_path)
            logger.info(f"Loaded {len(df)} records from CSV")
            return df
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            raise
    
    def _load_sqlite(self, query: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Load data from SQLite."""
        try:
            conn = sqlite3.connect(str(self.sqlite_path))
            
            if query is None:
                query = "SELECT * FROM sales"
            
            df = pd.read_sql_query(query, conn)
            logger.info(f"Loaded {len(df)} records from SQLite")
            conn.close()
            return df
        except FileNotFoundError:
            logger.error(f"SQLite database not found: {self.sqlite_path}")
            logger.info("Run: python database/create_sqlite_db.py")
            raise
    
    def _load_postgresql(self, query: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Load data from PostgreSQL."""
        try:
            from sqlalchemy import create_engine
            
            engine = create_engine(self.connection_string)
            
            if query is None:
                query = "SELECT * FROM sales"
            
            df = pd.read_sql_query(query, engine)
            logger.info(f"Loaded {len(df)} records from PostgreSQL")
            return df
        except ImportError:
            logger.error("SQLAlchemy required for PostgreSQL. Install: pip install sqlalchemy")
            raise
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            raise
    
    def get_summary(self) -> dict:
        """Get summary statistics of the data."""
        df = self.load()
        
        return {
            'total_records': len(df),
            'date_range': f"{df['order_date'].min()} to {df['order_date'].max()}",
            'total_revenue': df['total_revenue'].sum(),
            'avg_order_value': df['total_revenue'].mean(),
            'categories': df['product_category'].nunique(),
            'regions': df['customer_region'].nunique(),
            'payment_methods': df['payment_method'].nunique(),
        }
    
    def get_category_analysis(self) -> pd.DataFrame:
        """Get revenue analysis by product category."""
        df = self.load()
        
        return df.groupby('product_category').agg({
            'total_revenue': 'sum',
            'order_id': 'count',
            'quantity_sold': 'sum',
            'rating': 'mean',
            'discount_percent': 'mean'
        }).round(2).rename(columns={'order_id': 'order_count'})
    
    def get_region_analysis(self) -> pd.DataFrame:
        """Get revenue analysis by region."""
        df = self.load()
        
        return df.groupby('customer_region').agg({
            'total_revenue': 'sum',
            'order_id': 'count',
            'quantity_sold': 'sum',
            'rating': 'mean'
        }).round(2).rename(columns={'order_id': 'order_count'})
    
    def get_discount_analysis(self) -> pd.DataFrame:
        """Get revenue analysis by discount percentage."""
        df = self.load()
        
        return df.groupby('discount_percent').agg({
            'total_revenue': ['sum', 'mean'],
            'quantity_sold': 'mean',
            'order_id': 'count',
            'rating': 'mean'
        }).round(2)
    
    def export_to_csv(self, output_path: str) -> None:
        """Export data to CSV."""
        df = self.load()
        df.to_csv(output_path, index=False)
        logger.info(f"Data exported to {output_path}")


# Example usage
if __name__ == "__main__":
    # Load from CSV
    print("=" * 50)
    print("AMAZON E-COMMERCE SALES DATA LOADER")
    print("=" * 50)
    
    loader = DataLoader(source='csv')
    
    # Get summary
    print("\nDataset Summary:")
    summary = loader.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Get analysis
    print("\n\nRevenue by Category:")
    print(loader.get_category_analysis())
    
    print("\n\nRevenue by Region:")
    print(loader.get_region_analysis())
    
    print("\n\nRevenue by Discount:")
    print(loader.get_discount_analysis())
