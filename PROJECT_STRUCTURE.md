# Project Structure & File Guide

Complete guide to all files in the BI Dashboard Backend project.

## Quick Overview

This is a complete, production-ready FastAPI backend for converting natural language queries into interactive dashboards using Google Gemini LLM and multiple database backends.

---

## Core Application Files

### `main.py` ⭐
**FastAPI Application & API Routes**
- Entry point for the backend server
- Defines all REST API endpoints
- Includes request/response handlers
- Error handling and CORS middleware
- Startup/shutdown event handlers
- ~350 lines

**Key Endpoints:**
- GET `/` - API info
- GET `/health` - Health check
- POST `/api/dashboard/generate` - Generate dashboard
- POST `/api/dashboard/{id}/follow-up` - Follow-up questions
- GET `/api/schema` - Database schema
- GET `/api/tables` - Table listing
- POST `/api/query/execute` - Raw SQL execution

---

### `config.py`
**Configuration Management**
- Load settings from environment variables
- Pydantic Settings for type validation
- Database connection strings
- API keys and credentials
- CORS configuration
- ~30 lines

**Environment Variables:**
- `GEMINI_API_KEY` - Google Gemini API key
- `DATABASE_TYPE` - sqlite, postgresql
- `DATABASE_URL` - Connection string
- `DEBUG` - Debug mode toggle
- `HOST`, `PORT` - Server configuration

---

### `models.py`
**Pydantic Data Models**
- Request/response models for all endpoints
- Type validation and documentation
- Enum definitions (ChartType, etc.)
- ~100 lines

**Key Models:**
- `DashboardQueryRequest` - Client query input
- `DashboardResponse` - Complete dashboard output
- `ChartConfig` - Individual chart configuration
- `ChatMessage` - Follow-up question format
- `DataSourceInfo` - Table metadata
- `DatabaseSchema` - Full database structure

---

## Service Layer

### `dashboard_service.py` 🎯
**Main Orchestration Service**
- Coordinates all other services
- Generates complete dashboards from queries
- Manages dashboard caching
- Handles follow-up interactions
- Brain of the system
- ~250 lines

**Key Methods:**
- `generate_dashboard()` - Main workflow
- `handle_follow_up()` - Process refinements
- `_build_chart()` - Create chart configs
- `_build_modified_dashboard()` - Update after filters

---

### `llm_service.py`
**Google Gemini LLM Integration**
- Parse natural language to SQL
- Recommend chart types
- Generate business insights
- Process follow-up questions
- ~200 lines

**Key Methods:**
- `parse_natural_language_query()` - NL to SQL
- `recommend_chart_types()` - Visualization picking
- `generate_insights()` - Business analysis
- `generate_follow_up_response()` - Follow-up processing

---

### `database_service.py`
**Database Operations Layer**
- Support for SQLite, PostgreSQL, CSV
- Schema introspection
- Query execution
- Sample data initialization
- Connection management
- ~250 lines

**Key Classes:**
- `DatabaseService` - Main database operations
- `CSVService` - CSV file handling

---

### `data_processing_service.py`
**Data Transformation & Aggregation**
- Data filtering, sorting, limiting
- Aggregation (sum, avg, count, etc.)
- Chart-specific data preparation
- Statistical analysis
- ~200 lines

**Key Methods:**
- `aggregate_data()` - Group and aggregate
- `process_for_chart()` - Format for visualization
- `filter_data()` - Apply filters
- `get_data_statistics()` - Calculate stats

---

### `utils.py`
**Utility Functions & Helpers**
- SQL query builder
- Data validators
- Error formatting
- Simple cache manager
- ~150 lines

**Key Classes:**
- `QueryBuilder` - Dynamic SQL generation
- `DataValidator` - Input & config validation
- `CacheManager` - Simple in-memory cache
- `ErrorFormatter` - Error response formatting

---

## Testing & Management

### `test_api.py`
**Test Suite**
- Unit tests for all endpoints
- Model validation tests
- Query execution tests
- Error handling tests
- ~200 lines

**Test Classes:**
- `TestHealth` - Health check endpoints
- `TestSchema` - Schema endpoints
- `TestDashboardGeneration` - Dashboard creation
- `TestQuery` - Query execution
- `TestModels` - Data model validation
- `TestUtils` - Utility functions

**Run Tests:**
```bash
pytest test_api.py -v
```

---

### `manage.py`
**Database Management CLI**
- Manage database operations
- Initialize, reset, backup database
- Show schema and sample data
- Execute custom queries
- Test connections
- ~150 lines

**Commands:**
```bash
python manage.py init       # Initialize with sample data
python manage.py reset      # Delete all data
python manage.py list       # List tables
python manage.py schema     # Show schema
python manage.py sample     # Show sample data
python manage.py test       # Test connection
python manage.py query "SELECT ..." # Execute query
```

---

## Documentation Files

### `README.md`
**Main Documentation**
- Complete project overview
- Setup instructions
- Configuration guide
- API endpoint documentation
- Usage examples (cURL, Python)
- Troubleshooting guide
- Project structure
- Performance optimization tips
- Security considerations
- ~500 lines

**Sections:**
- Overview & features
- Architecture diagram
- Installation steps
- Configuration details
- Complete API reference
- Python client examples
- Database setup
- Production deployment
- Troubleshooting
- Performance tips

---

### `QUICKSTART.md`
**5-Minute Quick Start**
- Fast setup instructions
- First query examples
- Common issues table
- Docker quick start
- ~100 lines

**For:** New users who need to get running fast

---

### `API_REFERENCE.md`
**Complete API Documentation**
- All endpoints with examples
- Request/response formats
- Data models
- Status codes
- Error codes
- Best practices
- Rate limiting (future)
- ~400 lines

**For:** Frontend developers integrating with API

---

### `EXAMPLES.md`
**Example Queries**
- 10 progressive complexity examples
- Query patterns
- cURL, Python, Postman examples
- Expected results
- Testing checklist
- Common pitfalls
- Performance testing
- ~200 lines

**For:** Testing and understanding capabilities

---

### `DEPLOYMENT.md`
**Deployment Guide**
- Local development setup
- Docker deployment
- Kubernetes deployment
- Cloud platform guides (AWS, GCP, Heroku)
- Production checklist
- Monitoring and maintenance
- Scaling strategies
- Migration procedures
- Troubleshooting
- ~400 lines

**For:** DevOps and deployment engineers

---

## Configuration & Environment

### `.env`
**Environment Variables** (Git ignored)
```
GEMINI_API_KEY=your_api_key_here
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///./bi_dashboard.db
DEBUG=True
HOST=0.0.0.0
PORT=8000
CSV_DATA_PATH=./data/
```

**⚠️ IMPORTANT:** Never commit `.env` file with real credentials

---

### `.env.example`
**Example Environment File**
Template for creating `.env` file with all available options and documentation.

---

### `.gitignore`
**Git Ignore Rules**
Ignores:
- `.env` files (sensitive credentials)
- `__pycache__` directories
- Virtual environments (`venv/`, `ENV/`)
- IDE files (`.vscode/`, `.idea/`)
- Database files (`*.db`, `*.sqlite`)
- Python cache and dist files
- Test coverage files
- `.DS_Store` and OS files

---

## Dependency & Build Files

### `requirements.txt`
**Production Dependencies**
```
fastapi==0.104.1
uvicorn==0.24.0
google-generativeai==0.3.0
sqlalchemy==2.0.23
pandas==2.1.3
```

**Install:** `pip install -r requirements.txt`

---

### `requirements-dev.txt`
**Development Dependencies**
- Testing: pytest, pytest-cov
- Code quality: black, flake8, pylint, mypy
- Documentation: sphinx
- Development: ipython, jupyterlab

**Install:** `pip install -r requirements-dev.txt`

---

## Docker & Deployment

### `Dockerfile`
**Docker Image Definition**
- Base image: Python 3.11 slim
- Installs system dependencies
- Installs Python packages
- Exposes port 8000
- Health check configured
- Runs Uvicorn server

**Build:** `docker build -t bi-dashboard-backend:latest .`

---

### `docker-compose.yml`
**Multi-Container Orchestration**
- Backend service (FastAPI)
- PostgreSQL database service
- Networks and volumes
- Environment configuration
- Health checks
- Auto-restart policies

**Run:** `docker-compose up -d`

---

### `db_init.sql`
**PostgreSQL Initialization Script**
- Creates tables: sales, employees
- Inserts sample data
- Creates indexes for performance
- Sets up user permissions

**Used by:** Docker Compose on first startup

---

## API Testing

### `requests.http`
**HTTP Request Examples**
REST Client format with examples for:
- All endpoints
- Various query types
- Filter combinations
- Follow-up interactions

**Use with:** VS Code REST Client extension

---

## File Organization Summary

```
backend/
├── Core Application
│   ├── main.py                      # FastAPI app & routes
│   ├── config.py                    # Configuration
│   ├── models.py                    # Data models
│   └── utils.py                     # Utilities
│
├── Services (Business Logic)
│   ├── dashboard_service.py         # Main orchestration
│   ├── llm_service.py               # LLM integration
│   ├── database_service.py          # Database operations
│   └── data_processing_service.py   # Data transformation
│
├── Testing & Management
│   ├── test_api.py                  # Test suite
│   └── manage.py                    # CLI management
│
├── Documentation
│   ├── README.md                    # Main docs
│   ├── QUICKSTART.md                # Quick start
│   ├── API_REFERENCE.md             # API docs
│   ├── EXAMPLES.md                  # Example queries
│   └── DEPLOYMENT.md                # Deployment guide
│
├── Configuration
│   ├── .env                         # Environment vars (git ignored)
│   ├── .env.example                 # Example env file
│   └── .gitignore                   # Git ignore rules
│
├── Dependencies
│   ├── requirements.txt             # Production deps
│   └── requirements-dev.txt         # Dev dependencies
│
├── Docker & Deployment
│   ├── Dockerfile                   # Docker image
│   ├── docker-compose.yml           # Multi-container setup
│   └── db_init.sql                  # DB initialization
│
└── Testing
    ├── requests.http                # HTTP examples
    └── test_api.py                  # Test suite
```

---

## Component Dependencies

```
main.py (API Layer)
    ↓
dashboard_service.py (Orchestration)
    ├→ llm_service.py (NL Processing)
    ├→ database_service.py (DB Operations)
    └→ data_processing_service.py (Data Transform)
         └→ utils.py (Utilities)

models.py (Data Models)
    Used by: main.py, all services

config.py (Configuration)
    Used by: All modules

utils.py (Utilities)
    Used by: All services
```

---

## Data Flow

```
1. User Query (main.py)
    ↓
2. Create DashboardQueryRequest
    ↓
3. dashboard_service.generate_dashboard()
    ├─ Get database schema
    ├─ llm_service.parse_query()
    ├─ database_service.execute_query()
    ├─ data_processing_service.process_data()
    ├─ llm_service.recommend_charts()
    ├─ Build ChartConfig objects
    ├─ llm_service.generate_insights()
    │
4. Return DashboardResponse
    ↓
5. Cache dashboard
    ↓
6. Send to client
    ├─ Charts
    ├─ Insights
    ├─ Raw data
    └─ Summary
```

---

## Database Schema

### Tables

**sales**
- id, date, region, product_category, product_name, revenue, quantity, salesperson

**employees**
- id, name, department, salary, hire_date

### Indexes (PostgreSQL)
- idx_sales_region
- idx_sales_date
- idx_sales_product_category
- idx_sales_salesperson

---

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | API info |
| GET | /health | Health check |
| GET | /api/schema | Full DB schema |
| GET | /api/tables | List tables |
| GET | /api/tables/{name} | Table info |
| GET | /api/analytics/sample | Sample data |
| GET | /api/analytics/columns/{table} | Column info |
| POST | /api/dashboard/generate | Create dashboard |
| GET | /api/dashboard/{id} | Get cached dashboard |
| POST | /api/dashboard/{id}/follow-up | Ask question |
| POST | /api/query/execute | Execute SQL |

---

## Key Statistics

- **Total Lines of Code:** ~2,500
- **Python Modules:** 7 (main services)
- **API Endpoints:** 12
- **Supported Chart Types:** 8
- **Documentation Pages:** 5

---

## Getting Started

1. **Read:** [QUICKSTART.md](QUICKSTART.md) for immediate setup
2. **Explore:** [README.md](README.md) for complete documentation
3. **Learn:** [API_REFERENCE.md](API_REFERENCE.md) for integration
4. **Test:** [EXAMPLES.md](EXAMPLES.md) for query examples
5. **Deploy:** [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

---

## Maintenance & Support

- **Update Dependencies:** `pip install --upgrade -r requirements.txt`
- **Run Tests:** `pytest test_api.py -v`
- **Database Operations:** `python manage.py [command]`
- **View API Docs:** `http://localhost:8000/docs`
- **Check Logs:** `docker-compose logs -f backend` or console output

---

**Last Updated:** March 2024
**Status:** Production Ready ✅
**Version:** 1.0.0
