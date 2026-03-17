import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from models import ChartConfig, ChartType

logger = logging.getLogger(__name__)

class DataProcessingService:
    """Service for data transformation and aggregation."""
    
    @staticmethod
    def aggregate_data(data: List[Dict[str, Any]], 
                      group_by: List[str], 
                      aggregations: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Aggregate data by grouping and applying aggregation functions.
        
        Args:
            data: Raw data
            group_by: Columns to group by
            aggregations: Dict of {column: aggregation_function}
                         Functions: sum, avg, count, min, max
            
        Returns:
            Aggregated data
        """
        try:
            if not data or not group_by:
                return data
            
            df = pd.DataFrame(data)
            
            # Perform aggregation
            agg_dict = {}
            for col, func in aggregations.items():
                if col in df.columns:
                    agg_dict[col] = func.lower()
            
            if not agg_dict:
                agg_dict = {df.columns[0]: 'count'}
            
            result_df = df.groupby(group_by).agg(agg_dict).reset_index()
            return result_df.to_dict('records')
        except Exception as e:
            logger.error(f"Error aggregating data: {e}")
            return data
    
    @staticmethod
    def process_for_chart(data: List[Dict[str, Any]], 
                         x_axis: str, 
                         y_axis: str,
                         chart_type: ChartType) -> List[Dict[str, Any]]:
        """
        Process data for specific chart type.
        
        Args:
            data: Raw data
            x_axis: X-axis column name
            y_axis: Y-axis column name
            chart_type: Type of chart
            
        Returns:
            Processed data ready for charting
        """
        try:
            df = pd.DataFrame(data)
            
            if chart_type == ChartType.TABLE:
                return data
            
            # For other chart types, ensure we have required columns
            required_cols = [col for col in [x_axis, y_axis] if col]
            available_cols = [col for col in required_cols if col in df.columns]
            
            if not available_cols:
                return data
            
            # Select and prepare data
            select_cols = available_cols
            result_df = df[select_cols]
            
            # Remove duplicates for x-axis aggregation
            if len(available_cols) > 1:
                result_df = result_df.drop_duplicates()
            
            return result_df.to_dict('records')
        except Exception as e:
            logger.error(f"Error processing data for chart: {e}")
            return data
    
    @staticmethod
    def get_data_statistics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate basic statistics about the data.
        
        Args:
            data: Raw data
            
        Returns:
            Dictionary with statistics
        """
        try:
            df = pd.DataFrame(data)
            
            stats = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "columns": list(df.columns),
                "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
                "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            }
            
            # Add numeric summaries
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                stats["numeric_stats"] = numeric_df.describe().to_dict()
            
            return stats
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def filter_data(data: List[Dict[str, Any]], 
                   filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter data based on filter criteria.
        
        Args:
            data: Raw data
            filters: Dictionary of {column: value} or {column: [value1, value2]}
            
        Returns:
            Filtered data
        """
        try:
            if not filters or not data:
                return data
            
            df = pd.DataFrame(data)
            
            for column, value in filters.items():
                if column not in df.columns:
                    continue
                
                if isinstance(value, list):
                    df = df[df[column].isin(value)]
                else:
                    df = df[df[column] == value]
            
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            return data
    
    @staticmethod
    def sort_data(data: List[Dict[str, Any]], 
                 sort_by: str, 
                 ascending: bool = True) -> List[Dict[str, Any]]:
        """
        Sort data by a column.
        
        Args:
            data: Raw data
            sort_by: Column name to sort by
            ascending: Sort order
            
        Returns:
            Sorted data
        """
        try:
            df = pd.DataFrame(data)
            
            if sort_by not in df.columns:
                return data
            
            result_df = df.sort_values(by=sort_by, ascending=ascending)
            return result_df.to_dict('records')
        except Exception as e:
            logger.error(f"Error sorting data: {e}")
            return data
    
    @staticmethod
    def limit_data(data: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """
        Limit data to specified number of rows.
        
        Args:
            data: Raw data
            limit: Maximum rows to return
            
        Returns:
            Limited data
        """
        return data[:limit] if limit > 0 else data

# Initialize service
data_processing_service = DataProcessingService()
