# PostgreSQL Migration Guide

> **Note:** The current system uses PostgreSQL (with pgvector) exclusively for all vector storage and retrieval. ChromaDB is no longer used in any part of the system. The following guide is retained for historical reference.

This guide covers the migration from ChromaDB to PostgreSQL with pgvector extension for the Regulatory Compliance RAG System.

## Overview

The system has been migrated from ChromaDB to PostgreSQL with pgvector to provide:
- **ACID Compliance**: Transactional integrity for data operations
- **Scalability**: Handle larger datasets and concurrent users
- **Standard SQL**: Familiar database operations and ecosystem
- **Backup/Restore**: Automated database backup capabilities
- **Monitoring**: Rich database performance metrics

## Prerequisites

### 1. PostgreSQL Installation

**Option A: Docker (Recommended)**
```bash
# Start PostgreSQL with pgvector
docker-compose up -d postgres
```

**Option B: Local Installation**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS with Homebrew
brew install postgresql

# Enable pgvector extension
# Follow pgvector installation guide: https://github.com/pgvector/pgvector
```

### 2. Python Dependencies

The requirements.txt has been updated with PostgreSQL dependencies:
```bash
pip install -r backend/requirements.txt
```

Key new dependencies:
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `pgvector==0.2.4` - Vector operations
- `sqlalchemy==2.0.41` - ORM
- `alembic==1.13.1` - Database migrations

## Database Setup

### 1. Environment Configuration

Update your `.env` file with PostgreSQL settings:
```bash
# PostgreSQL Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 2. Database Initialization

Run the database setup script:
```bash
cd backend
python setup_database.py
```

This script will:
- Connect to PostgreSQL
- Enable pgvector extension
- Create database tables
- Verify setup

### 3. Manual Database Setup (Alternative)

If you prefer manual setup:

```sql
-- Connect to PostgreSQL
psql -U postgres -d rag_system

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create tables (handled by SQLAlchemy models)
-- The setup script will create these automatically
```

## Migration Process

### 1. Data Migration (if migrating existing ChromaDB data)

If you have existing ChromaDB data to migrate:

```python
# Export from ChromaDB
from chromadb import PersistentClient
client = PersistentClient(path="data/chromadb")
collection = client.get_collection("regulatory_documents")

# Get all data
results = collection.get()
documents = results['documents']
metadatas = results['metadatas']
embeddings = results['embeddings']

# Import to PostgreSQL
from app.services.vector_service import PostgreSQLVectorService
vector_service = PostgreSQLVectorService()

# Process each document
for i, doc in enumerate(documents):
    # Store in PostgreSQL
    # (This is handled automatically by the new system)
```

### 2. Application Migration

The application code has been updated to use PostgreSQL:

**Before (ChromaDB):**
```python
# ChromaDB operations
self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
results = self.collection.query(query_texts=[query], n_results=10)
```

**After (PostgreSQL):**
```python
# PostgreSQL operations
with self.SessionLocal() as db:
    for chunk in chunks:
        db_chunk = DBDocumentChunk(...)
        db.add(db_chunk)
    db.commit()

# Vector search
sql_query = "SELECT ... FROM document_chunks ORDER BY embedding <=> %s"
```

## Database Schema

### DocumentChunks Table

```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    chunk_id VARCHAR(255) UNIQUE NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    chunk_type VARCHAR(100) NOT NULL,
    page_number INTEGER,
    file_hash VARCHAR(64) NOT NULL,
    embedding vector(1536), -- OpenAI text-embedding-3-small dimension
    metadata TEXT, -- JSON string
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Indexes for Performance

```sql
-- Standard indexes
CREATE INDEX idx_document_chunks_document_name ON document_chunks(document_name);
CREATE INDEX idx_document_chunks_chunk_type ON document_chunks(chunk_type);
CREATE INDEX idx_document_chunks_file_hash ON document_chunks(file_hash);

-- Vector index for similarity search
CREATE INDEX idx_document_chunks_embedding ON document_chunks 
USING ivfflat (embedding vector_cosine_ops);
```

## Vector Search Implementation

### Similarity Search Query

```sql
SELECT 
    content,
    metadata,
    chunk_type,
    document_name,
    page_number,
    1 - (embedding <=> $1) as similarity_score
FROM document_chunks
WHERE chunk_type = $2
ORDER BY embedding <=> $1
LIMIT 10;
```

### Key Features

- **Cosine Similarity**: Using pgvector's `<=>` operator
- **IVFFlat Index**: Efficient approximate nearest neighbor search
- **Metadata Filtering**: Filter by document type, name, etc.
- **Configurable Limits**: Adjustable result counts

## Performance Optimizations

### 1. Connection Pooling

SQLAlchemy connection pool configuration:
```python
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)
```

### 2. Batch Operations

Bulk embedding generation and storage:
```python
# Generate embeddings in batches
embeddings = await self._generate_embeddings(texts)

# Bulk insert
with self.SessionLocal() as db:
    for i, chunk in enumerate(chunks):
        db_chunk = DBDocumentChunk(embedding=embeddings[i], ...)
        db.add(db_chunk)
    db.commit()
```

### 3. Index Optimization

- **IVFFlat Index**: For large datasets (>1M vectors)
- **HNSW Index**: For smaller datasets with high accuracy requirements
- **Regular Indexes**: For metadata filtering

## Monitoring and Maintenance

### 1. Database Monitoring

```sql
-- Check vector index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
WHERE indexname LIKE '%embedding%';

-- Monitor query performance
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
WHERE query LIKE '%embedding%'
ORDER BY total_time DESC;
```

### 2. Backup and Recovery

```bash
# Create backup
pg_dump -U postgres -d rag_system > backup.sql

# Restore backup
psql -U postgres -d rag_system < backup.sql
```

### 3. Maintenance Tasks

```sql
-- Analyze tables for query optimization
ANALYZE document_chunks;

-- Vacuum to reclaim storage
VACUUM ANALYZE document_chunks;

-- Reindex vector index if needed
REINDEX INDEX idx_document_chunks_embedding;
```

## Troubleshooting

### Common Issues

**1. pgvector Extension Not Found**
```bash
# Install pgvector extension
# Follow: https://github.com/pgvector/pgvector#installation
```

**2. Connection Errors**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify connection settings in .env
# Test connection manually
psql -U postgres -d rag_system -h localhost
```

**3. Vector Dimension Mismatch**
```sql
-- Check embedding dimension
SELECT array_length(embedding, 1) FROM document_chunks LIMIT 1;

-- Should return 1536 for OpenAI text-embedding-3-small
```

**4. Performance Issues**
```sql
-- Check index usage
EXPLAIN ANALYZE SELECT * FROM document_chunks 
ORDER BY embedding <=> '[0.1, 0.2, ...]' LIMIT 10;

-- Ensure vector index is being used
```

## Production Deployment

### 1. Database Configuration

```bash
# Production PostgreSQL settings
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

### 2. Connection Pooling

```python
# Production connection pool
engine = create_engine(
    database_url,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

### 3. Monitoring Setup

- **pg_stat_statements**: Query performance monitoring
- **pg_stat_monitor**: Advanced monitoring (if available)
- **Custom metrics**: Vector search latency, throughput

## Rollback Plan

If you need to rollback to ChromaDB:

1. **Keep ChromaDB code**: The old ChromaDB implementation is preserved
2. **Data backup**: Export PostgreSQL data before migration
3. **Configuration**: Switch environment variables
4. **Testing**: Verify functionality before production deployment

## Benefits Summary

| Aspect | ChromaDB | PostgreSQL + pgvector |
|--------|----------|----------------------|
| **ACID Compliance** | ❌ | ✅ |
| **Scalability** | Limited | High |
| **Backup/Restore** | Manual | Automated |
| **Monitoring** | Basic | Rich |
| **SQL Ecosystem** | ❌ | ✅ |
| **Vector Operations** | ✅ | ✅ |
| **Performance** | Good | Excellent |

## Next Steps

1. **Test the migration** in a development environment
2. **Validate performance** with your data volume
3. **Update monitoring** and alerting systems
4. **Train team** on PostgreSQL operations
5. **Plan production deployment** with rollback strategy

For questions or issues, refer to:
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) 