from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum

class ChartType(str, Enum):
    """Supported chart types for visualization."""
    BAR = "bar"
    LINE = "line"
    AREA = "area"
    PIE = "pie"
    SCATTER = "scatter"
    TABLE = "table"
    HEATMAP = "heatmap"
    HISTOGRAM = "histogram"

class DashboardQueryRequest(BaseModel):
    """Request model for natural language dashboard query."""
    query: str
    filters: Optional[Dict[str, Any]] = None
    limit: Optional[int] = 100
    data_source: Optional[str] = None  # table name or CSV file name

class ChartConfig(BaseModel):
    """Configuration for a single chart in the dashboard."""
    type: ChartType
    title: str
    description: Optional[str] = None
    x_axis: str
    y_axis: str
    data: List[Dict[str, Any]]
    color_scheme: Optional[str] = "default"
    aggregation: Optional[str] = None  # sum, avg, count, etc.

class DashboardResponse(BaseModel):
    """Response model containing dashboard with charts and insights."""
    query: str
    charts: List[ChartConfig]
    insights: List[str]
    summary: str
    raw_data: Optional[List[Dict[str, Any]]] = None
    execution_time_ms: float

class ChatMessage(BaseModel):
    """Model for follow-up chat interaction."""
    dashboard_id: str
    message: str
    filters: Optional[Dict[str, Any]] = None

class FilterRequest(BaseModel):
    """Request model for filtering existing dashboard."""
    dashboard_id: str
    filters: Dict[str, Any]

class DataSourceInfo(BaseModel):
    """Information about available data sources."""
    name: str
    type: str  # table, csv, etc.
    columns: List[str]
    row_count: int

class DatabaseSchema(BaseModel):
    """Database schema information."""
    tables: List[DataSourceInfo]
