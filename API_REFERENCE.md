# API Reference Documentation

Complete API reference for the BI Dashboard Backend.

## Base URL

```
http://localhost:8000
```

## API Version

```
v1.0.0
```

## Response Format

All responses are in JSON format.

### Success Response

```json
{
  "data": {...},
  "status": "success",
  "timestamp": "2024-03-17T10:30:45.123456"
}
```

### Error Response

```json
{
  "error": "Error message",
  "status_code": 400,
  "timestamp": "2024-03-17T10:30:45.123456"
}
```

## Authentication

Currently no authentication required. For production:
- Implement API key authentication
- Use OAuth2 + JWT tokens
- Rate limiting per API key

---

# Endpoints

## Health & Status

### GET /

**Description**: Get API information and status

**Response**:
```json
{
  "name": "Business Intelligence Dashboard API",
  "version": "1.0.0",
  "status": "running",
  "timestamp": "2024-03-17T10:30:45.123456"
}
```

**Status Code**: `200 OK`

---

### GET /health

**Description**: Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-03-17T10:30:45.123456"
}
```

**Status Code**: `200 OK`

---

## Schema Management

### GET /api/schema

**Description**: Get complete database schema

**Response**:
```json
{
  "tables": [
    {
      "name": "sales",
      "type": "table",
      "columns": ["id", "date", "region", "product", "revenue"],
      "row_count": 5000
    },
    {
      "name": "employees",
      "type": "table",
      "columns": ["id", "name", "department", "salary"],
      "row_count": 50
    }
  ]
}
```

**Status Codes**: 
- `200 OK`
- `500 Internal Server Error`

---

### GET /api/tables

**Description**: List all available tables

**Response**:
```json
{
  "tables": ["sales", "employees", "products"]
}
```

**Status Codes**: 
- `200 OK`
- `500 Internal Server Error`

---

### GET /api/tables/{table_name}

**Description**: Get information about a specific table

**Path Parameters**:
- `table_name` (string, required): Name of the table

**Response**:
```json
{
  "name": "sales",
  "type": "table",
  "columns": [
    "id",
    "date",
    "region",
    "product_category",
    "product_name",
    "revenue",
    "quantity",
    "salesperson"
  ],
  "row_count": 15
}
```

**Status Codes**: 
- `200 OK`
- `404 Not Found`
- `500 Internal Server Error`

---

## Analytics

### GET /api/analytics/sample

**Description**: Get sample data from a table

**Query Parameters**:
- `table_name` (string, default: "sales"): Table to sample from
- `limit` (integer, default: 10): Number of rows (max: 100)

**Response**:
```json
{
  "table": "sales",
  "row_count": 5,
  "data": [
    {
      "id": 1,
      "date": "2024-01-01",
      "region": "North",
      "product_category": "Electronics",
      "product_name": "Laptop",
      "revenue": 5000.0,
      "quantity": 2,
      "salesperson": "John"
    }
  ]
}
```

**Status Codes**: 
- `200 OK`
- `400 Bad Request`
- `500 Internal Server Error`

---

### GET /api/analytics/columns/{table_name}

**Description**: Get column information for a table

**Path Parameters**:
- `table_name` (string, required): Table name

**Response**:
```json
{
  "table": "sales",
  "columns": [
    "id",
    "date",
    "region",
    "product_category",
    "product_name",
    "revenue",
    "quantity",
    "salesperson"
  ],
  "column_count": 8
}
```

**Status Codes**: 
- `200 OK`
- `404 Not Found`
- `500 Internal Server Error`

---

## Dashboard Management

### POST /api/dashboard/generate

**Description**: Generate an interactive dashboard from a natural language query

**Request Body** (application/json):
```json
{
  "query": "Show me monthly sales revenue broken down by region",
  "filters": {
    "region": "East"
  },
  "limit": 100,
  "data_source": "sales"
}
```

**Request Fields**:
- `query` (string, required, min 3 chars): Natural language query
- `filters` (object, optional): Filter criteria {column: value}
- `limit` (integer, optional, default 100, max 1000): Result row limit
- `data_source` (string, optional): Specific table to query

**Response** (DashboardResponse):
```json
{
  "query": "Show me monthly sales revenue broken down by region",
  "charts": [
    {
      "type": "bar",
      "title": "Sales Revenue by Region",
      "description": "Bar chart showing regional performance",
      "x_axis": "region",
      "y_axis": "revenue",
      "data": [
        {"region": "North", "revenue": 7000},
        {"region": "East", "revenue": 6200},
        {"region": "West", "revenue": 4800},
        {"region": "South", "revenue": 7300}
      ],
      "aggregation": "sum"
    },
    {
      "type": "table",
      "title": "Detailed Regional Data",
      "description": "Raw data table",
      "x_axis": "region",
      "y_axis": "revenue",
      "data": [...]
    }
  ],
  "insights": [
    "South region leads with $7,300 in revenue",
    "North region shows steady performance at $7,000",
    "West region is underperforming at $4,800",
    "Total combined revenue: $25,300"
  ],
  "summary": "The South and North regions are driving the majority of revenue, accounting for 57% of total sales.",
  "raw_data": [...],
  "execution_time_ms": 2345.67
}
```

**Status Codes**: 
- `200 OK` - Dashboard generated successfully
- `400 Bad Request` - Invalid query format
- `500 Internal Server Error` - Server error

---

### GET /api/dashboard/{dashboard_id}

**Description**: Retrieve a previously generated dashboard

**Path Parameters**:
- `dashboard_id` (string, required): Dashboard ID from generation response

**Response**: DashboardResponse (same as generate endpoint)

**Status Codes**: 
- `200 OK`
- `404 Not Found` - Dashboard not in cache
- `500 Internal Server Error`

---

### POST /api/dashboard/{dashboard_id}/follow-up

**Description**: Ask follow-up questions or modify an existing dashboard

**Path Parameters**:
- `dashboard_id` (string, required): Dashboard ID

**Request Body** (application/json):
```json
{
  "message": "Now filter this to only show the East Coast",
  "filters": {
    "region": "East"
  }
}
```

**Request Fields**:
- `message` (string, required, min 3 chars): Follow-up question or instruction
- `filters` (object, optional): Additional filters to apply

**Response**: Modified DashboardResponse

**Status Codes**: 
- `200 OK` - Follow-up processed successfully
- `400 Bad Request` - Invalid message format
- `404 Not Found` - Dashboard not found
- `500 Internal Server Error`

---

## Query Execution

### POST /api/query/execute

**Description**: Execute a raw SQL query (advanced users only)

**Query Parameters**:
- `query_text` (string, required, min 3 chars): SQL query to execute

**Response**:
```json
{
  "results": [
    {
      "id": 1,
      "region": "North",
      "revenue": 5000
    },
    {
      "id": 2,
      "region": "South",
      "revenue": 8000
    }
  ],
  "row_count": 2
}
```

**Status Codes**: 
- `200 OK` - Query executed successfully
- `400 Bad Request` - Invalid SQL query
- `500 Internal Server Error`

**Security Note**: 
- Limited to SELECT and analysis queries
- No DDL/DML operations allowed
- Results limited to 1000 rows

---

# Data Models

## DashboardQueryRequest

```json
{
  "query": "string (required, min 3 chars)",
  "filters": {
    "column_name": "value or [value1, value2]"
  },
  "limit": "integer (optional, default 100, max 1000)",
  "data_source": "string (optional)"
}
```

## DashboardResponse

```json
{
  "query": "string",
  "charts": [
    {
      "type": "bar|line|area|pie|scatter|table|heatmap|histogram",
      "title": "string",
      "description": "string",
      "x_axis": "string",
      "y_axis": "string",
      "data": [
        {
          "key": "value"
        }
      ],
      "color_scheme": "string",
      "aggregation": "sum|avg|count|min|max|none"
    }
  ],
  "insights": [
    "string"
  ],
  "summary": "string",
  "raw_data": [
    {
      "key": "value"
    }
  ],
  "execution_time_ms": "number"
}
```

## ChartConfig

```json
{
  "type": "string (bar|line|area|pie|scatter|table|heatmap|histogram)",
  "title": "string",
  "description": "string",
  "x_axis": "string",
  "y_axis": "string",
  "data": [
    {
      "key": "value"
    }
  ],
  "color_scheme": "string",
  "aggregation": "string"
}
```

## DataSourceInfo

```json
{
  "name": "string",
  "type": "string",
  "columns": [
    "string"
  ],
  "row_count": "integer"
}
```

---

# Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | OK | Request successful |
| 400 | Bad Request | Check request format, validate parameters |
| 404 | Not Found | Verify table/dashboard ID exists |
| 500 | Server Error | Check API logs, verify database connection |
| 503 | Service Unavailable | API temporarily down, retry later |

---

# Usage Examples

## Example 1: Basic Dashboard

**Request**:
```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show total sales by region"
  }'
```

**Response**: Dashboard with regional sales breakdown

## Example 2: Filtered Dashboard

**Request**:
```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show sales by product category",
    "filters": {"region": "North"},
    "limit": 50
  }'
```

**Response**: Dashboard filtered to North region only

## Example 3: Follow-up

**Request**:
```bash
curl -X POST "http://localhost:8000/api/dashboard/{dashboard_id}/follow-up" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Now show me the top 5 products"
  }'
```

**Response**: Modified dashboard with top 5 products

---

# Rate Limiting (Future)

```
- Free: 100 requests/hour
- Pro: 1000 requests/hour
- Enterprise: Unlimited
```

---

# Best Practices

1. **Query Design**
   - Be specific: "Q3 revenue" vs "revenue"
   - Use business terms: "sales", "revenue", "orders"
   - Include context: time period, region, category

2. **Performance**
   - Use reasonable limits (100-500)
   - Filter when possible
   - Cache results in frontend

3. **Error Handling**
   - Always check response status codes
   - Parse error messages for guidance
   - Retry on 5xx errors with exponential backoff

4. **Pagination**
   - Use limit parameter for large datasets
   - Implement offset if needed (future feature)
   - Cache results for repeat queries

---

# Support

- Interactive Docs: `GET /docs`
- Alternative Docs: `GET /redoc`
- API GitHub: https://github.com/...
- Email: support@...

---

**Last Updated**: March 2024  
**API Version**: 1.0.0  
**Status**: Production Ready
