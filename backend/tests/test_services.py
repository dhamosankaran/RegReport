"""
Service layer tests for RegReportRAG backend
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List

from app.services.rag_service import RAGService
from app.services.vector_service import PostgreSQLVectorService
from app.models.schemas import ComplianceQuery, ComplianceResponse

class TestRAGService:
    """Test RAG service functionality."""
    
    @pytest.fixture
    def mock_vector_service(self):
        """Create mock vector service."""
        mock_service = AsyncMock(spec=PostgreSQLVectorService)
        return mock_service
    
    @pytest.fixture
    def rag_service(self, mock_vector_service):
        """Create RAG service with mocked dependencies."""
        return RAGService(mock_vector_service)
    
    @pytest.mark.asyncio
    async def test_check_compliance_success(self, rag_service, mock_vector_service):
        """Test successful compliance check."""
        # Mock vector search results
        mock_search_results = [
            {
                "content": "Data privacy requirements mandate encryption",
                "metadata": {"source": "Instructions.pdf", "section": "2.1"},
                "score": 0.95
            },
            {
                "content": "Access controls must be implemented",
                "metadata": {"source": "Rules.pdf", "section": "1.3"},
                "score": 0.88
            }
        ]
        mock_vector_service.search_similar_chunks.return_value = mock_search_results
        
        # Mock OpenAI response
        with patch('app.services.rag_service.openai.ChatCompletion.create') as mock_openai:
            mock_openai.return_value = MagicMock(
                choices=[MagicMock(
                    message=MagicMock(
                        content='{"status": "compliant", "confidence": 0.85, "explanation": "Test explanation", "relevant_sections": ["2.1", "1.3"], "recommendations": ["Implement encryption", "Set up access controls"]}'
                    )
                )]
            )
            
            query = ComplianceQuery(
                concern="Data privacy compliance for customer information",
                context="Processing customer data for financial services"
            )
            
            result = await rag_service.check_compliance(query.concern, query.context)
            
            assert isinstance(result, ComplianceResponse)
            assert result.status == "compliant"
            assert result.confidence == 0.85
            assert "explanation" in result.explanation
            assert len(result.relevant_sections) > 0
            assert len(result.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_check_compliance_no_relevant_chunks(self, rag_service, mock_vector_service):
        """Test compliance check when no relevant chunks found."""
        # Mock empty search results
        mock_vector_service.search_similar_chunks.return_value = []
        
        query = ComplianceQuery(
            concern="Unrelated topic",
            context="No relevant context"
        )
        
        result = await rag_service.check_compliance(query.concern, query.context)
        
        assert isinstance(result, ComplianceResponse)
        assert result.status == "unknown"
        assert result.confidence < 0.5
    
    @pytest.mark.asyncio
    async def test_check_compliance_openai_error(self, rag_service, mock_vector_service):
        """Test compliance check when OpenAI API fails."""
        # Mock search results
        mock_search_results = [
            {
                "content": "Test content",
                "metadata": {"source": "Instructions.pdf"},
                "score": 0.8
            }
        ]
        mock_vector_service.search_similar_chunks.return_value = mock_search_results
        
        # Mock OpenAI error
        with patch('app.services.rag_service.openai.ChatCompletion.create') as mock_openai:
            mock_openai.side_effect = Exception("OpenAI API error")
            
            query = ComplianceQuery(
                concern="Test concern",
                context="Test context"
            )
            
            with pytest.raises(Exception):
                await rag_service.check_compliance(query.concern, query.context)
    
    @pytest.mark.asyncio
    async def test_check_compliance_invalid_openai_response(self, rag_service, mock_vector_service):
        """Test compliance check with invalid OpenAI response."""
        # Mock search results
        mock_search_results = [
            {
                "content": "Test content",
                "metadata": {"source": "Instructions.pdf"},
                "score": 0.8
            }
        ]
        mock_vector_service.search_similar_chunks.return_value = mock_search_results
        
        # Mock invalid OpenAI response
        with patch('app.services.rag_service.openai.ChatCompletion.create') as mock_openai:
            mock_openai.return_value = MagicMock(
                choices=[MagicMock(
                    message=MagicMock(
                        content="Invalid JSON response"
                    )
                )]
            )
            
            query = ComplianceQuery(
                concern="Test concern",
                context="Test context"
            )
            
            result = await rag_service.check_compliance(query.concern, query.context)
            
            # Should handle invalid response gracefully
            assert isinstance(result, ComplianceResponse)
            assert result.status == "unknown"
    
    @pytest.mark.asyncio
    async def test_check_compliance_different_scenarios(self, rag_service, mock_vector_service):
        """Test compliance check with different scenarios."""
        test_cases = [
            {
                "concern": "Data encryption requirements",
                "expected_status": "compliant"
            },
            {
                "concern": "Audit trail maintenance",
                "expected_status": "compliant"
            },
            {
                "concern": "Unrelated topic",
                "expected_status": "unknown"
            }
        ]
        
        for test_case in test_cases:
            # Mock search results based on scenario
            if "unrelated" in test_case["concern"].lower():
                mock_search_results = []
            else:
                mock_search_results = [
                    {
                        "content": f"Relevant content for {test_case['concern']}",
                        "metadata": {"source": "Instructions.pdf"},
                        "score": 0.9
                    }
                ]
            
            mock_vector_service.search_similar_chunks.return_value = mock_search_results
            
            # Mock OpenAI response
            with patch('app.services.rag_service.openai.ChatCompletion.create') as mock_openai:
                mock_openai.return_value = MagicMock(
                    choices=[MagicMock(
                        message=MagicMock(
                            content=f'{{"status": "{test_case["expected_status"]}", "confidence": 0.85, "explanation": "Test", "relevant_sections": ["1.1"], "recommendations": ["Test"]}}'
                        )
                    )]
                )
                
                result = await rag_service.check_compliance(
                    test_case["concern"], 
                    "Test context"
                )
                
                assert isinstance(result, ComplianceResponse)
                assert result.status == test_case["expected_status"]

class TestVectorService:
    """Test vector service functionality."""
    
    @pytest.fixture
    def mock_chroma_client(self):
        """Create mock ChromaDB client."""
        mock_client = MagicMock()
        mock_collection = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection
        return mock_client, mock_collection
    
    @pytest.mark.asyncio
    async def test_initialize_database(self, mock_chroma_client):
        """Test database initialization."""
        mock_client, mock_collection = mock_chroma_client
        
        with patch('app.services.vector_service.chromadb.PersistentClient', return_value=mock_client):
            service = PostgreSQLVectorService()
            await service.initialize_database()
            
            mock_client.get_or_create_collection.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_similar_chunks(self, mock_chroma_client):
        """Test searching for similar chunks."""
        mock_client, mock_collection = mock_chroma_client
        
        # Mock search results
        mock_results = {
            "documents": [["Test document content"]],
            "metadatas": [[{"source": "Instructions.pdf", "section": "1.1"}]],
            "distances": [[0.1]]
        }
        mock_collection.query.return_value = mock_results
        
        with patch('app.services.vector_service.chromadb.PersistentClient', return_value=mock_client):
            service = PostgreSQLVectorService()
            
            results = await service.search_similar_chunks("test query", limit=5)
            
            assert len(results) > 0
            assert "content" in results[0]
            assert "metadata" in results[0]
            assert "score" in results[0]
    
    @pytest.mark.asyncio
    async def test_get_document_status(self, mock_chroma_client):
        """Test getting document status."""
        mock_client, mock_collection = mock_chroma_client
        
        # Mock collection count
        mock_collection.count.return_value = 150
        
        # Mock get results
        mock_get_results = {
            "metadatas": [
                [{"source": "Instructions.pdf", "section": "1.1"}],
                [{"source": "Rules.pdf", "section": "2.1"}]
            ]
        }
        mock_collection.get.return_value = mock_get_results
        
        with patch('app.services.vector_service.chromadb.PersistentClient', return_value=mock_client):
            service = PostgreSQLVectorService()
            
            status = await service.get_document_status()
            
            assert status.total_documents == 2
            assert status.total_chunks == 150
            assert len(status.documents) == 2
    
    @pytest.mark.asyncio
    async def test_reload_documents(self, mock_chroma_client):
        """Test document reload functionality."""
        mock_client, mock_collection = mock_chroma_client
        
        with patch('app.services.vector_service.chromadb.PersistentClient', return_value=mock_client):
            with patch('app.services.vector_service.PostgreSQLVectorService._load_documents') as mock_load:
                service = PostgreSQLVectorService()
                
                await service.reload_documents()
                
                mock_load.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_close_connection(self, mock_chroma_client):
        """Test closing database connection."""
        mock_client, mock_collection = mock_chroma_client
        
        with patch('app.services.vector_service.chromadb.PersistentClient', return_value=mock_client):
            service = PostgreSQLVectorService()
            
            await service.close()
            
            # Should handle cleanup gracefully
            assert True  # No exception should be raised

class TestServiceIntegration:
    """Test integration between services."""
    
    @pytest.mark.asyncio
    async def test_rag_vector_integration(self):
        """Test integration between RAG and vector services."""
        # Create real vector service with mocked ChromaDB
        with patch('app.services.vector_service.chromadb.PersistentClient') as mock_chroma:
            mock_client = MagicMock()
            mock_collection = MagicMock()
            mock_client.get_or_create_collection.return_value = mock_collection
            mock_chroma.return_value = mock_client
            
            # Mock search results
            mock_results = {
                "documents": [["Test regulatory content"]],
                "metadatas": [[{"source": "Instructions.pdf", "section": "1.1"}]],
                "distances": [[0.1]]
            }
            mock_collection.query.return_value = mock_results
            mock_collection.count.return_value = 100
            
            vector_service = PostgreSQLVectorService()
            rag_service = RAGService(vector_service)
            
            # Test the integration
            await vector_service.initialize_database()
            
            # Mock OpenAI for RAG service
            with patch('app.services.rag_service.openai.ChatCompletion.create') as mock_openai:
                mock_openai.return_value = MagicMock(
                    choices=[MagicMock(
                        message=MagicMock(
                            content='{"status": "compliant", "confidence": 0.85, "explanation": "Test", "relevant_sections": ["1.1"], "recommendations": ["Test"]}'
                        )
                    )]
                )
                
                result = await rag_service.check_compliance(
                    "Data privacy compliance",
                    "Customer data processing"
                )
                
                assert isinstance(result, ComplianceResponse)
                assert result.status == "compliant"
            
            await vector_service.close()

class TestErrorHandling:
    """Test error handling in services."""
    
    @pytest.mark.asyncio
    async def test_vector_service_connection_error(self):
        """Test vector service connection error handling."""
        with patch('app.services.vector_service.chromadb.PersistentClient') as mock_chroma:
            mock_chroma.side_effect = Exception("Connection failed")
            
            service = PostgreSQLVectorService()
            
            with pytest.raises(Exception):
                await service.initialize_database()
    
    @pytest.mark.asyncio
    async def test_rag_service_vector_error(self, mock_vector_service):
        """Test RAG service handling vector service errors."""
        mock_vector_service.search_similar_chunks.side_effect = Exception("Vector search failed")
        
        rag_service = RAGService(mock_vector_service)
        
        with pytest.raises(Exception):
            await rag_service.check_compliance("test", "test")
    
    @pytest.mark.asyncio
    async def test_service_graceful_degradation(self, mock_vector_service):
        """Test service graceful degradation."""
        # Mock partial failure
        mock_vector_service.search_similar_chunks.return_value = []
        
        rag_service = RAGService(mock_vector_service)
        
        # Should handle empty results gracefully
        result = await rag_service.check_compliance("unrelated topic", "context")
        
        assert isinstance(result, ComplianceResponse)
        assert result.status == "unknown" 