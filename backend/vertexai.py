import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json
import hashlib
from pathlib import Path
import sys

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from sqlalchemy import text
import numpy as np

# Vertex AI imports
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel

# Import from the existing app structure
from app.models.schemas import DocumentStatus, DocumentsStatus
from app.utils.logging_config import get_logger

# Import Gemini-specific database model
from gemini_database import create_session_factory, GeminiDocumentChunk as DBDocumentChunk, init_gemini_database

# Import the Gemini-specific document processor
from gemini_document_processor import GeminiDocumentProcessor, DocumentChunk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vertexai_vector_service.log'),
        logging.StreamHandler()
    ]
)
logger = get_logger("vertexai_vector_service")

class VertexAIVectorService:
    """
    Standalone Vector Service using Google Cloud Vertex AI for embeddings and LLM processing
    """
    
    def __init__(self, 
                 embedding_model: str = "text-embedding-004",
                 llm_model: str = "gemini-1.5-flash",
                 project_id: str = None,
                 location: str = "us-central1"):
        
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location
        
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable or project_id parameter is required")
        
        # Initialize Vertex AI
        vertexai.init(project=self.project_id, location=self.location)
        
        # Initialize the generative model for LLM tasks
        self.llm = GenerativeModel(self.llm_model)
        
        # Initialize the embedding model
        self.embedding_model_instance = TextEmbeddingModel.from_pretrained(self.embedding_model)
        
        # Initialize database
        self.SessionLocal, self.engine = create_session_factory()
        
        # Initialize Gemini-specific document processor (no tiktoken)
        self.document_processor = GeminiDocumentProcessor(
            max_chunk_size=4000,  # Characters, not tokens
            chunk_overlap=200,    # Character overlap
            min_chunk_size=100    # Minimum chunk size
        )
        
        # Track document processing status
        self.document_status = {}
        
        logger.info(f"Initialized Vertex AI Vector Service with embedding model: {embedding_model}")
        logger.info(f"Using LLM model: {llm_model}")
        logger.info(f"Project ID: {self.project_id}, Location: {self.location}")
        logger.info(f"Chunking strategy: Character-based (no tiktoken) - max_size: {self.document_processor.max_chunk_size}, overlap: {self.document_processor.chunk_overlap}")
    
    def _get_file_hash(self, file_path: str) -> str:
        """Compute MD5 hash of a file for change detection"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    async def initialize_database(self):
        """Initialize PostgreSQL database with pgvector extension"""
        try:
            # Initialize database tables and pgvector extension
            init_gemini_database()
            logger.info("Initialized PostgreSQL database with pgvector extension (Vertex AI table)")
            
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL database: {str(e)}")
            raise
    
    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Vertex AI"""
        try:
            embeddings = []
            for text in texts:
                # Generate embedding for each text using Vertex AI
                result = self.embedding_model_instance.get_embeddings([text])
                embeddings.append(result[0].values)
            
            logger.debug(f"Generated {len(embeddings)} embeddings using Vertex AI")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating Vertex AI embeddings: {str(e)}")
            raise
    
    async def generate_answer(self, query: str, context_documents: List[Dict[str, Any]]) -> str:
        """Generate answer using Vertex AI Gemini Flash LLM"""
        try:
            # Prepare context from retrieved documents
            context = "\n\n".join([
                f"Document: {doc['document_name']} (Page {doc['page_number']})\n"
                f"Content: {doc['content']}"
                for doc in context_documents
            ])
            
            # Create prompt
            prompt = f"""You are an AI assistant helping with regulatory compliance analysis. 
            
Based on the following context documents, please answer the user's question:

CONTEXT:
{context}

QUESTION: {query}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to answer the question, please indicate that clearly.

ANSWER:"""
            
            # Generate response using Vertex AI
            response = self.llm.generate_content(prompt)
            
            logger.debug(f"Generated answer for query: {query}")
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating answer with Vertex AI: {str(e)}")
            raise
    
    async def add_documents(self, file_paths: List[str], file_hash: str = None) -> Dict[str, Any]:
        """Add documents to the PostgreSQL vector database"""
        try:
            results = {"processed": [], "failed": []}
            
            for file_path in file_paths:
                try:
                    # Compute hash if not provided
                    hash_to_use = file_hash or self._get_file_hash(file_path)
                    self.document_status[file_path] = {
                        "status": "processing",
                        "last_updated": datetime.now(),
                        "chunk_count": 0
                    }
                    
                    # Process PDF
                    logger.info(f"Processing PDF: {file_path}")
                    chunks = await self.document_processor.process_pdf(file_path)
                    logger.info(f"Created {len(chunks)} chunks for {file_path}")
                    
                    if not chunks:
                        logger.warning(f"No chunks extracted from {file_path}")
                        continue
                    
                    # Generate embeddings for all chunks
                    texts = [chunk.content for chunk in chunks]
                    embeddings = await self._generate_embeddings(texts)
                    
                    # Store chunks and embeddings in database
                    with self.SessionLocal() as db:
                        for i, chunk in enumerate(chunks):
                            db_chunk = DBDocumentChunk(
                                chunk_id=chunk.chunk_id,
                                document_name=os.path.basename(file_path),
                                content=chunk.content,
                                chunk_type=chunk.metadata.get("chunk_type", "general"),
                                page_number=chunk.metadata.get("page_number", 1),
                                file_hash=hash_to_use,
                                embedding=embeddings[i],
                                chunk_metadata=json.dumps(chunk.metadata)
                            )
                            db.add(db_chunk)
                        
                        db.commit()
                    
                    self.document_status[file_path] = {
                        "status": "loaded",
                        "last_updated": datetime.now(),
                        "chunk_count": len(chunks)
                    }
                    
                    results["processed"].append({
                        "file": file_path,
                        "chunk_count": len(chunks)
                    })
                    
                    # Get chunk statistics
                    chunk_stats = self.document_processor.get_chunk_stats(chunks)
                    logger.info(f"Added {len(chunks)} chunks from {file_path} using Vertex AI embeddings")
                    logger.info(f"Chunk stats: avg_size={chunk_stats.get('average_size', 0):.0f}, min={chunk_stats.get('min_size', 0)}, max={chunk_stats.get('max_size', 0)}")
                    logger.info(f"Chunking method: {chunk_stats.get('chunking_method', 'unknown')}")
                    
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
                    self.document_status[file_path] = {
                        "status": "error",
                        "last_updated": datetime.now(),
                        "error": str(e),
                        "chunk_count": 0
                    }
                    results["failed"].append({
                        "file": file_path,
                        "error": str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    async def search_similar_documents(self, 
                                     query: str, 
                                     n_results: int = 20,
                                     filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for similar documents using cosine similarity with pgvector"""
        try:
            # Generate embedding for the query using Vertex AI
            query_embedding = self.embedding_model_instance.get_embeddings([query])
            query_vector = query_embedding[0].values
            
            with self.SessionLocal() as db:
                # Build the similarity search query
                sql_query = """
                SELECT 
                    content,
                    chunk_metadata,
                    chunk_type,
                    document_name,
                    page_number,
                    1 - (embedding <=> CAST(:query_vector AS vector)) as similarity_score
                FROM gemini_document_chunks
                """
                params = {"query_vector": query_vector}
                conditions = []
                
                # Add metadata filters if provided
                if filter_metadata:
                    for key, value in filter_metadata.items():
                        if key == "document_name":
                            conditions.append("document_name = :document_name")
                            params["document_name"] = value
                        elif key == "chunk_type":
                            conditions.append("chunk_type = :chunk_type")
                            params["chunk_type"] = value
                        elif key == "file_hash":
                            conditions.append("file_hash = :file_hash")
                            params["file_hash"] = value
                
                if conditions:
                    sql_query += " WHERE " + " AND ".join(conditions)
                
                sql_query += " ORDER BY embedding <=> CAST(:query_vector AS vector) LIMIT :n_results"
                params["n_results"] = n_results
                
                # Execute the query
                result = db.execute(text(sql_query), params)
                rows = result.fetchall()
                
                # Format results
                formatted_results = []
                for row in rows:
                    formatted_results.append({
                        "content": row[0],
                        "metadata": json.loads(row[1]) if row[1] else {},
                        "chunk_type": row[2],
                        "document_name": row[3],
                        "page_number": row[4],
                        "similarity_score": float(row[5]),
                        "distance": 1.0 - float(row[5])
                    })
                
                logger.debug(f"Found {len(formatted_results)} similar documents for query: {query}")
                return formatted_results
                
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise
    
    async def query_with_rag(self, query: str, n_results: int = 10) -> Dict[str, Any]:
        """Perform RAG query: retrieve relevant documents and generate answer"""
        try:
            # Retrieve relevant documents
            relevant_docs = await self.search_similar_documents(query, n_results)
            
            if not relevant_docs:
                return {
                    "query": query,
                    "answer": "I couldn't find any relevant documents to answer your question.",
                    "sources": [],
                    "context_used": 0
                }
            
            # Generate answer using retrieved context
            answer = await self.generate_answer(query, relevant_docs)
            
            # Format sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    "document_name": doc["document_name"],
                    "page_number": doc["page_number"],
                    "similarity_score": doc["similarity_score"],
                    "content_preview": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"]
                })
            
            return {
                "query": query,
                "answer": answer,
                "sources": sources,
                "context_used": len(relevant_docs)
            }
            
        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            raise
    
    async def get_document_status(self) -> Dict[str, Any]:
        """Get the status of loaded documents"""
        try:
            with self.SessionLocal() as db:
                # Get total counts
                total_chunks = db.query(DBDocumentChunk).count()
                total_documents = db.query(DBDocumentChunk.document_name).distinct().count()
                
                # Get document details
                documents = []
                for doc_name in db.query(DBDocumentChunk.document_name).distinct():
                    doc_name = doc_name[0]
                    chunk_count = db.query(DBDocumentChunk).filter(
                        DBDocumentChunk.document_name == doc_name
                    ).count()
                    
                    documents.append({
                        "document_name": doc_name,
                        "status": "loaded",
                        "chunk_count": chunk_count
                    })
                
                return {
                    "total_documents": total_documents,
                    "total_chunks": total_chunks,
                    "documents": documents,
                    "embedding_model": self.embedding_model,
                    "llm_model": self.llm_model,
                    "project_id": self.project_id,
                    "location": self.location
                }
                
        except Exception as e:
            logger.error(f"Error getting document status: {str(e)}")
            raise
    
    async def clear_database(self):
        """Clear all documents from the database"""
        try:
            with self.SessionLocal() as db:
                db.query(DBDocumentChunk).delete()
                db.commit()
            
            self.document_status = {}
            logger.info("Cleared all documents from database")
            
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            raise
    
    async def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()

# Standalone testing functions
async def test_vertexai_vector_service():
    """Test the Vertex AI Vector Service with sample PDF files"""
    
    print("=== Vertex AI Vector Service Test ===")
    
    # Initialize service
    service = VertexAIVectorService()
    
    try:
        # Initialize database
        await service.initialize_database()
        print("✓ Database initialized")
        
        # Find PDF files to test
        project_root = Path(__file__).parent.parent
        test_files = []
        
        # Look for common PDF files
        potential_files = [
            project_root / "Instructions.pdf",
            project_root / "Rules.pdf",
            project_root / "data" / "sample.pdf",
            project_root / "TestData" / "sample.pdf"
        ]
        
        for file_path in potential_files:
            if file_path.exists():
                test_files.append(str(file_path))
        
        if not test_files:
            print("⚠ No PDF files found for testing")
            return
        
        print(f"Found {len(test_files)} PDF files to test: {test_files}")
        
        # Add documents
        results = await service.add_documents(test_files)
        print(f"✓ Processing complete: {len(results['processed'])} processed, {len(results['failed'])} failed")
        
        # Check status
        status = await service.get_document_status()
        print(f"✓ Database status: {status['total_documents']} documents, {status['total_chunks']} chunks")
        
        # Test queries
        test_queries = [
            "What are the main compliance requirements?",
            "How should regulatory reports be structured?",
            "What are the key rules to follow?",
            "Explain the document processing requirements"
        ]
        
        print("\n=== Testing RAG Queries ===")
        for query in test_queries:
            print(f"\nQuery: {query}")
            
            # Perform RAG query
            result = await service.query_with_rag(query, n_results=5)
            
            print(f"Answer: {result['answer'][:200]}...")
            print(f"Sources used: {result['context_used']}")
            
            # Show top sources
            for i, source in enumerate(result['sources'][:3]):
                print(f"  Source {i+1}: {source['document_name']} (page {source['page_number']}) - Score: {source['similarity_score']:.3f}")
        
        print("\n=== Test Complete ===")
        
    except Exception as e:
        print(f"✗ Error during testing: {str(e)}")
        raise
    
    finally:
        await service.close()

# Main execution
if __name__ == "__main__":
    import asyncio
    
    # Check environment
    if not os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("Error: GOOGLE_CLOUD_PROJECT environment variable is required")
        print("Please set it in your .env file or environment")
        print("You can also pass it as a parameter to VertexAIVectorService()")
        sys.exit(1)
    
    # Run the test
    asyncio.run(test_vertexai_vector_service()) 
