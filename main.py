from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import traceback

from config import settings
from models import (
    DashboardQueryRequest, 
    DashboardResponse, 
    ChatMessage,
    DatabaseSchema,
    DataSourceInfo
)
from dashboard_service import dashboard_service
from database_service import db_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API for generating interactive data dashboards from natural language queries"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================== Health Check Endpoints ========================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }

# ======================== Schema Endpoints ========================

@app.get("/api/schema", response_model=DatabaseSchema, tags=["Schema"])
async def get_database_schema():
    """
    Get the database schema information including all tables and columns.
    
    Returns:
        DatabaseSchema: Information about all available tables
    """
    try:
        schema = db_service.get_schema()
        tables = list(schema.values())
        return DatabaseSchema(tables=tables)
    except Exception as e:
        logger.error(f"Error fetching schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tables", tags=["Schema"])
async def list_tables():
    """
    Get list of available tables/data sources.
    
    Returns:
        List of table names
    """
    try:
        tables = db_service.get_available_tables()
        return {"tables": tables}
    except Exception as e:
        logger.error(f"Error listing tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tables/{table_name}", tags=["Schema"])
async def get_table_info(table_name: str):
    """
    Get information about a specific table.
    
    Args:
        table_name: Name of the table
        
    Returns:
        Table metadata including columns and row count
    """
    try:
        schema = db_service.get_schema()
        if table_name not in schema:
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
        
        table_info = schema[table_name]
        return {
            "name": table_info.name,
            "type": table_info.type,
            "columns": table_info.columns,
            "row_count": table_info.row_count
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching table info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ======================== Dashboard Endpoints ========================

@app.post("/api/dashboard/generate", response_model=DashboardResponse, tags=["Dashboard"])
async def generate_dashboard(request: DashboardQueryRequest):
    """
    Generate an interactive dashboard from a natural language query.
    
    This endpoint takes a plain-English query, analyzes it with an LLM,
    executes the appropriate database query, and generates visualization
    recommendations with business insights.
    
    Args:
        request: DashboardQueryRequest containing the natural language query
        
    Returns:
        DashboardResponse: Complete dashboard with charts and insights
        
    Example:
        {
            "query": "Show me the monthly sales revenue for Q3 broken down by region",
            "filters": {"region": "East"},
            "limit": 100
        }
    """
    try:
        logger.info(f"Dashboard generation request: {request.query}")
        
        # Validate query
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )
        
        # Generate dashboard
        dashboard = dashboard_service.generate_dashboard(
            query=request.query,
            filters=request.filters,
            limit=request.limit or 100,
            data_source=request.data_source
        )
        
        logger.info("Dashboard generated successfully")
        return dashboard
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating dashboard: {str(e)}"
        )

@app.get("/api/dashboard/{dashboard_id}", response_model=DashboardResponse, tags=["Dashboard"])
async def get_dashboard(dashboard_id: str):
    """
    Retrieve a previously generated dashboard from cache.
    
    Args:
        dashboard_id: ID of the dashboard
        
    Returns:
        DashboardResponse: The cached dashboard
    """
    try:
        dashboard = dashboard_service.get_dashboard(dashboard_id)
        if not dashboard:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        return dashboard
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ======================== Chat/Follow-up Endpoints ========================

@app.post("/api/dashboard/{dashboard_id}/follow-up", response_model=DashboardResponse, tags=["Dashboard"])
async def follow_up_question(dashboard_id: str, message: ChatMessage):
    """
    Ask a follow-up question or request modifications to an existing dashboard.
    
    This allows users to refine their dashboard with additional filters,
    aggregations, or drill-down queries.
    
    Args:
        dashboard_id: ID of the dashboard to modify
        message: ChatMessage with follow-up question
        
    Returns:
        DashboardResponse: Modified dashboard with new charts
        
    Example:
        {
            "message": "Now filter this to only show the East Coast",
            "filters": {"region": "East"}
        }
    """
    try:
        logger.info(f"Follow-up question for dashboard {dashboard_id}: {message.message}")
        
        if not message.message or len(message.message.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Message must be at least 3 characters long"
            )
        
        dashboard = dashboard_service.handle_follow_up(
            dashboard_id=dashboard_id,
            follow_up_message=message.message
        )
        
        if not dashboard:
            raise HTTPException(status_code=404, detail="Dashboard not found")
        
        logger.info("Follow-up processed successfully")
        return dashboard
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing follow-up: {e}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing follow-up: {str(e)}"
        )

# ======================== Query Endpoints ========================

@app.post("/api/query/execute", tags=["Query"])
async def execute_query(query_text: str = Query(..., min_length=3, description="SQL query to execute")):
    """
    Execute a raw SQL query against the database.
    
    **Warning**: This endpoint is for advanced users and requires SQL knowledge.
    Use the /api/dashboard/generate endpoint for natural language queries.
    
    Args:
        query_text: SQL query to execute
        
    Returns:
        Query results as list of dictionaries
    """
    try:
        logger.info(f"Executing raw query: {query_text}")
        
        # Limit query results for safety
        results = db_service.execute_query(query_text)
        return {
            "results": results[:1000],  # Limit to 1000 rows
            "row_count": len(results)
        }
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise HTTPException(status_code=400, detail=f"Query error: {str(e)}")

# ======================== Analytics Endpoints ========================

@app.get("/api/analytics/sample", tags=["Analytics"])
async def get_sample_data(table_name: str = Query("sales", description="Table to sample from"), 
                         limit: int = Query(10, description="Number of rows to return")):
    """
    Get sample data from a table for exploration.
    
    Args:
        table_name: Name of the table to sample
        limit: Maximum number of rows to return
        
    Returns:
        Sample data from the table
    """
    try:
        query = f"SELECT * FROM {table_name} LIMIT {min(limit, 100)}"
        results = db_service.execute_query(query)
        return {
            "table": table_name,
            "row_count": len(results),
            "data": results
        }
    except Exception as e:
        logger.error(f"Error getting sample data: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/columns/{table_name}", tags=["Analytics"])
async def get_column_info(table_name: str):
    """
    Get detailed information about columns in a table.
    
    Args:
        table_name: Name of the table
        
    Returns:
        Column metadata including data types
    """
    try:
        schema = db_service.get_schema()
        if table_name not in schema:
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
        
        table_info = schema[table_name]
        return {
            "table": table_name,
            "columns": table_info.columns,
            "column_count": len(table_info.columns)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting column info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ======================== Error Handlers ========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": str(exc) if settings.debug else "An error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# ======================== Startup/Shutdown ========================

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.api_title} v{settings.api_version}")
    logger.info(f"Database Type: {settings.database_type}")
    logger.info(f"Debug Mode: {settings.debug}")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
