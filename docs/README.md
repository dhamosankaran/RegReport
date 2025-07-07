# RAG System Documentation

This directory contains comprehensive documentation for the Regulatory Compliance RAG System.

## Documentation Index

### 📋 Technical Documentation
- **[TECHNICAL_OVERVIEW.md](./TECHNICAL_OVERVIEW.md)** - High-level system architecture and workflow
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference and examples
- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Deployment instructions for different environments

### 🔧 System Architecture

The RAG system follows a modern microservices architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAG SYSTEM WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Query → Frontend → FastAPI → RAG Pipeline → OpenAI       │
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │  Document   │    │   Vector    │    │     LLM     │         │
│  │ Processing  │───▶│   Search    │───▶│  Analysis   │         │
│  │             │    │ (ChromaDB)  │    │ (GPT-4o)    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📖 Quick Navigation

#### For Developers
- **Getting Started**: See [TECHNICAL_OVERVIEW.md](./TECHNICAL_OVERVIEW.md) for system workflow
- **API Integration**: See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for endpoint details
- **Local Development**: Use the `start_rag_system.sh` script in the root directory

#### For DevOps/Deployment
- **Production Setup**: See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **Docker Deployment**: Docker Compose configurations included
- **Cloud Deployment**: AWS, GCP, and Kubernetes examples provided

#### For System Administration
- **Monitoring**: Prometheus metrics and logging configurations
- **Security**: Production security checklist and best practices
- **Scaling**: Horizontal scaling and performance optimization guidelines

### 🚀 Key Features Documented

1. **Document Processing Pipeline**
   - PDF text extraction and cleaning
   - Semantic chunking with 1000-token windows
   - Content type classification (rules, procedures, requirements)
   - Vector embedding generation and storage

2. **RAG Pipeline**
   - Hybrid search strategy (targeted + semantic)
   - Context building and prompt engineering
   - LLM analysis with structured JSON output
   - Response validation and error handling

3. **API Endpoints**
   - `/api/v1/compliance/check` - Main compliance analysis
   - `/api/v1/documents/status` - Document processing status
   - `/api/v1/documents/reload` - Document refresh capability
   - `/health` - System health monitoring

4. **Frontend Interface**
   - React-based user interface with Tailwind CSS
   - Real-time compliance checking
   - Interactive results with expandable sections
   - Document status monitoring

### 📊 Performance Metrics

| Component | Performance |
|-----------|-------------|
| Document Processing | ~50 pages/second |
| Vector Search | ~100ms average |
| LLM Analysis | ~3-5 seconds |
| Total Query Time | ~3-8 seconds |

### 🔐 Security Features

- Input validation and sanitization
- CORS configuration
- API key secure storage
- Error handling without information leakage
- Production security checklist

### 📈 Scalability

The system is designed for:
- **Horizontal scaling** with load balancers
- **Cloud deployment** (AWS, GCP, Kubernetes)
- **Containerization** with Docker
- **Monitoring** with Prometheus and logging

### 🔧 Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI + Pydantic |
| Vector DB | ChromaDB |
| Embeddings | SentenceTransformers |
| LLM | OpenAI GPT-4o-mini |
| Document Processing | PyPDF2 + LangChain |

---

## Getting Started

1. **Read the Technical Overview** - Understand the system architecture
2. **Review API Documentation** - Learn about available endpoints
3. **Follow Deployment Guide** - Set up your environment
4. **Run the System** - Use `./start_rag_system.sh` for local development

For questions or issues, refer to the troubleshooting sections in each document or check the main README.md in the project root. 