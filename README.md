# Regulatory Compliance RAG System

A comprehensive AI-powered Retrieval-Augmented Generation (RAG) system for regulatory compliance checking. This system analyzes user concerns against regulatory documents (Instructions.pdf and Rules.pdf) and provides detailed compliance assessments with reasoning, impacted rules, and actionable recommendations.

## 🚀 Features

- **AI-Powered Analysis**: Uses OpenAI GPT-4o-mini for intelligent compliance assessment
- **Semantic Document Search**: ChromaDB vector database with advanced chunking strategy
- **Real-time Processing**: Fast document retrieval and analysis
- **Detailed Reporting**: Comprehensive compliance reports with confidence scores
- **Interactive UI**: Modern React-based web interface
- **Rule Impact Analysis**: Identifies specific rules and regulations affected
- **Actionable Recommendations**: Provides clear next steps for compliance
- **Document Management**: Monitor and reload regulatory documents

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   FastAPI       │    │   ChromaDB      │
│   (Port 3000)   │───▶│   Backend       │───▶│   Vector Store  │
│                 │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   OpenAI API    │
                       │   GPT-4o-mini   │
                       └─────────────────┘
```

## 📋 Prerequisites

- **Python 3.8+** - Backend development
- **Node.js 16+** - Frontend development
- **npm** - Package management
- **OpenAI API Key** - For AI-powered analysis
- **Instructions.pdf** - Regulatory instructions document
- **Rules.pdf** - Regulatory rules document

## 🚀 Quick Start

1. **Clone or setup the project structure:**
   ```bash
   # Ensure you have the following files in your project root:
   # - Instructions.pdf
   # - Rules.pdf
   # - start_rag_system.sh
   ```

2. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. **Make the startup script executable:**
   ```bash
   chmod +x start_rag_system.sh
   ```

4. **Run the system:**
   ```bash
   ./start_rag_system.sh
   ```

The script will:
- ✅ Check all prerequisites
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ Configure the database
- ✅ Start both backend and frontend servers
- ✅ Process the regulatory documents

## 🌐 Access the Application

Once running, access the application at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
RegReportRAG/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── models/            # Pydantic models and schemas
│   │   │   └── schemas.py
│   │   └── services/          # Business logic services
│   │       ├── document_processor.py  # PDF processing & chunking
│   │       ├── vector_service.py      # ChromaDB operations
│   │       └── rag_service.py         # RAG pipeline orchestration
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Header.js
│   │   │   ├── ComplianceChecker.js
│   │   │   ├── ComplianceResult.js
│   │   │   ├── DocumentStatus.js
│   │   │   └── LoadingSpinner.js
│   │   ├── services/          # API service layer
│   │   │   └── api.js
│   │   ├── App.js             # Main React application
│   │   └── index.js           # React entry point
│   ├── package.json           # Node.js dependencies
│   └── tailwind.config.js     # Tailwind CSS configuration
├── data/                      # Data storage
│   └── chromadb/             # ChromaDB persistence
├── venv/                      # Python virtual environment
├── Instructions.pdf           # Regulatory instructions document
├── Rules.pdf                  # Regulatory rules document
├── start_rag_system.sh        # System startup script
└── README.md                  # This file
```

## 🔧 Technical Implementation

### Document Processing Pipeline

1. **PDF Text Extraction**: Uses PyPDF2 for reliable text extraction
2. **Semantic Chunking**: Intelligent text splitting with context preservation
3. **Chunk Classification**: Categorizes content (rules, procedures, requirements, etc.)
4. **Vector Embedding**: Generates semantic embeddings using SentenceTransformers
5. **Vector Storage**: Persists embeddings in PostgreSQL (pgvector) for fast retrieval

### RAG Pipeline

1. **Query Processing**: Analyzes user concerns and context
2. **Semantic Search**: Retrieves relevant document chunks using vector similarity
3. **Context Building**: Constructs comprehensive context from retrieved documents
4. **LLM Analysis**: Uses OpenAI GPT-4o-mini for compliance assessment
5. **Response Formatting**: Structures detailed compliance reports

### Chunking Strategy

- **Semantic Boundaries**: Respects paragraph and sentence boundaries
- **Context Preservation**: Maintains document structure and page references
- **Optimal Size**: Balances context richness with retrieval precision
- **Content Classification**: Categorizes chunks by regulatory content type
- **Metadata Enrichment**: Adds page numbers, document sources, and relevance scores

## 🔍 API Endpoints

### Compliance Checking
- `POST /api/v1/compliance/check` - Check regulatory compliance
- `GET /api/v1/documents/status` - Get document processing status
- `POST /api/v1/documents/reload` - Reload regulatory documents

### System Health
- `GET /health` - Health check endpoint
- `GET /` - API information

## 🎯 Usage Examples

### Basic Compliance Check
```bash
curl -X POST "http://localhost:8000/api/v1/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{
    "concern": "Can we store customer data in international servers?",
    "context": "We are planning to expand our services globally"
  }'
```

### Document Status Check
```bash
curl -X GET "http://localhost:8000/api/v1/documents/status"
```

## 📊 Response Format

The system provides detailed compliance responses including:

- **Compliance Status**: compliant, non_compliant, partial_compliance, requires_review
- **Confidence Score**: 0-1 confidence level
- **Impacted Rules**: List of specific regulatory rules affected
- **Detailed Analysis**: Comprehensive reasoning and assessment
- **Recommendations**: Actionable next steps
- **Source Documents**: Relevant document excerpts with relevance scores
- **Processing Metadata**: Timing and processing information

## 🛠️ Configuration

### Environment Variables
```bash
# Backend (.env file)
OPENAI_API_KEY=your-openai-api-key-here
API_HOST=0.0.0.0
API_PORT=8000

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

### Advanced Configuration
- **Chunk Size**: Modify `max_chunk_size` in `document_processor.py`
- **Retrieval Count**: Adjust `max_retrieved_docs` in `rag_service.py`
- **Model Selection**: Change `model_name` in `rag_service.py`

## 🔄 Document Updates

To update regulatory documents:

1. Replace `Instructions.pdf` and/or `Rules.pdf` in the project root
2. Use the "Reload Documents" button in the web interface
3. Or call the reload API endpoint:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/documents/reload"
   ```

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not set"**
   - Set the environment variable: `export OPENAI_API_KEY="your-key"`
   - Or create a `.env` file in the backend directory

2. **"Documents not found"**
   - Ensure `Instructions.pdf` and `Rules.pdf` are in the project root
   - Check file permissions

3. **"Backend server failed to start"**
   - Check if port 8000 is available
   - Verify Python dependencies are installed
   - Check the backend logs for specific errors

4. **"Frontend build fails"**
   - Ensure Node.js 16+ is installed
   - Delete `node_modules` and run `npm install` again
   - Check for any missing dependencies

### Log Analysis
- Backend logs: Available in the terminal running the backend
- Frontend logs: Check browser console for React errors
- API logs: Monitor network requests in browser dev tools

## 📈 Performance Optimization

- **Chunking**: Optimized for 1000-token chunks with 200-token overlap
- **Caching**: ChromaDB provides efficient vector caching
- **Async Processing**: Asynchronous document processing and API calls
- **Batch Operations**: Efficient batch processing for multiple documents

## 🔒 Security Considerations

- **API Key Security**: Store OpenAI API keys securely
- **Input Validation**: Comprehensive input validation and sanitization
- **Rate Limiting**: Consider implementing rate limiting for production
- **CORS**: Configured for local development (adjust for production)

## 🚀 Production Deployment

For production deployment:

1. **Environment Setup**:
   - Use production-grade database (PostgreSQL for metadata)
   - Configure proper CORS origins
   - Set up SSL/TLS certificates
   - Use environment-specific configuration

2. **Scaling**:
   - Deploy backend with gunicorn/uvicorn workers
   - Use nginx for reverse proxy
   - Consider containerization with Docker
   - Implement horizontal scaling for high load

3. **Monitoring**:
   - Add logging and monitoring
   - Set up health checks
   - Monitor API performance and usage
   - Track document processing metrics

## 📄 License

This project is for educational and internal use. Ensure compliance with OpenAI's terms of service and your organization's policies.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review the API documentation at `/docs`
- Examine the logs for specific error messages
- Verify all prerequisites are met

---

**Built with ❤️ using FastAPI, React, and OpenAI** 