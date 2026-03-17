# Example Queries for Testing

This file contains example natural language queries you can use to test the BI Dashboard API.

## Basic Queries

### 1. Simple Aggregation
```
"Show me total revenue by region"
```

Expected Result: Bar chart showing total revenue for each region with business insights about which region performs best.

### 2. Time Series
```
"Display monthly sales trend over the last quarter"
```

Expected Result: Line chart showing revenue progression over time with trend insights.

### 3. Product Analysis
```
"What are the top selling products by category"
```

Expected Result: Bar or pie chart showing product performance within each category.

## Intermediate Queries

### 4. Multi-dimensional Analysis
```
"Show me sales revenue by region and product category as a breakdown"
```

Expected Result: Multiple charts including bar chart and table showing combined dimensions.

### 5. Comparative Analysis
```
"Compare Q3 performance across all four regions - highlight the best and worst performers"
```

Expected Result: Multiple visualization types comparing regional performance with insights.

### 6. Sales Performance
```
"Which salesperson generated the most revenue in each region?"
```

Expected Result: Bar chart or table showing top salesperson per region.

## Advanced Queries

### 7. Complex Aggregation
```
"Calculate average order value by product category and region for the East Coast"
```

Expected Result: Heatmap or table showing detailed metrics across dimensions.

### 8. Trend Analysis with Filters
```
"Show me the revenue trend for electronics products in the North region over the past 3 months"
```

Expected Result: Line chart with trend analysis for specific subset of data.

### 9. Distribution Analysis
```
"What's the distribution of order quantities across different products?"
```

Expected Result: Histogram or distribution chart showing quantity patterns.

### 10. Insight-Focused Query
```
"Identify which regions show declining sales trends and which products are failing to meet expectations"
```

Expected Result: Dashboard with multiple charts highlighting problem areas and insights.

## Using with cURL

### Query 1: Basic Aggregation
```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me total revenue by region",
    "limit": 100
  }'
```

### Query 2: With Filters
```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Display monthly sales trend",
    "filters": {"region": "East"},
    "limit": 100
  }'
```

### Query 3: Follow-up
First, run a basic query to get the dashboard_id, then:
```bash
curl -X POST "http://localhost:8000/api/dashboard/{dashboard_id}/follow-up" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Now show me only the top 3 products"
  }'
```

## Using with Python

```python
import requests
import json

API_BASE = "http://localhost:8000"

queries = [
    "Show me total revenue by region",
    "Display monthly sales trend over the last quarter",
    "What are the top selling products by category",
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    
    response = requests.post(
        f"{API_BASE}/api/dashboard/generate",
        json={"query": query, "limit": 100}
    )
    
    result = response.json()
    
    print(f"Generated {len(result['charts'])} charts")
    print(f"Summary: {result['summary']}")
    print(f"Insights:")
    for insight in result['insights']:
        print(f"  - {insight}")
    print(f"Execution time: {result['execution_time_ms']:.2f}ms")
```

## Using with Postman

1. Create a new POST request
2. Set URL to: `http://localhost:8000/api/dashboard/generate`
3. Set headers:
   - `Content-Type: application/json`
4. Set body (raw JSON):
```json
{
  "query": "Show me total revenue by region",
  "filters": null,
  "limit": 100
}
```
5. Click Send

## Progressive Complexity

### Level 1: Simple (Good for beginners)
- Single aggregation: "Show total sales by region"
- Simple filter: "Show East region sales"
- Single chart output expected

### Level 2: Intermediate
- Multi-dimensional: "Revenue by region and product"
- Time series: "Monthly trend"
- Multiple charts in dashboard

### Level 3: Advanced
- Complex filters: "Electronics in East region last quarter"
- Comparative: "Compare top regions"
- Insights-focused: "What's failing and why"
- Follow-up interactions

## Tips for Best Results

1. **Be Specific**: "Show me Q3 revenue by region" is better than "show revenue"
2. **Use Business Terms**: "sales", "revenue", "orders" instead of generic terms
3. **Add Context**: Include time periods, regions, or categories when relevant
4. **Ask Follow-ups**: Use the follow-up feature to progressively refine results

## Expected Chart Types

The system will automatically recommend:
- **Bar Chart**: Category comparisons, regional breakdowns
- **Line Chart**: Time series, trends
- **Pie Chart**: Part-to-whole relationships
- **Area Chart**: Cumulative trends
- **Scatter Plot**: Relationship analysis
- **Table**: Detailed data view
- **Heatmap**: Multi-dimensional relationships
- **Histogram**: Distribution analysis

## Testing Checklist

- [ ] API is running (`/health` returns 200)
- [ ] Database has sample data (`/api/analytics/sample` returns data)
- [ ] Simple query works (`"Show me total sales by region"`)
- [ ] Filters work (add region filter to above query)
- [ ] Follow-up works (ask to filter or modify existing dashboard)
- [ ] Multiple chart types render correctly
- [ ] Insights are generated and relevant
- [ ] Response times are acceptable (<5 seconds)

## Common Pitfalls

1. **API Key not configured**: Check .env has valid GEMINI_API_KEY
2. **Database empty**: Ensure sample data is initialized
3. **Query too complex**: Start simple and build up
4. **Timeout errors**: LLM might be slow, increase timeout
5. **No charts generated**: Check query makes sense for data structure

## Performance Testing

```python
import time
import requests

API_BASE = "http://localhost:8000"

query = "Show me total revenue by region and product category"

start = time.time()
response = requests.post(
    f"{API_BASE}/api/dashboard/generate",
    json={"query": query, "limit": 100}
)
elapsed = time.time() - start

result = response.json()
print(f"Total time: {elapsed:.2f}s")
print(f"API reported: {result['execution_time_ms']}ms")
print(f"Generated charts: {len(result['charts'])}")
```

Expected performance:
- Simple queries: 1-3 seconds
- Complex queries: 3-8 seconds
- Very complex queries: 8-15 seconds
