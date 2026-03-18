import json
import logging
from typing import Any, Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class QueryBuilder:
    """Utility class for building SQL queries dynamically."""
    
    @staticmethod
    def build_select_query(table: str, 
                          columns: List[str] = None, 
                          where: str = None,
                          group_by: str = None,
                          order_by: str = None,
                          limit: int = None) -> str:
        """
        Build a SELECT query dynamically.
        
        Args:
            table: Table name
            columns: Columns to select (default: all)
            where: WHERE clause
            group_by: GROUP BY clause
            order_by: ORDER BY clause
            limit: LIMIT clause value
            
        Returns:
            SQL query string
        """
        try:
            select_cols = ", ".join(columns) if columns else "*"
            query = f"SELECT {select_cols} FROM {table}"
            
            if where:
                query += f" WHERE {where}"
            
            if group_by:
                query += f" GROUP BY {group_by}"
            
            if order_by:
                query += f" ORDER BY {order_by}"
            
            if limit:
                query += f" LIMIT {limit}"
            
            return query
        except Exception as e:
            logger.error(f"Error building query: {e}")
            return ""

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for complex types."""
    
    def default(self, obj):
        """Override default JSON encoding."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

class DataValidator:
    """Utility class for data validation."""
    
    @staticmethod
    def validate_query_params(query: str, filters: Dict = None) -> bool:
        """
        Validate query parameters for safety.
        
        Args:
            query: Query string
            filters: Filter dictionary
            
        Returns:
            True if valid, False otherwise
        """
        if not query or not isinstance(query, str):
            return False
        
        if len(query.strip()) < 3:
            return False
        
        # Check for SQL injection patterns (basic check)
        dangerous_patterns = ["DROP", "DELETE", "TRUNCATE", "ALTER", "EXEC"]
        query_upper = query.upper()
        
        for pattern in dangerous_patterns:
            if pattern in query_upper:
                return False
        
        if filters:
            if not isinstance(filters, dict):
                return False
        
        return True
    
    @staticmethod
    def validate_chart_config(config: Dict[str, Any]) -> bool:
        """
        Validate chart configuration.
        
        Args:
            config: Chart configuration dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["type", "title", "x_axis", "y_axis"]
        
        for field in required_fields:
            if field not in config:
                return False
        
        valid_types = ["bar", "line", "area", "pie", "scatter", "table", "heatmap", "histogram"]
        if config.get("type") not in valid_types:
            return False
        
        return True

class CacheManager:
    """Simple in-memory cache manager."""
    
    def __init__(self, max_size: int = 100):
        """Initialize cache manager."""
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
    
    def get(self, key: str) -> Any:
        """Get value from cache."""
        if key in self.cache:
            self.access_count[key] = self.access_count.get(key, 0) + 1
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        if len(self.cache) >= self.max_size:
            # Remove least accessed item
            if self.access_count:
                least_accessed = min(self.access_count, key=self.access_count.get)
                del self.cache[least_accessed]
                del self.access_count[least_accessed]
        
        self.cache[key] = value
        self.access_count[key] = 0
    
    def clear(self) -> None:
        """Clear all cache."""
        self.cache.clear()
        self.access_count.clear()

class ErrorFormatter:
    """Utility for formatting error responses."""
    
    @staticmethod
    def format_error(error: Exception, debug: bool = False) -> Dict[str, Any]:
        """
        Format exception into error response.
        
        Args:
            error: Exception object
            debug: Whether to include debug info
            
        Returns:
            Formatted error dictionary
        """
        response = {
            "error": str(error),
            "type": error.__class__.__name__,
            "timestamp": datetime.now().isoformat()
        }
        
        if debug:
            import traceback
            response["traceback"] = traceback.format_exc()
        
        return response
