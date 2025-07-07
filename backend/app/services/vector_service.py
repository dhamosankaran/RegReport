import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy import text, bindparam
import numpy as np

from openai import OpenAI

from .document_processor import DocumentProcessor, DocumentChunk
from ..models.schemas import DocumentStatus, DocumentsStatus
from ..models.database import create_session_factory, DocumentChunk as DBDocumentChunk, init_database
from ..utils.logging_config import get_logger

logger = get_logger("vector_service")

class PostgreSQLVectorService:
    def __init__(self, 
                 embedding_model: str = "text-embedding-3-small"):
        
        self.embedding_model = embedding_model
        
        # Initialize database
        self.SessionLocal, self.engine = create_session_factory()
        
        # Initialize document processor
        self.document_processor = DocumentProcessor()
        
        # Initialize OpenAI client for embeddings
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.openai_client = OpenAI(api_key=api_key)
        
        # Track document processing status
        self.document_status = {}
    
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
            init_database()
            logger.info("Initialized PostgreSQL database with pgvector extension")
            logger.info(f"Using OpenAI embedding model: {self.embedding_model}")
            
            # Process initial documents if they exist
            await self._process_initial_documents()
            
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL database: {str(e)}")
            raise
    
    async def _process_initial_documents(self):
        """Process initial PDF documents if they exist and are new/changed"""
        # Get the project root directory (4 levels up from vector_service.py)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        pdf_files = [
            os.path.join(project_root, "Instructions.pdf"),
            os.path.join(project_root, "Rules.pdf")
        ]
        existing_files = []
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                existing_files.append(pdf_file)
        if existing_files:
            logger.info(f"Checking initial documents for changes: {existing_files}")
            await self._add_documents_if_changed(existing_files)

    async def _add_documents_if_changed(self, file_paths: List[str]) -> None:
        """Add documents only if new or changed (by file hash)"""
        for file_path in file_paths:
            file_hash = self._get_file_hash(file_path)
            doc_name = os.path.basename(file_path)
            
            # Check if any chunk for this document and hash exists
            with self.SessionLocal() as db:
                existing = db.query(DBDocumentChunk).filter(
                    DBDocumentChunk.document_name == doc_name,
                    DBDocumentChunk.file_hash == file_hash
                ).first()
                
                if existing:
                    logger.info(f"Skipping {file_path}: already vectorized with hash {file_hash}")
                    self.document_status[file_path] = {
                        "status": "loaded",
                        "last_updated": datetime.now(),
                        "chunk_count": db.query(DBDocumentChunk).filter(
                            DBDocumentChunk.document_name == doc_name
                        ).count()
                    }
                    continue
                
            logger.info(f"Processing {file_path}: new or changed (hash {file_hash})")
            await self.add_documents([file_path], file_hash=file_hash)

    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI API"""
        try:
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Error generating OpenAI embeddings: {str(e)}")
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
                    chunks = await self.document_processor.process_pdf(file_path)
                    logger.debug(f"[DEBUG] Created {len(chunks)} chunks for {file_path}")
                    for chunk in chunks:
                        logger.debug(f"[DEBUG] Chunk metadata: {chunk.metadata}")
                    
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
                    
                    logger.info(f"Added {len(chunks)} chunks from {file_path} using OpenAI embeddings")
                    
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
            # Generate embedding for the query
            query_embedding = await self._generate_embeddings([query])
            query_vector = query_embedding[0]
            # Pass query_vector as a plain list; use CAST in SQL
            
            with self.SessionLocal() as db:
                # Build the similarity search query using named parameters and CAST
                sql_query = """
                SELECT 
                    content,
                    chunk_metadata,
                    chunk_type,
                    document_name,
                    page_number,
                    1 - (embedding <=> CAST(:query_vector AS vector)) as similarity_score
                FROM document_chunks
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
                
                # Execute the query with named parameters
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
                logger.debug(f"[DEBUG] search_similar_documents returned {len(formatted_results)} results for query '{query}'")
                for doc in formatted_results:
                    logger.debug(f"[DEBUG] Retrieved doc: {doc}")
                return formatted_results
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise
    
    async def get_document_status(self) -> DocumentsStatus:
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
                    
                    # Get latest file hash for this document
                    latest_chunk = db.query(DBDocumentChunk).filter(
                        DBDocumentChunk.document_name == doc_name
                    ).order_by(DBDocumentChunk.updated_at.desc()).first()
                    
                    documents.append(DocumentStatus(
                        document_name=doc_name,
                        status="loaded" if chunk_count > 0 else "not_loaded",
                        chunk_count=chunk_count,
                        last_updated=latest_chunk.updated_at if latest_chunk else datetime.now()
                    ))
                
                return DocumentsStatus(
                    total_documents=total_documents,
                    total_chunks=total_chunks,
                    documents=documents,
                    last_refresh=datetime.now()
                )
                
        except Exception as e:
            logger.error(f"Error getting document status: {str(e)}")
            raise
    
    async def reload_documents(self):
        """Reload all documents into the vector database"""
        try:
            # Clear existing data
            with self.SessionLocal() as db:
                db.query(DBDocumentChunk).delete()
                db.commit()
            
            # Reset document status
            self.document_status = {}
            
            # Process documents
            # Get the project root directory (4 levels up from vector_service.py)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            pdf_files = [
                os.path.join(project_root, "Instructions.pdf"),
                os.path.join(project_root, "Rules.pdf")
            ]
            
            existing_files = []
            for pdf_file in pdf_files:
                if os.path.exists(pdf_file):
                    existing_files.append(pdf_file)
            
            if existing_files:
                await self.add_documents(existing_files)
                logger.info("Documents reloaded successfully")
            else:
                logger.warning("No PDF files found to reload")
                
        except Exception as e:
            logger.error(f"Error reloading documents: {str(e)}")
            raise
    
    async def hybrid_search(self, 
                          query: str, 
                          n_results: int = 20,
                          include_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Perform hybrid search combining semantic similarity with metadata filtering"""
        try:
            # Build metadata filter
            filter_metadata = {}
            if include_types:
                # For hybrid search, we'll search across all types but prioritize specified ones
                pass
            
            # Perform semantic search
            results = await self.search_similar_documents(query, n_results, filter_metadata)
            
            # If we have type filters, we can re-rank results here
            if include_types:
                # Prioritize results from specified types
                prioritized_results = []
                other_results = []
                
                for result in results:
                    if result["chunk_type"] in include_types:
                        prioritized_results.append(result)
                    else:
                        other_results.append(result)
                
                # Combine prioritized results first, then others
                results = prioritized_results + other_results
                results = results[:n_results]
            
            logger.debug(f"[DEBUG] hybrid_search returning {len(results)} results for query '{query}'")
            for doc in results:
                logger.debug(f"[DEBUG] Hybrid search doc: {doc}")
            return results
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {str(e)}")
            raise
    
    async def debug_top_chunks(self, query: str, n_results: int = 10) -> list:
        """Return the top N chunks for a query, including content and metadata, for debugging retrieval."""
        results = await self.search_similar_documents(query, n_results=n_results)
        debug_info = []
        for i, doc in enumerate(results):
            debug_info.append({
                "rank": i+1,
                "similarity_score": doc.get("similarity_score"),
                "document_name": doc.get("metadata", {}).get("document_name", doc.get("document_name", "Unknown")),
                "page_number": doc.get("metadata", {}).get("page_number", doc.get("page_number", "Unknown")),
                "chunk_type": doc.get("metadata", {}).get("chunk_type", doc.get("chunk_type", "Unknown")),
                "content": doc.get("content", "")[:300] + ("..." if len(doc.get("content", "")) > 300 else "")
            })
        return debug_info
    
    async def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with self.SessionLocal() as db:
                total_chunks = db.query(DBDocumentChunk).count()
                total_documents = db.query(DBDocumentChunk.document_name).distinct().count()
                
                # Get chunk type distribution
                chunk_types = db.query(DBDocumentChunk.chunk_type).distinct()
                type_distribution = {}
                for chunk_type in chunk_types:
                    count = db.query(DBDocumentChunk).filter(
                        DBDocumentChunk.chunk_type == chunk_type[0]
                    ).count()
                    type_distribution[chunk_type[0]] = count
                
                return {
                    "total_chunks": total_chunks,
                    "total_documents": total_documents,
                    "chunk_type_distribution": type_distribution,
                    "database_type": "PostgreSQL with pgvector"
                }
                
        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {"error": str(e)}

# Alias for backward compatibility
VectorService = PostgreSQLVectorService 