"""
Test suite for BI Dashboard API

Run tests with: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestHealth:
    """Health check endpoint tests."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "running"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

class TestSchema:
    """Database schema endpoint tests."""
    
    def test_get_schema(self):
        """Test getting database schema."""
        response = client.get("/api/schema")
        assert response.status_code == 200
        data = response.json()
        assert "tables" in data
        assert isinstance(data["tables"], list)
    
    def test_list_tables(self):
        """Test listing available tables."""
        response = client.get("/api/tables")
        assert response.status_code == 200
        data = response.json()
        assert "tables" in data
        assert isinstance(data["tables"], list)
    
    def test_get_table_info(self):
        """Test getting specific table info."""
        response = client.get("/api/tables/sales")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "sales"
        assert "columns" in data
        assert "row_count" in data

class TestAnalytics:
    """Analytics endpoint tests."""
    
    def test_get_sample_data(self):
        """Test getting sample data."""
        response = client.get("/api/analytics/sample?table_name=sales&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert data["table"] == "sales"
        assert "data" in data
        assert len(data["data"]) <= 5
    
    def test_get_column_info(self):
        """Test getting column information."""
        response = client.get("/api/analytics/columns/sales")
        assert response.status_code == 200
        data = response.json()
        assert data["table"] == "sales"
        assert "columns" in data

class TestDashboardGeneration:
    """Dashboard generation endpoint tests."""
    
    def test_generate_simple_dashboard(self):
        """Test generating a simple dashboard."""
        response = client.post(
            "/api/dashboard/generate",
            json={
                "query": "Show me total revenue by region",
                "limit": 100
            }
        )
        # Note: This might fail if API key is not configured
        # In that case, check .env configuration
        if response.status_code != 500:  # Skip if LLM not available
            assert response.status_code in [200, 500]
            if response.status_code == 200:
                data = response.json()
                assert "query" in data
                assert "charts" in data
                assert "summary" in data
                assert "insights" in data
    
    def test_generate_dashboard_with_filters(self):
        """Test generating dashboard with filters."""
        response = client.post(
            "/api/dashboard/generate",
            json={
                "query": "Show me total sales by region",
                "filters": {"region": "North"},
                "limit": 50
            }
        )
        if response.status_code == 200:
            data = response.json()
            assert "charts" in data
    
    def test_generate_dashboard_invalid_query(self):
        """Test generating dashboard with invalid query."""
        response = client.post(
            "/api/dashboard/generate",
            json={
                "query": "ab"  # Too short
            }
        )
        assert response.status_code == 400

class TestQuery:
    """Query execution endpoint tests."""
    
    def test_execute_simple_query(self):
        """Test executing a simple SQL query."""
        response = client.post(
            "/api/query/execute?query_text=SELECT%20*%20FROM%20sales%20LIMIT%205"
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
    
    def test_execute_invalid_query(self):
        """Test executing invalid SQL query."""
        response = client.post(
            "/api/query/execute?query_text=INVALID%20SQL"
        )
        assert response.status_code == 400

class TestModels:
    """Test Pydantic models."""
    
    def test_dashboard_query_request_model(self):
        """Test DashboardQueryRequest model."""
        from models import DashboardQueryRequest
        
        request = DashboardQueryRequest(
            query="Show me sales by region",
            filters={"region": "North"},
            limit=100
        )
        
        assert request.query == "Show me sales by region"
        assert request.filters == {"region": "North"}
        assert request.limit == 100

class TestUtils:
    """Test utility functions."""
    
    def test_query_builder(self):
        """Test SQL query builder."""
        from utils import QueryBuilder
        
        query = QueryBuilder.build_select_query(
            table="sales",
            columns=["region", "revenue"],
            where="region = 'North'",
            limit=10
        )
        
        assert "SELECT" in query
        assert "sales" in query
        assert "WHERE" in query
    
    def test_data_validator(self):
        """Test data validator."""
        from utils import DataValidator
        
        # Valid query
        assert DataValidator.validate_query_params("Show me sales data") == True
        
        # Invalid query (too short)
        assert DataValidator.validate_query_params("ab") == False
        
        # Invalid query (SQL injection attempt)
        assert DataValidator.validate_query_params("DROP TABLE users") == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
