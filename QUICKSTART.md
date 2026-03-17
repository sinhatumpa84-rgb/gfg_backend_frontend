# Quick Start Guide

Get up and running with the BI Dashboard Backend API in 5 minutes.

## Prerequisites

- Python 3.9+
- Google Gemini API key (free from [https://ai.google.dev](https://ai.google.dev))

## Installation & Setup

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here_AIzaSy...
```

### Step 3: Run the Server

```bash
python main.py
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 4: Check it's Working

Open your browser to:

**http://localhost:8000/docs**

You'll see the interactive API documentation (Swagger UI).

## First Query

### Using Swagger UI (Easiest)

1. Go to http://localhost:8000/docs
2. Click on `POST /api/dashboard/generate`
3. Click "Try it out"
4. In the Request body, enter:

```json
{
  "query": "Show me total revenue by region",
  "limit": 100
}
```

5. Click "Execute"
6. See your results!

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/dashboard/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me total revenue by region",
    "limit": 100
  }'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/dashboard/generate",
    json={
        "query": "Show me total revenue by region",
        "limit": 100
    }
)

result = response.json()
print(f"Generated {len(result['charts'])} charts")
print(f"Summary: {result['summary']}")
```

## Example Queries to Try

1. **Basic**: "Show me total revenue by region"
2. **Time Series**: "Display monthly sales trend"
3. **Category**: "What are the top selling products"
4. **Comparative**: "Compare performance across regions"
5. **Filtered**: "Show me electronics sales in the East region"

## Common Issues

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "GEMINI_API_KEY not found" | Create `.env` file with your API key |
| "Connection refused" | Make sure server is running (`python main.py`) |
| "No results" | Try simpler query like "show me all sales" |

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [EXAMPLES.md](EXAMPLES.md) for more query examples
- Explore API endpoints in Swagger UI
- Set up PostgreSQL for production (see README)
- Deploy with Docker (see below)

## Docker Deployment

```bash
# Build and run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Stop
docker-compose down
```

## Testing

```bash
# Run tests
pytest test_api.py -v

# With coverage
pytest test_api.py --cov
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app & routes
├── config.py              # Configuration
├── models.py              # Data models
├── llm_service.py         # LLM integration
├── database_service.py    # Database operations
├── data_processing_service.py  # Data transformation
├── dashboard_service.py   # Main orchestration
├── utils.py               # Utilities
├── requirements.txt       # Dependencies
├── .env                   # Configuration (create from .env.example)
├── bi_dashboard.db        # SQLite database (auto-created)
└── README.md              # Full documentation
```

## Key Features

✅ Natural language queries → SQL  
✅ Automatic chart recommendations  
✅ Business insights generation  
✅ Follow-up questions support  
✅ Multiple database support  
✅ Fast execution  
✅ Easy deployment  

## Support

- Full API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- See README.md for troubleshooting
- Check EXAMPLES.md for query patterns

---

**That's it!** You're ready to build intelligent dashboards with natural language. 🚀
