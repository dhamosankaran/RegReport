"""
API endpoint tests for RegReportRAG backend
"""
import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.main import app
from app.models.schemas import ComplianceQuery, ComplianceResponse

class TestRootEndpoint:
    """Test root endpoint functionality."""
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint returns correct response."""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Regulatory Compliance RAG API"
        assert data["version"] == "1.0.0"

class TestHealthEndpoint:
    """Test health check endpoint functionality."""
    
    def test_health_check_success(self, test_client):
        """Test health check returns healthy status."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "vector_db" in data

class TestComplianceCheckEndpoint:
    """Test compliance check endpoint functionality."""
    
    def test_compliance_check_success(self, test_client, sample_compliance_query):
        """Test successful compliance check."""
        with patch('app.main.rag_service') as mock_rag:
            mock_rag.check_compliance.return_value = ComplianceResponse(
                status="compliant",
                confidence=0.85,
                explanation="Test explanation",
                relevant_sections=["Section 1"],
                recommendations=["Test recommendation"]
            )
            
            response = test_client.post(
                "/api/v1/compliance/check",
                json=sample_compliance_query.dict()
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "compliant"
            assert data["confidence"] == 0.85
            assert "explanation" in data
            assert "relevant_sections" in data
            assert "recommendations" in data
    
    def test_compliance_check_invalid_input(self, test_client):
        """Test compliance check with invalid input."""
        invalid_data = {
            "concern": "",  # Empty concern
            "context": "test"
        }
        
        response = test_client.post(
            "/api/v1/compliance/check",
            json=invalid_data
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_compliance_check_missing_fields(self, test_client):
        """Test compliance check with missing required fields."""
        incomplete_data = {
            "concern": "test concern"
            # Missing context field
        }
        
        response = test_client.post(
            "/api/v1/compliance/check",
            json=incomplete_data
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_compliance_check_service_error(self, test_client, sample_compliance_query):
        """Test compliance check when service throws error."""
        with patch('app.main.rag_service') as mock_rag:
            mock_rag.check_compliance.side_effect = Exception("Service error")
            
            response = test_client.post(
                "/api/v1/compliance/check",
                json=sample_compliance_query.dict()
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
    
    @pytest.mark.parametrize("test_case", [
        {
            "concern": "Data privacy compliance",
            "context": "Customer data processing",
            "expected_status": "compliant"
        },
        {
            "concern": "Security requirements",
            "context": "Access control implementation",
            "expected_status": "compliant"
        },
        {
            "concern": "Audit trail requirements",
            "context": "Data access tracking",
            "expected_status": "compliant"
        }
    ])
    def test_compliance_check_various_scenarios(self, test_client, test_case):
        """Test compliance check with various scenarios."""
        with patch('app.main.rag_service') as mock_rag:
            mock_rag.check_compliance.return_value = ComplianceResponse(
                status=test_case["expected_status"],
                confidence=0.85,
                explanation="Test explanation",
                relevant_sections=["Section 1"],
                recommendations=["Test recommendation"]
            )
            
            query_data = {
                "concern": test_case["concern"],
                "context": test_case["context"]
            }
            
            response = test_client.post(
                "/api/v1/compliance/check",
                json=query_data
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == test_case["expected_status"]

class TestDocumentStatusEndpoint:
    """Test document status endpoint functionality."""
    
    def test_document_status_success(self, test_client):
        """Test successful document status retrieval."""
        with patch('app.main.vector_service') as mock_vector:
            mock_status = {
                "total_documents": 2,
                "total_chunks": 150,
                "documents": [
                    {"name": "Instructions.pdf", "chunks": 75, "status": "loaded"},
                    {"name": "Rules.pdf", "chunks": 75, "status": "loaded"}
                ]
            }
            mock_vector.get_document_status.return_value = mock_status
            
            response = test_client.get("/api/v1/documents/status")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_documents"] == 2
            assert data["total_chunks"] == 150
            assert len(data["documents"]) == 2
    
    def test_document_status_service_error(self, test_client):
        """Test document status when service throws error."""
        with patch('app.main.vector_service') as mock_vector:
            mock_vector.get_document_status.side_effect = Exception("Service error")
            
            response = test_client.get("/api/v1/documents/status")
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data

class TestDocumentReloadEndpoint:
    """Test document reload endpoint functionality."""
    
    def test_document_reload_success(self, test_client):
        """Test successful document reload."""
        with patch('app.main.vector_service') as mock_vector:
            mock_vector.reload_documents.return_value = None
            
            response = test_client.post("/api/v1/documents/reload")
            
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Documents reloaded successfully"
    
    def test_document_reload_service_error(self, test_client):
        """Test document reload when service throws error."""
        with patch('app.main.vector_service') as mock_vector:
            mock_vector.reload_documents.side_effect = Exception("Service error")
            
            response = test_client.post("/api/v1/documents/reload")
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data

class TestErrorHandling:
    """Test error handling across endpoints."""
    
    def test_404_error(self, test_client):
        """Test 404 error for non-existent endpoint."""
        response = test_client.get("/api/v1/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, test_client):
        """Test method not allowed error."""
        response = test_client.put("/api/v1/compliance/check")
        assert response.status_code == 405
    
    def test_invalid_json(self, test_client):
        """Test invalid JSON handling."""
        response = test_client.post(
            "/api/v1/compliance/check",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

class TestCORSConfiguration:
    """Test CORS configuration."""
    
    def test_cors_headers(self, test_client):
        """Test CORS headers are present."""
        response = test_client.options("/api/v1/compliance/check")
        assert response.status_code == 200
        # CORS headers should be present (handled by FastAPI middleware)

class TestPerformance:
    """Test API performance characteristics."""
    
    def test_compliance_check_response_time(self, test_client, sample_compliance_query):
        """Test compliance check response time."""
        import time
        
        with patch('app.main.rag_service') as mock_rag:
            mock_rag.check_compliance.return_value = ComplianceResponse(
                status="compliant",
                confidence=0.85,
                explanation="Test explanation",
                relevant_sections=["Section 1"],
                recommendations=["Test recommendation"]
            )
            
            start_time = time.time()
            response = test_client.post(
                "/api/v1/compliance/check",
                json=sample_compliance_query.dict()
            )
            end_time = time.time()
            
            assert response.status_code == 200
            assert (end_time - start_time) < 5.0  # Should respond within 5 seconds
    
    def test_concurrent_requests(self, test_client, sample_compliance_query):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        errors = []
        
        def make_request():
            try:
                with patch('app.main.rag_service') as mock_rag:
                    mock_rag.check_compliance.return_value = ComplianceResponse(
                        status="compliant",
                        confidence=0.85,
                        explanation="Test explanation",
                        relevant_sections=["Section 1"],
                        recommendations=["Test recommendation"]
                    )
                    
                    response = test_client.post(
                        "/api/v1/compliance/check",
                        json=sample_compliance_query.dict()
                    )
                    results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))
        
        # Start 10 concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert len(errors) == 0
        assert len(results) == 10
        assert all(status == 200 for status in results) 