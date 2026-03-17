import json
import logging
import time
from typing import Dict, Any, List, Optional
import uuid
from models import DashboardResponse, ChartConfig, ChartType
from llm_service import llm_service
from database_service import db_service
from data_processing_service import data_processing_service

logger = logging.getLogger(__name__)

class DashboardService:
    """Service for orchestrating dashboard generation from natural language queries."""
    
    def __init__(self):
        """Initialize dashboard service."""
        self.dashboards_cache = {}  # Simple in-memory cache for dashboards
    
    def generate_dashboard(self, 
                          query: str, 
                          filters: Optional[Dict[str, Any]] = None,
                          limit: int = 100,
                          data_source: Optional[str] = None) -> DashboardResponse:
        """
        Generate a complete dashboard from a natural language query.
        
        Args:
            query: Natural language query
            filters: Optional filters to apply
            limit: Maximum rows to return
            data_source: Specific table/CSV to query
            
        Returns:
            DashboardResponse with charts and insights
        """
        start_time = time.time()
        
        try:
            logger.info(f"Starting dashboard generation for query: {query}")
            
            # Step 1: Get database schema
            schema_str = db_service.get_table_schema_string()
            available_tables = db_service.get_available_tables()
            
            # Step 2: Parse query with LLM to get SQL
            logger.info("Parsing natural language query...")
            parsed_query = llm_service.parse_natural_language_query(
                query=query,
                schema=schema_str,
                table_names=available_tables
            )
            
            if "error" in parsed_query:
                logger.error(f"Error parsing query: {parsed_query['error']}")
                raise Exception(f"Failed to parse query: {parsed_query['error']}")
            
            logger.info(f"Parsed query: {json.dumps(parsed_query, indent=2)}")
            
            # Step 3: Execute SQL query
            logger.info("Executing database query...")
            sql_query = parsed_query.get("sql_query")
            if not sql_query:
                raise Exception("No SQL query generated")
            
            raw_data = db_service.execute_query(sql_query)
            
            if not raw_data:
                logger.warning("Query returned no results")
                raw_data = []
            
            logger.info(f"Retrieved {len(raw_data)} rows")
            
            # Step 4: Apply filters if provided
            if filters:
                logger.info(f"Applying filters: {filters}")
                raw_data = data_processing_service.filter_data(raw_data, filters)
            
            # Step 5: Limit data
            raw_data = data_processing_service.limit_data(raw_data, limit)
            
            # Step 6: Get data statistics
            stats = data_processing_service.get_data_statistics(raw_data)
            logger.info(f"Data stats: {json.dumps(stats, indent=2)}")
            
            # Step 7: Recommend chart types with LLM
            logger.info("Recommending chart types...")
            chart_recommendations = llm_service.recommend_chart_types(
                query=query,
                data_sample=raw_data,
                columns=stats.get("columns", [])
            )
            
            logger.info(f"Chart recommendations: {json.dumps(chart_recommendations, indent=2)}")
            
            # Step 8: Build chart configurations
            charts = []
            for i, rec in enumerate(chart_recommendations[:3]):  # Limit to 3 charts
                try:
                    chart = self._build_chart(
                        recommendation=rec,
                        data=raw_data,
                        query=query
                    )
                    if chart:
                        charts.append(chart)
                except Exception as e:
                    logger.error(f"Error building chart {i}: {e}")
                    continue
            
            # If no charts were built, add a default table
            if not charts:
                charts.append(ChartConfig(
                    type=ChartType.TABLE,
                    title="Query Results",
                    description="Raw data from query",
                    x_axis="index",
                    y_axis="value",
                    data=raw_data[:50]
                ))
            
            # Step 9: Generate insights with LLM
            logger.info("Generating insights...")
            summary, insights = llm_service.generate_insights(
                query=query,
                data=raw_data,
                aggregations=parsed_query.get("aggregations", [])
            )
            
            logger.info(f"Generated summary and {len(insights)} insights")
            
            # Step 10: Create dashboard response
            execution_time = (time.time() - start_time) * 1000  # Convert to ms
            
            dashboard = DashboardResponse(
                query=query,
                charts=charts,
                insights=insights,
                summary=summary,
                raw_data=raw_data[:20],  # Include sample of raw data
                execution_time_ms=execution_time
            )
            
            # Cache dashboard
            dashboard_id = str(uuid.uuid4())
            self.dashboards_cache[dashboard_id] = {
                "dashboard": dashboard,
                "query": query,
                "raw_data": raw_data,
                "parsed_query": parsed_query
            }
            
            logger.info(f"Dashboard generated successfully in {execution_time:.2f}ms")
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}", exc_info=True)
            raise
    
    def _build_chart(self, 
                    recommendation: Dict[str, Any], 
                    data: List[Dict[str, Any]],
                    query: str) -> Optional[ChartConfig]:
        """
        Build a chart configuration from recommendation and data.
        
        Args:
            recommendation: Chart recommendation from LLM
            data: Processed data for the chart
            query: Original query
            
        Returns:
            ChartConfig or None if chart cannot be built
        """
        try:
            chart_type = recommendation.get("type", "table")
            x_axis = recommendation.get("x_axis", "")
            y_axis = recommendation.get("y_axis", "")
            
            # Validate chart type
            try:
                chart_type_enum = ChartType[chart_type.upper()]
            except KeyError:
                chart_type_enum = ChartType.TABLE
            
            # Process data for chart
            if data:
                chart_data = data_processing_service.process_for_chart(
                    data=data,
                    x_axis=x_axis,
                    y_axis=y_axis,
                    chart_type=chart_type_enum
                )
            else:
                chart_data = []
            
            chart = ChartConfig(
                type=chart_type_enum,
                title=recommendation.get("title", "Chart"),
                description=recommendation.get("description", ""),
                x_axis=x_axis,
                y_axis=y_axis,
                data=chart_data,
                aggregation=recommendation.get("recommended_aggregation")
            )
            
            return chart
        except Exception as e:
            logger.error(f"Error building chart: {e}")
            return None
    
    def handle_follow_up(self,
                        dashboard_id: str,
                        follow_up_message: str) -> Optional[DashboardResponse]:
        """
        Handle follow-up questions/modifications to a dashboard.
        
        Args:
            dashboard_id: ID of the cached dashboard
            follow_up_message: User's follow-up message
            
        Returns:
            Modified DashboardResponse or None
        """
        try:
            if dashboard_id not in self.dashboards_cache:
                logger.error(f"Dashboard {dashboard_id} not found in cache")
                return None
            
            cached = self.dashboards_cache[dashboard_id]
            original_query = cached["query"]
            raw_data = cached["raw_data"]
            
            logger.info(f"Processing follow-up: {follow_up_message}")
            
            # Get modification instructions from LLM
            modification = llm_service.generate_follow_up_response(
                original_query=original_query,
                follow_up_message=follow_up_message,
                current_data=raw_data
            )
            
            logger.info(f"Modification: {json.dumps(modification, indent=2)}")
            
            # Apply modifications
            modified_data = raw_data
            
            if modification.get("action") == "filter":
                filters = modification.get("filters", {})
                modified_data = data_processing_service.filter_data(modified_data, filters)
            
            elif modification.get("action") == "aggregate":
                # Regenerate dashboard with modified data
                pass
            
            # Generate new dashboard with modified data
            new_dashboard = self._build_modified_dashboard(
                original_dashboard=cached["dashboard"],
                modified_data=modified_data,
                query=original_query,
                follow_up=follow_up_message
            )
            
            # Update cache
            self.dashboards_cache[dashboard_id]["dashboard"] = new_dashboard
            self.dashboards_cache[dashboard_id]["raw_data"] = modified_data
            
            return new_dashboard
            
        except Exception as e:
            logger.error(f"Error handling follow-up: {e}", exc_info=True)
            return None
    
    def _build_modified_dashboard(self,
                                 original_dashboard: DashboardResponse,
                                 modified_data: List[Dict[str, Any]],
                                 query: str,
                                 follow_up: str) -> DashboardResponse:
        """
        Build a modified dashboard based on follow-up changes.
        
        Args:
            original_dashboard: Original DashboardResponse
            modified_data: Modified data after filters/aggregation
            query: Original query
            follow_up: Follow-up message
            
        Returns:
            New DashboardResponse with modified data
        """
        try:
            # Rebuild charts with modified data
            charts = []
            for chart_rec in original_dashboard.charts:
                # Process modified data for each chart
                chart_data = data_processing_service.process_for_chart(
                    data=modified_data,
                    x_axis=chart_rec.x_axis,
                    y_axis=chart_rec.y_axis,
                    chart_type=chart_rec.type
                )
                
                chart = ChartConfig(
                    type=chart_rec.type,
                    title=chart_rec.title,
                    description=chart_rec.description,
                    x_axis=chart_rec.x_axis,
                    y_axis=chart_rec.y_axis,
                    data=chart_data,
                    aggregation=chart_rec.aggregation
                )
                charts.append(chart)
            
            # Generate new insights
            summary, insights = llm_service.generate_insights(
                query=f"{query} (Follow-up: {follow_up})",
                data=modified_data,
                aggregations=[]
            )
            
            return DashboardResponse(
                query=f"{query} - {follow_up}",
                charts=charts,
                insights=insights,
                summary=summary,
                raw_data=modified_data[:20],
                execution_time_ms=0
            )
        except Exception as e:
            logger.error(f"Error building modified dashboard: {e}")
            return original_dashboard
    
    def get_dashboard(self, dashboard_id: str) -> Optional[DashboardResponse]:
        """
        Retrieve a cached dashboard.
        
        Args:
            dashboard_id: ID of the dashboard
            
        Returns:
            DashboardResponse or None
        """
        cached = self.dashboards_cache.get(dashboard_id)
        return cached["dashboard"] if cached else None

# Initialize service
dashboard_service = DashboardService()
