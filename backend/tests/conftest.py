"""
Pytest configuration and fixtures for RegReportRAG backend testing
"""
import pytest
import asyncio
import os
import tempfile
import shutil
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import httpx
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add backend to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.services.vector_service import PostgreSQLVectorService
from app.services.rag_service import RAGService
from app.models.schemas import ComplianceQuery, ComplianceResponse

# Test configuration
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_db_engine():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()

@pytest.fixture(scope="session")
def test_db_session(test_db_engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_db_engine
    )
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
async def mock_vector_service():
    """Mock vector service for testing."""
    mock_service = AsyncMock(spec=PostgreSQLVectorService)
    
    # Mock document status
    mock_status = MagicMock()
    mock_status.total_documents = 2
    mock_status.total_chunks = 150
    mock_status.documents = [
        {"name": "Instructions.pdf", "chunks": 75, "status": "loaded"},
        {"name": "Rules.pdf", "chunks": 75, "status": "loaded"}
    ]
    mock_service.get_document_status.return_value = mock_status
    
    # Mock reload documents
    mock_service.reload_documents.return_value = None
    
    # Mock initialize database
    mock_service.initialize_database.return_value = None
    
    # Mock close
    mock_service.close.return_value = None
    
    return mock_service

@pytest.fixture
async def mock_rag_service(mock_vector_service):
    """Mock RAG service for testing."""
    mock_service = AsyncMock(spec=RAGService)
    
    # Mock compliance check responses
    mock_response = ComplianceResponse(
        status="compliant",
        confidence=0.85,
        explanation="Based on regulatory guidelines, this appears to be compliant.",
        relevant_sections=["Section 2.1", "Section 3.4"],
        recommendations=["Ensure proper documentation", "Maintain audit trail"]
    )
    mock_service.check_compliance.return_value = mock_response
    
    return mock_service

@pytest.fixture
def test_client(mock_vector_service, mock_rag_service):
    """Create test client with mocked services."""
    # Override the services in the app
    app.dependency_overrides = {}
    
    # Create test client
    with TestClient(app) as client:
        yield client

@pytest.fixture
def sample_compliance_query():
    """Sample compliance query for testing."""
    return ComplianceQuery(
        concern="Data privacy compliance for customer information handling",
        context="Processing customer data for financial services"
    )

@pytest.fixture
def sample_compliance_response():
    """Sample compliance response for testing."""
    return ComplianceResponse(
        status="compliant",
        confidence=0.85,
        explanation="Based on regulatory guidelines, this appears to be compliant.",
        relevant_sections=["Section 2.1", "Section 3.4"],
        recommendations=["Ensure proper documentation", "Maintain audit trail"]
    )

@pytest.fixture
def test_documents_dir():
    """Create temporary directory for test documents."""
    temp_dir = tempfile.mkdtemp()
    
    # Create sample test documents
    instructions_content = """
    REGULATORY INSTRUCTIONS
    
    Section 1: Data Privacy
    - All customer data must be encrypted at rest and in transit
    - Access controls must be implemented for sensitive information
    - Audit trails must be maintained for all data access
    
    Section 2: Compliance Requirements
    - Regular compliance audits must be conducted
    - Documentation must be maintained for all processes
    - Training must be provided to all staff members
    """
    
    rules_content = """
    REGULATORY RULES
    
    Section 1: Data Handling
    - Customer data must be processed according to GDPR requirements
    - Data retention policies must be clearly defined
    - Consent must be obtained for data processing activities
    
    Section 2: Security Measures
    - Multi-factor authentication must be implemented
    - Regular security assessments must be conducted
    - Incident response procedures must be in place
    """
    
    # Write test documents
    with open(os.path.join(temp_dir, "Instructions.pdf"), "w") as f:
        f.write(instructions_content)
    
    with open(os.path.join(temp_dir, "Rules.pdf"), "w") as f:
        f.write(rules_content)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)

@pytest.fixture
def async_client():
    """Create async HTTP client for testing."""
    return httpx.AsyncClient(app=app, base_url="http://test")

# Test data fixtures
@pytest.fixture
def compliance_test_cases():
    """Test cases for compliance checking."""
    return [
        {
            "name": "data_privacy_compliance",
            "query": ComplianceQuery(
                concern="Data privacy compliance for customer information",
                context="Processing customer data for financial services"
            ),
            "expected_status": "compliant"
        },
        {
            "name": "security_requirements",
            "query": ComplianceQuery(
                concern="Security measures for data protection",
                context="Implementing access controls and encryption"
            ),
            "expected_status": "compliant"
        },
        {
            "name": "audit_trail_requirements",
            "query": ComplianceQuery(
                concern="Audit trail maintenance requirements",
                context="Tracking data access and modifications"
            ),
            "expected_status": "compliant"
        }
    ]

@pytest.fixture
def error_test_cases():
    """Test cases for error handling."""
    return [
        {
            "name": "empty_concern",
            "query": ComplianceQuery(concern="", context="test"),
            "expected_error": "concern cannot be empty"
        },
        {
            "name": "very_long_concern",
            "query": ComplianceQuery(
                concern="x" * 10000,
                context="test"
            ),
            "expected_error": "concern too long"
        }
    ]

# Performance testing fixtures
@pytest.fixture
def load_test_data():
    """Generate load test data."""
    return [
        ComplianceQuery(
            concern=f"Test compliance concern {i}",
            context=f"Test context {i}"
        )
        for i in range(100)
    ]

# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Cleanup test data after each test."""
    yield
    # Cleanup any test data created during tests
    pass 