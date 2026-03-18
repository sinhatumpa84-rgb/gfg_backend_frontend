"""
Database migration and setup utilities

Run with: python manage.py [command]
"""

import argparse
import logging
import sqlite3
from database_service import db_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manage database operations."""
    
    @staticmethod
    def init_db():
        """Initialize database with sample data."""
        try:
            logger.info("Initializing database...")
            # Database is already initialized by database_service
            schema = db_service.get_schema()
            logger.info(f"Database initialized with {len(schema)} tables")
            for table_name, info in schema.items():
                logger.info(f"  - {table_name}: {info.row_count} rows")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
    
    @staticmethod
    def reset_db():
        """Reset database (DELETE all data)."""
        try:
            from config import settings
            if "sqlite" in settings.database_url:
                db_path = settings.database_url.replace("sqlite:///", "")
                import os
                if os.path.exists(db_path):
                    os.remove(db_path)
                    logger.info(f"Deleted SQLite database: {db_path}")
            logger.info("Database reset. Run --init to recreate.")
            return True
        except Exception as e:
            logger.error(f"Failed to reset database: {e}")
            return False
    
    @staticmethod
    def list_tables():
        """List all tables and their info."""
        try:
            schema = db_service.get_schema()
            logger.info(f"\nFound {len(schema)} table(s):")
            for table_name, info in schema.items():
                logger.info(f"\n  Table: {table_name}")
                logger.info(f"    Rows: {info.row_count}")
                logger.info(f"    Columns: {', '.join(info.columns)}")
            return True
        except Exception as e:
            logger.error(f"Failed to list tables: {e}")
            return False
    
    @staticmethod
    def show_schema():
        """Display database schema."""
        try:
            schema_str = db_service.get_table_schema_string()
            logger.info("\nDatabase Schema:")
            logger.info(schema_str)
            return True
        except Exception as e:
            logger.error(f"Failed to show schema: {e}")
            return False
    
    @staticmethod
    def sample_data():
        """Show sample data from all tables."""
        try:
            schema = db_service.get_schema()
            for table_name in schema.keys():
                logger.info(f"\n{'='*60}")
                logger.info(f"Sample data from {table_name}:")
                logger.info('='*60)
                query = f"SELECT * FROM {table_name} LIMIT 5"
                results = db_service.execute_query(query)
                for i, row in enumerate(results, 1):
                    logger.info(f"\nRow {i}:")
                    for key, value in row.items():
                        logger.info(f"  {key}: {value}")
            return True
        except Exception as e:
            logger.error(f"Failed to show sample data: {e}")
            return False
    
    @staticmethod
    def test_connection():
        """Test database connection."""
        try:
            schema = db_service.get_schema()
            if schema:
                logger.info("✓ Database connection successful")
                logger.info(f"  Found {len(schema)} table(s)")
                return True
            else:
                logger.warning("⚠ Database connected but no tables found")
                return False
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            return False
    
    @staticmethod
    def query(sql: str):
        """Execute a custom query."""
        try:
            logger.info(f"Executing: {sql}\n")
            results = db_service.execute_query(sql)
            logger.info(f"Returned {len(results)} row(s):\n")
            for i, row in enumerate(results, 1):
                logger.info(f"Row {i}: {row}")
            return True
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return False

def main():
    """CLI interface for database management."""
    parser = argparse.ArgumentParser(
        description="Database management utility"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Commands
    subparsers.add_parser("init", help="Initialize database with sample data")
    subparsers.add_parser("reset", help="Reset database (delete all data)")
    subparsers.add_parser("list", help="List all tables")
    subparsers.add_parser("schema", help="Show database schema")
    subparsers.add_parser("sample", help="Show sample data from all tables")
    subparsers.add_parser("test", help="Test database connection")
    
    query_parser = subparsers.add_parser("query", help="Execute SQL query")
    query_parser.add_argument("sql", help="SQL query to execute")
    
    args = parser.parse_args()
    
    manager = DatabaseManager()
    
    if args.command == "init":
        manager.init_db()
    elif args.command == "reset":
        manager.reset_db()
    elif args.command == "list":
        manager.list_tables()
    elif args.command == "schema":
        manager.show_schema()
    elif args.command == "sample":
        manager.sample_data()
    elif args.command == "test":
        manager.test_connection()
    elif args.command == "query":
        manager.query(args.sql)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
