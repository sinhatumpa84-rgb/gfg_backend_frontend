# Business Intelligence Dashboard Backend API

An intelligent backend system that converts natural language queries into interactive data dashboards using FastAPI, Google Gemini LLM, and SQLAlchemy.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Database Setup](#database-setup)
- [Troubleshooting](#troubleshooting)

## Overview

This backend service enables non-technical users to generate fully functional, interactive data dashboards using only natural language prompts. The system:

1. **Parses natural language queries** using Google Gemini LLM
2. **Converts them to SQL** queries based on database schema
3. **Executes queries** against SQLite, PostgreSQL, or CSV data
4. **Recommends optimal chart types** for visualization
5. **Generates business insights** from the data
6. **Supports follow-up questions** for dashboard refinement

### Key Features

- 🤖 **Natural Language Processing**: Convert plain English to database queries
- 📊 **Smart Chart Selection**: AI-powered recommendations for optimal visualizations
- 💡 **Business Insights**: Automatic generation of key findings
- 🔄 **Interactive Follow-ups**: Refine dashboards with follow-up questions
- 📈 **Multiple Chart Types**: Bar, Line, Area, Pie, Scatter, Heatmap, Table
- 🗄️ **Multi-Database Support**: SQLite, PostgreSQL, CSV
- ⚡ **Fast Execution**: Optimized data processing and aggregation
- 🔒 **Security**: Input validation and error handling

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vue)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST
┌─────────────────────▼───────────────────────────────────────┐
│                   FastAPI Application                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         API Routes & Request Handlers               │   │
│  └──────────────────────────────────────────────────────┘   │
└────────┬────────────┬────────────┬──────────────────────────┘
         │            │            │
    ┌────▼────┐  ┌────▼────┐  ┌──▼────────┐
    │  LLM    │  │Database │  │  Data     │
    │Service  │  │Service  │  │Processing│
    │(Gemini) │  │(SQLAlch)│  │ Service   │
    └────┬────┘  └────┬────┘  └──┬────────┘
         │            │          │
    ┌────▼────────────▼──────────▼───────┐
    │   Dashboard Service (Orchestrator)  │
    └──────────────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │    Database Layer                  │
    │  ┌──────────────────────────────┐ │
    │  │SQLite / PostgreSQL / CSV Files│ │
    │  └──────────────────────────────┘ │
    └────────────────────────────────────┘
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google Gemini API key (from [https://ai.google.dev](https://ai.google.dev))
- For PostgreSQL: PostgreSQL server (optional)

### Installation

1. **Clone or navigate to the backend directory**

```bash
cd backend
```

2. **Create a virtual environment** (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

5. **Run the application**

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**View API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
DATABASE_TYPE=sqlite  # Options: sqlite, postgresql
DATABASE_URL=sqlite:///./bi_dashboard.db

# For PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Server Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# CSV Data Storage
CSV_DATA_PATH=./data/
```

### Database Configuration

#### SQLite (Default)

The default setup uses SQLite with sample sales and employee data. No additional setup required!

```env
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./bi_dashboard.db
```

#### PostgreSQL

For production use with PostgreSQL:

```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/bi_dashboard
```

Then run migrations to set up tables.

## API Documentation

### Base URL

```
http://localhost:8000
```

### Authentication

Currently, no authentication is required. For production, implement API key or OAuth2 authentication.

### Endpoints

#### 1. Generate Dashboard from Natural Language Query

**POST** `/api/dashboard/generate`

Convert a natural language query into an interactive dashboard.

**Request Body:**
```json
{
  "query": "Show me the monthly sales revenue for Q3 broken down by region",
  "filters": {
    "region": "East"
  },
  "limit": 100,
  "data_source": "sales"
}
```

**Response:**
```json
{
  "query": "Show me the monthly sales revenue...",
  "charts": [
    {
      "type": "bar",
      "title": "Monthly Sales Revenue by Region",
      "description": "Bar chart showing regional revenue trends",
      "x_axis": "region",
      "y_axis": "revenue",
      "data": [
        {"region": "East", "revenue": 15000},
        {"region": "West", "revenue": 12000}
      ],
      "aggregation": "sum"
    }
  ],
  "insights": [
    "East Coast shows the highest revenue at $15k",
    "West Coast revenue decreased 8% compared to previous period",
    "North region shows steady growth"
  ],
  "summary": "Q3 revenue analysis reveals strong East Coast performance",
  "raw_data": [...],
  "execution_time_ms": 1250.5
}
```

**Status Codes:**
- `200`: Dashboard generated successfully
- `400`: Invalid query format
- `500`: Server error

#### 2. Ask Follow-up Questions

**POST** `/api/dashboard/{dashboard_id}/follow-up`

Refine an existing dashboard with follow-up questions.

**Request Body:**
```json
{
  "message": "Now filter this to only show the East Coast",
  "filters": {}
}
```

**Response:** Modified DashboardResponse

#### 3. Get Database Schema

**GET** `/api/schema`

Retrieve information about all tables and columns.

**Response:**
```json
{
  "tables": [
    {
      "name": "sales",
      "type": "table",
      "columns": ["id", "date", "region", "product", "revenue"],
      "row_count": 1000
    }
  ]
}
```

#### 4. List Available Tables

**GET** `/api/tables`

Get list of all available data sources.

**Response:**
```json
{
  "tables": ["sales", "employees", "products"]
}
```

#### 5. Get Table Information

**GET** `/api/tables/{table_name}`

Get detailed information about a specific table.

**Response:**
```json
{
  "name": "sales",
  "type": "table",
  "columns": ["id", "date", "region", "product", "revenue", "quantity"],
  "row_count": 5000
}
```

#### 6. Get Sample Data

**GET** `/api/analytics/sample?table_name=sales&limit=10`

Get sample data from a table for exploration.

**Query Parameters:**
- `table_name` (string): Table to sample from (default: "sales")
- `limit` (integer): Number of rows (default: 10, max: 100)

#### 7. Get Column Information

**GET** `/api/analytics/columns/{table_name}`

Get detailed information about columns in a table.

#### 8. Execute Raw SQL Query

**POST** `/api/query/execute?query_text=SELECT * FROM sales LIMIT 10`

Execute a raw SQL query (advanced users).

**Warning**: Use with caution and validate all queries.

#### 9. Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-03-17T10:30:45.123456"
}
```

## Usage Examples

### Example 1: Simple Revenue Analysis

```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me total sales revenue by region"
  }'
```

### Example 2: With Filters

```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me quarterly revenue trends by product category",
    "filters": {
      "region": "North"
    },
    "limit": 100
  }'
```

### Example 3: Follow-up Question

```bash
# First, generate initial dashboard and get dashboard_id from response

curl -X POST "http://localhost:8000/api/dashboard/{dashboard_id}/follow-up" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Now show me the top 5 best-selling products"
  }'
```

### Example 4: Get Sales Data Sample

```bash
curl -X GET "http://localhost:8000/api/analytics/sample?table_name=sales&limit=5"
```

### Python Client Example

```python
import requests
import json

API_BASE = "http://localhost:8000"

# Generate dashboard
response = requests.post(
    f"{API_BASE}/api/dashboard/generate",
    json={
        "query": "Show me monthly sales revenue broken down by region",
        "limit": 100
    }
)

dashboard = response.json()
print(f"Generated {len(dashboard['charts'])} charts")
print(f"Summary: {dashboard['summary']}")

# Process follow-up
dashboard_id = "returned-id"  # From response header or stored
follow_up = requests.post(
    f"{API_BASE}/api/dashboard/{dashboard_id}/follow-up",
    json={
        "message": "Filter to only East Coast sales"
    }
)

updated_dashboard = follow_up.json()
print(updated_dashboard)
```

## Database Setup

### Sample Data

The SQLite database comes pre-populated with sample data for demonstration:

**Sales Table:**
- Columns: id, date, region, product_category, product_name, revenue, quantity, salesperson
- Sample data: Monthly sales across 4 regions (North, South, East, West)

**Employees Table:**
- Columns: id, name, department, salary, hire_date
- Sample data: 4 sales representatives

### Adding Your Own Data

#### Option 1: SQLite

Connect using any SQLite client and import data:

```bash
sqlite3 bi_dashboard.db
```

#### Option 2: CSV Files

Place CSV files in `./data/` directory and configure accordingly.

#### Option 3: PostgreSQL

Update `.env`:
```env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/bi_dashboard
```

## Project Structure

```
backend/
├── main.py                      # FastAPI application and routes
├── config.py                    # Configuration and settings
├── models.py                    # Pydantic models for requests/responses
├── llm_service.py              # Google Gemini LLM integration
├── database_service.py         # Database operations (SQLite, PostgreSQL, CSV)
├── data_processing_service.py  # Data aggregation and transformation
├── dashboard_service.py        # Main orchestration service
├── utils.py                    # Utility functions and helpers
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .env                       # Actual environment variables (gitignored)
├── bi_dashboard.db           # SQLite database (auto-created)
└── data/                      # CSV data files (optional)
```

## Key Components

### LLM Service (`llm_service.py`)

Handles all LLM interactions:
- Parse natural language queries to SQL
- Recommend chart types
- Generate business insights
- Process follow-up questions

### Database Service (`database_service.py`)

Manages database operations:
- Execute SQL queries
- Retrieve schema information
- Support multiple database types
- Initialize sample data

### Data Processing Service (`data_processing_service.py`)

Transforms and prepares data:
- Aggregation and grouping
- Filtering and sorting
- Chart data preparation
- Statistical analysis

### Dashboard Service (`dashboard_service.py`)

Orchestrates the complete workflow:
- Coordinates LLM, database, and processing services
- Manages dashboard caching
- Handles follow-up interactions

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution**: Make sure `.env` file exists and contains:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Issue: "Database connection failed"

**Solution**: Check .env DATABASE_URL and ensure database file exists:
```env
DATABASE_URL=sqlite:///./bi_dashboard.db
```

### Issue: "No results from query"

**Solution**: 
1. Check database contains data: `/api/tables`
2. Verify schema: `/api/schema`
3. Get sample data: `/api/analytics/sample?table_name=sales`

### Issue: "LLM service timeout"

**Solution**: Increase timeout in `config.py` or check Gemini API quota

### Issue: "CORS errors from frontend"

**Solution**: `CORS_ORIGINS` in `.env` or `config.py`:
```env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

## Performance Optimization

### Query Limits
- Default limit: 100 rows
- Maximum limit: 1000 rows per query
- Customize in `DashboardQueryRequest`

### Caching
- Dashboards cached in memory (100 max by default)
- Customize cache size in `dashboard_service.py`

### Database Indexing
For PostgreSQL, add indexes on frequently queried columns:
```sql
CREATE INDEX idx_sales_region ON sales(region);
CREATE INDEX idx_sales_date ON sales(date);
```

## Security Considerations

1. **Input Validation**: All queries validated for safety
2. **SQL Injection**: Parameterized queries used throughout
3. **Rate Limiting**: Implement rate limiting for production
4. **Authentication**: Add API key or OAuth2 for production
5. **HTTPS**: Use HTTPS in production environments
6. **Environment Variables**: Never commit `.env` file

## Production Deployment

### Recommendations

1. Use PostgreSQL instead of SQLite
2. Implement authentication/authorization
3. Add rate limiting and request validation
4. Set DEBUG=False in production
5. Use a production ASGI server (Gunicorn, Hypercorn)
6. Implement logging and monitoring
7. Add database connection pooling

### Deployment Command

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

## Contributing

Guidelines for extending the backend:

1. Add new chart types in `models.py`
2. Extend LLM prompts in `llm_service.py`
3. Add data processing functions in `data_processing_service.py`
4. Create new API endpoints in `main.py`

## License

[Your License Here]

## Support

For issues and questions:
1. Check [Troubleshooting](#troubleshooting)
2. Review API Documentation
3. Check logs in console output

---

**Built with:**
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/)
- [Pandas](https://pandas.pydata.org/)
