# RAG System Technical Overview

## System Architecture

```
User Query → Frontend → FastAPI → RAG Pipeline → OpenAI → PostgreSQL → Response → UI
```

## Core Workflow

### 1. Document Processing (Initialization)
```
PDF Files → Text Extraction → Semantic Chunking → OpenAI Embeddings → PostgreSQL + pgvector Storage
```

**Key Files:**
- `document_processor.py` - PDF processing and chunking
- `vector_service.py` - PostgreSQL operations with pgvector
- `database.py` - SQLAlchemy models and database setup

**Process:**
1. Extract text from Instructions.pdf and Rules.pdf using PyPDF2
2. Clean and normalize text content
3. Split into 1000-token chunks with 200-token overlap
4. Classify chunks by type (regulatory_rule, requirement, procedure, etc.)
5. Generate embeddings using OpenAI text-embedding-3-small
6. Store in PostgreSQL with pgvector extension for efficient similarity search

### 2. Query Processing (RAG Pipeline)
```
User Query → OpenAI Embedding → PostgreSQL Vector Search → Context Retrieval → OpenAI GPT-4o-mini → Response
```

**Key Components:**
- `rag_service.py` - Main RAG orchestration
- `vector_service.py` - Vector similarity search
- `openai_service.py` - LLM integration

**Process:**
1. Generate embedding for user query using OpenAI
2. Perform cosine similarity search in PostgreSQL using pgvector
3. Retrieve top-k most relevant document chunks
4. Format context for LLM prompt
5. Generate response using GPT-4o-mini
6. Return structured response with sources

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

-- Indexes for performance
CREATE INDEX idx_document_chunks_document_name ON document_chunks(document_name);
CREATE INDEX idx_document_chunks_chunk_type ON document_chunks(chunk_type);
CREATE INDEX idx_document_chunks_file_hash ON document_chunks(file_hash);
CREATE INDEX idx_document_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops);
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

**Features:**
- Cosine similarity using pgvector's `<=>` operator
- Efficient indexing with IVFFlat for large datasets
- Metadata filtering for targeted searches
- Configurable result limits

## API Endpoints

### Core Endpoints
- `POST /api/v1/chat` - Main chat interface
- `GET /api/v1/documents/status` - Document processing status
- `POST /api/v1/documents/reload` - Reload documents
- `GET /health` - Health check

### Response Format
```json
{
  "response": "AI-generated response",
  "sources": [
    {
      "content": "Relevant document chunk",
      "document_name": "Instructions.pdf",
      "page_number": 5,
      "similarity_score": 0.92
    }
  ],
  "metadata": {
    "total_tokens": 1500,
    "processing_time": 2.3
  }
}
```

## Environment Configuration

### Required Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Performance Optimizations

### Database Optimizations
- **pgvector IVFFlat Index**: Efficient approximate nearest neighbor search
- **Connection Pooling**: SQLAlchemy connection pool for concurrent requests
- **Batch Processing**: Bulk embedding generation and storage
- **Metadata Indexing**: Fast filtering by document type and name

### Caching Strategy
- **File Hash Caching**: Skip reprocessing unchanged documents
- **Embedding Caching**: Reuse embeddings for identical content
- **Query Result Caching**: Cache frequent search results

## Security Features

### Data Protection
- **Environment Variables**: Secure API key management
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy
- **File Hash Verification**: Ensure document integrity

### Access Control
- **CORS Configuration**: Frontend-only access
- **Rate Limiting**: Prevent API abuse
- **Error Handling**: Secure error messages

## Deployment Options

### Local Development
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Run the application
./start_rag_system.sh
```

### Production Deployment
- **PostgreSQL**: Managed database service (AWS RDS, Google Cloud SQL)
- **pgvector**: Ensure extension is enabled
- **Connection Pooling**: Configure for production load
- **Monitoring**: Database performance metrics

## Monitoring and Logging

### Database Metrics
- Query performance monitoring
- Vector search latency tracking
- Storage usage monitoring
- Connection pool statistics

### Application Logging
- Structured logging with python-json-logger
- Request/response logging
- Error tracking and alerting
- Performance profiling

## Migration from ChromaDB

> **Note:** The current system uses PostgreSQL (with pgvector) exclusively for all vector storage and retrieval. ChromaDB is no longer used in any part of the system.

### Key Changes
1. **Database**: ChromaDB → PostgreSQL + pgvector
2. **Embedding Storage**: Local files → Database columns
3. **Search**: ChromaDB client → SQL queries with pgvector
4. **Scalability**: File-based → ACID-compliant database
5. **Backup**: Manual → Automated database backups

### Benefits
- **ACID Compliance**: Transactional integrity
- **Scalability**: Handle larger datasets
- **Backup/Restore**: Standard database operations
- **Monitoring**: Rich database metrics
- **Integration**: Standard SQL ecosystem 