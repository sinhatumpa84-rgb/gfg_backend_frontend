from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
from typing import List, Dict, Any, Optional
import sqlite3
import logging
import os
from config import settings
from models import DataSourceInfo

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service for database operations supporting multiple database types."""
    
    def __init__(self):
        """Initialize database connection."""
        self.db_type = settings.database_type
        self.engine = None
        self.SessionLocal = None
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize database connection based on configuration."""
        try:
            if self.db_type == "sqlite":
                self.engine = create_engine(settings.database_url, echo=False)
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
                # Create tables if they don't exist
                self._init_sqlite_tables()
            elif self.db_type == "postgresql":
                self.engine = create_engine(settings.database_url, echo=False)
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            logger.info(f"Database connection initialized: {self.db_type}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _init_sqlite_tables(self):
        """Initialize sample tables in SQLite for demo purposes."""
        try:
            conn = sqlite3.connect(settings.database_url.replace("sqlite:///", ""))
            cursor = conn.cursor()
            
            # Check if tables already exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            existing_tables = cursor.fetchall()
            
            if not existing_tables:
                # Create sample tables for demonstration
                # Sales data table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        region TEXT,
                        product_category TEXT,
                        product_name TEXT,
                        revenue REAL,
                        quantity INTEGER,
                        salesperson TEXT
                    )
                """)
                
                # Insert sample data
                sample_sales_data = [
                    ('2024-01-01', 'North', 'Electronics', 'Laptop', 5000, 2, 'John'),
                    ('2024-01-02', 'South', 'Furniture', 'Desk', 800, 1, 'Sarah'),
                    ('2024-01-03', 'East', 'Electronics', 'Phone', 1200, 3, 'Mike'),
                    ('2024-01-04', 'West', 'Clothing', 'Shirt', 50, 5, 'Emma'),
                    ('2024-01-05', 'North', 'Electronics', 'Tablet', 2000, 1, 'John'),
                    ('2024-02-01', 'South', 'Electronics', 'Laptop', 5000, 1, 'Sarah'),
                    ('2024-02-02', 'East', 'Furniture', 'Chair', 500, 4, 'Mike'),
                    ('2024-02-03', 'West', 'Electronics', 'Monitor', 600, 2, 'Emma'),
                    ('2024-03-01', 'North', 'Clothing', 'Jacket', 150, 2, 'John'),
                    ('2024-03-02', 'South', 'Furniture', 'Table', 1500, 1, 'Sarah'),
                ]
                
                cursor.executemany(
                    "INSERT INTO sales VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                    sample_sales_data
                )
                
                # Employees table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        department TEXT,
                        salary REAL,
                        hire_date TEXT
                    )
                """)
                
                sample_employees_data = [
                    ('John', 'Sales', 50000, '2020-01-15'),
                    ('Sarah', 'Sales', 55000, '2019-06-01'),
                    ('Mike', 'Sales', 52000, '2021-03-10'),
                    ('Emma', 'Sales', 48000, '2022-01-20'),
                ]
                
                cursor.executemany(
                    "INSERT INTO employees VALUES (NULL, ?, ?, ?, ?)",
                    sample_employees_data
                )
                
                conn.commit()
                logger.info("Sample data initialized in SQLite")
            
            conn.close()
        except Exception as e:
            logger.warning(f"Could not initialize SQLite tables: {e}")
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results as list of dicts.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result rows as dictionaries
        """
        try:
            if params is None:
                params = {}
            
            session = self.SessionLocal()
            result = session.execute(text(query), params)
            
            # Convert to list of dicts
            rows = result.fetchall()
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in rows]
            
            session.close()
            return data
        except Exception as e:
            logger.error(f"Error executing query: {e}\nQuery: {query}")
            raise
    
    def get_schema(self) -> Dict[str, DataSourceInfo]:
        """
        Get database schema information.
        
        Returns:
            Dictionary of table information
        """
        try:
            inspector = inspect(self.engine)
            tables = {}
            
            for table_name in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns(table_name)]
                
                # Get row count
                session = self.SessionLocal()
                result = session.execute(text(f"SELECT COUNT(*) as count FROM {table_name}"))
                row_count = result.fetchone()[0]
                session.close()
                
                tables[table_name] = DataSourceInfo(
                    name=table_name,
                    type="table",
                    columns=columns,
                    row_count=row_count
                )
            
            return tables
        except Exception as e:
            logger.error(f"Error getting schema: {e}")
            return {}
    
    def get_table_schema_string(self) -> str:
        """
        Get formatted string representation of database schema for LLM.
        
        Returns:
            Formatted schema string
        """
        schema = self.get_schema()
        schema_str = "Database Tables:\n"
        
        for table_name, table_info in schema.items():
            schema_str += f"\nTable: {table_name}\n"
            schema_str += f"  Columns: {', '.join(table_info.columns)}\n"
            schema_str += f"  Rows: {table_info.row_count}\n"
        
        return schema_str
    
    def get_available_tables(self) -> List[str]:
        """Get list of available table names."""
        try:
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"Error getting table names: {e}")
            return []

class CSVService:
    """Service for handling CSV data sources."""
    
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """
        Load CSV file into DataFrame.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Pandas DataFrame
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {e}")
            raise
    
    @staticmethod
    def query_csv(df: pd.DataFrame, query_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query CSV data using simple filter dictionary.
        
        Args:
            df: Pandas DataFrame
            query_dict: Dictionary with filters
            
        Returns:
            List of result rows
        """
        try:
            result_df = df.copy()
            
            # Apply filters if provided
            if 'filters' in query_dict:
                for column, value in query_dict['filters'].items():
                    if column in result_df.columns:
                        result_df = result_df[result_df[column] == value]
            
            return result_df.to_dict('records')
        except Exception as e:
            logger.error(f"Error querying CSV: {e}")
            return []

# Initialize services
db_service = DatabaseService()
