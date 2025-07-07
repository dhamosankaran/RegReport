from pathlib import Path
import logging

# Setup logging first
from .utils.logging_config import setup_logging, log_system_info, get_logger

# Load .env from backend directory first, then fallback to parent directory
try:
    from dotenv import load_dotenv
    # Try backend/.env first
    backend_env_path = Path(__file__).resolve().parents[1] / '.env'
    if backend_env_path.exists():
        load_dotenv(dotenv_path=backend_env_path)
        print(f"Loaded environment from: {backend_env_path}")
    else:
        # Fallback to parent directory
        parent_env_path = Path(__file__).resolve().parents[2] / '.env'
        if parent_env_path.exists():
            load_dotenv(dotenv_path=parent_env_path)
            print(f"Loaded environment from: {parent_env_path}")
        else:
            print("No .env file found in backend/ or parent directory")
except ImportError:
    print("python-dotenv not installed, skipping .env loading")

# Setup logging after environment is loaded
setup_logging(log_level="INFO", log_dir="logs")
logger = get_logger("main")
log_system_info()

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
from contextlib import asynccontextmanager

from .services.vector_service import PostgreSQLVectorService
from .services.rag_service import RAGService
from .models.schemas import ComplianceQuery, ComplianceResponse

# Global services
vector_service = None
rag_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global vector_service, rag_service
    
    logger.info("Starting application services...")
    try:
        vector_service = PostgreSQLVectorService()
        rag_service = RAGService(vector_service)
        
        # Initialize vector database on startup
        logger.info("Initializing vector database...")
        await vector_service.initialize_database()
        logger.info("Vector database initialized successfully")
        
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Failed to start application services: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application services...")
    if vector_service:
        try:
            await vector_service.close()
            logger.info("Vector service closed successfully")
        except Exception as e:
            logger.error(f"Error closing vector service: {str(e)}")
    logger.info("Application shutdown completed")

app = FastAPI(
    title="Regulatory Compliance RAG API",
    description="API for checking regulatory compliance using RAG with Instructions.pdf and Rules.pdf",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Regulatory Compliance RAG API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    status = "connected" if vector_service else "disconnected"
    logger.info(f"Vector DB status: {status}")
    return {"status": "healthy", "vector_db": status}

@app.post("/api/v1/compliance/check", response_model=ComplianceResponse)
async def check_compliance(query: ComplianceQuery):
    """
    Check regulatory compliance for provided data concerns against Instructions.pdf and Rules.pdf
    """
    logger.info(f"Compliance check requested - Concern: {query.concern[:100]}...")
    try:
        result = await rag_service.check_compliance(query.concern, query.context)
        logger.info(f"Compliance check completed successfully - Status: {result.status}")
        return result
    except Exception as e:
        logger.error(f"Compliance check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/documents/status")
async def get_document_status():
    """
    Get the status of loaded documents in the vector database
    """
    logger.info("Document status requested")
    try:
        status = await vector_service.get_document_status()
        logger.info(f"Document status retrieved - Total documents: {status.total_documents}, Total chunks: {status.total_chunks}")
        return status
    except Exception as e:
        logger.error(f"Failed to get document status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/documents/reload")
async def reload_documents():
    """
    Reload documents into the vector database
    """
    logger.info("Document reload requested")
    try:
        await vector_service.reload_documents()
        logger.info("Documents reloaded successfully")
        return {"message": "Documents reloaded successfully"}
    except Exception as e:
        logger.error(f"Failed to reload documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/debug/top-chunks")
async def debug_top_chunks(query: str = Body(...), n_results: int = Body(10)):
    """Debug endpoint to return the top N chunks for a query, including content and metadata."""
    return await vector_service.debug_top_chunks(query, n_results)

@app.post("/api/v1/debug/llm-response")
async def debug_llm_response(concern: str = Body(...), context: str = Body("")):
    """Debug endpoint to see the raw LLM response for a compliance check."""
    try:
        # Get the RAG service instance
        from .services.rag_service import RAGService
        from .services.vector_service import PostgreSQLVectorService
        
        vector_service = PostgreSQLVectorService()
        await vector_service.initialize_database()
        rag_service = RAGService(vector_service)
        
        # Retrieve documents
        retrieved_docs = await rag_service._retrieve_relevant_documents(concern, context)
        
        # Generate LLM response
        llm_response = await rag_service._generate_compliance_response(concern, context, retrieved_docs)
        
        return {
            "raw_llm_response": llm_response,
            "retrieved_docs_count": len(retrieved_docs),
            "retrieved_docs": retrieved_docs[:2]  # Show first 2 docs for debugging
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 