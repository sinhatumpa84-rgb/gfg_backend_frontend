import google.generativeai as genai
from config import settings
from typing import Dict, Any, List, Tuple
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interfacing with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini API with credentials."""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def parse_natural_language_query(self, 
                                    query: str, 
                                    schema: str,
                                    table_names: List[str]) -> Dict[str, Any]:
        """
        Convert natural language query to structured SQL query.
        
        Args:
            query: Natural language query
            schema: Database schema information
            table_names: Available table names
            
        Returns:
            Dictionary containing SQL and query metadata
        """
        prompt = f"""You are a SQL expert. Convert the following natural language query to SQL.

Database Schema:
{schema}

Available Tables: {', '.join(table_names)}

Natural Language Query: {query}

Return a JSON response with the following structure:
{{
    "sql_query": "SELECT ...",
    "tables_used": ["table1", "table2"],
    "columns_selected": ["col1", "col2"],
    "aggregations": ["sum", "avg"],
    "filters": ["filter1", "filter2"],
    "intent": "analysis or reporting"
}}

Only return valid JSON, nothing else."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            logger.error(f"Error parsing query with LLM: {e}")
            return {"error": str(e)}
    
    def recommend_chart_types(self, 
                             query: str, 
                             data_sample: List[Dict[str, Any]],
                             columns: List[str]) -> List[Dict[str, Any]]:
        """
        Recommend appropriate chart types based on query and data.
        
        Args:
            query: Original query
            data_sample: Sample of query results
            columns: Column names in the data
            
        Returns:
            List of recommended charts with configurations
        """
        prompt = f"""You are a data visualization expert. Based on the user's query and data characteristics,
recommend the best chart types to visualize this data.

User Query: {query}

Data Columns: {', '.join(columns)}

Data Sample (first few rows):
{json.dumps(data_sample[:3], indent=2)}

Return a JSON array with recommended charts:
[
    {{
        "type": "bar|line|pie|scatter|area|heatmap|table",
        "title": "clear, descriptive title",
        "description": "why this chart is good for this data",
        "x_axis": "column name",
        "y_axis": "column name",
        "recommended_aggregation": "sum|avg|count|none"
    }}
]

Return only valid JSON array, nothing else."""
        
        try:
            response = self.model.generate_content(prompt)
            recommendations = json.loads(response.text)
            return recommendations if isinstance(recommendations, list) else [recommendations]
        except Exception as e:
            logger.error(f"Error recommending charts: {e}")
            return [{"type": "table", "title": "Data Table", "description": "Default table view"}]
    
    def generate_insights(self, 
                         query: str, 
                         data: List[Dict[str, Any]],
                         aggregations: List[str]) -> Tuple[str, List[str]]:
        """
        Generate business insights from query results.
        
        Args:
            query: Original query
            data: Query results
            aggregations: Performed aggregations
            
        Returns:
            Tuple of (summary, list of insights)
        """
        prompt = f"""You are a business analyst. Analyze the following data and provide:
1. A brief summary (1-2 sentences)
2. 3-5 key business insights

User Query: {query}

Data (first 10 rows):
{json.dumps(data[:10], indent=2)}

Return JSON with structure:
{{
    "summary": "brief summary of findings",
    "insights": [
        "insight 1",
        "insight 2",
        "insight 3"
    ]
}}

Return only valid JSON, nothing else."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result.get("summary", ""), result.get("insights", [])
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return "Data analysis complete", ["Unable to generate insights at this time"]
    
    def generate_follow_up_response(self,
                                   original_query: str,
                                   follow_up_message: str,
                                   current_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate follow-up modifications to dashboard based on chat message.
        
        Args:
            original_query: Original dashboard query
            follow_up_message: User's follow-up message (e.g., "filter to East Coast")
            current_data: Current dashboard data
            
        Returns:
            Dictionary with filter instructions and modifications
        """
        prompt = f"""You are a data filtering expert. The user wants to modify their dashboard.

Original Query: {original_query}

Follow-up Message: {follow_up_message}

Current Data Sample:
{json.dumps(current_data[:5], indent=2)}

Provide modification instructions as JSON:
{{
    "action": "filter|aggregate|modify",
    "filters": {{"column": "value"}},
    "explanation": "what the modification does"
}}

Return only valid JSON, nothing else."""
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            logger.error(f"Error processing follow-up: {e}")
            return {"action": "none", "explanation": "Unable to process follow-up"}

# Initialize service
llm_service = LLMService()
