from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Index, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector
from datetime import datetime
import os
from typing import List

Base = declarative_base()

class DocumentChunk(Base):
    """Database model for document chunks with vector embeddings"""
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String(255), unique=True, index=True, nullable=False)
    document_name = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    chunk_type = Column(String(100), index=True, nullable=False)
    page_number = Column(Integer, nullable=True)
    file_hash = Column(String(64), index=True, nullable=False)
    embedding = Column(Vector(1536), nullable=False)  # OpenAI embedding dimension
    chunk_metadata = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create indexes for better performance
Index('idx_document_chunks_document_name', DocumentChunk.document_name)
Index('idx_document_chunks_chunk_type', DocumentChunk.chunk_type)
Index('idx_document_chunks_file_hash', DocumentChunk.file_hash)

def get_database_url():
    """Get database URL from environment variables"""
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "rag_system")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

def create_database_engine():
    """Create SQLAlchemy engine with pgvector support"""
    database_url = get_database_url()
    engine = create_engine(
        database_url,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,
        pool_recycle=300
    )
    return engine

def create_session_factory():
    """Create session factory for database operations"""
    engine = create_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal, engine

def init_database():
    """Initialize database tables and pgvector extension"""
    engine = create_database_engine()
    
    # Enable pgvector extension
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    return engine 