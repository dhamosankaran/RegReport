# PDF to Vector Database Loader

A standalone script to load PDF files into the PostgreSQL vector database without running the full FastAPI application.

## Features

- 🔄 **Standalone Processing**: Load PDFs without starting the web server
- 📊 **Smart Duplicate Detection**: Skips already processed files (based on file hash)
- 🔍 **Status Monitoring**: Check current document status and statistics
- 📁 **Flexible File Input**: Process default PDFs or specify custom files
- 🔄 **Reload Capability**: Clear and reprocess all documents
- 📝 **Comprehensive Logging**: Detailed logs for debugging and monitoring

## Prerequisites

1. **Database Setup**: Ensure PostgreSQL with pgvector is running
2. **Environment Variables**: Configure `.env` file with database credentials
3. **Dependencies**: Install required Python packages

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database (if not already done)
cd backend
python setup_database.py
```

## Usage Examples

### 1. Load Default PDFs

Place your PDF files in the project root directory:
- `Instructions.pdf`
- `Rules.pdf`

```bash
cd backend
python load_pdfs_to_vector_db.py
```

### 2. Load Custom PDF Files

```bash
cd backend
python load_pdfs_to_vector_db.py --pdf-files /path/to/document1.pdf /path/to/document2.pdf
```

### 3. Check Document Status

```bash
cd backend
python load_pdfs_to_vector_db.py --status
```

### 4. Reload All Documents

```bash
cd backend
python load_pdfs_to_vector_db.py --reload
```

## What the Script Does

1. **Initialization**:
   - Connects to PostgreSQL database
   - Initializes vector service and document processor
   - Sets up logging

2. **PDF Processing**:
   - Extracts text from PDF files using PyPDF2
   - Cleans and normalizes text content
   - Splits text into semantic chunks (1000 tokens with 200 overlap)
   - Classifies chunk types (regulatory_rule, procedure, requirement, etc.)

3. **Vector Generation**:
   - Creates embeddings using OpenAI's text-embedding-3-small model
   - Generates 1536-dimensional vectors for each chunk

4. **Database Storage**:
   - Stores chunks and embeddings in PostgreSQL with pgvector
   - Maintains metadata for each chunk (page numbers, document names, etc.)
   - Uses MD5 hashes to detect file changes

## Example Output

```
🚀 PDF to Vector Database Loader
==================================================
2024-01-15 10:30:15 [INFO] Initializing PDF loader...
2024-01-15 10:30:16 [INFO] PDF loader initialized successfully
2024-01-15 10:30:16 [INFO] Loading default PDF files from project root...
2024-01-15 10:30:16 [INFO] Found 2 PDF files to process
2024-01-15 10:30:16 [INFO]   - /path/to/Instructions.pdf
2024-01-15 10:30:16 [INFO]   - /path/to/Rules.pdf
2024-01-15 10:30:16 [INFO] Processing 2 PDF files...
2024-01-15 10:30:16 [INFO] Processing PDF 1/2: Instructions.pdf
2024-01-15 10:30:18 [INFO]   ✅ Processed: Instructions.pdf (45 chunks)
2024-01-15 10:30:18 [INFO] Processing PDF 2/2: Rules.pdf
2024-01-15 10:30:20 [INFO]   ✅ Processed: Rules.pdf (38 chunks)
2024-01-15 10:30:20 [INFO] 🎉 PDF loading completed! Total chunks: 83

📊 Current Document Status:
  Total Documents: 2
  Total Chunks: 83
  Last Refresh: 2024-01-15 10:30:20

📋 Document Details:
  - Instructions.pdf: loaded (45 chunks)
  - Rules.pdf: loaded (38 chunks)
```

## Configuration

The script uses the same environment variables as the main application:

```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Verify pgvector extension is installed

2. **PDF Processing Error**:
   - Check if PDF files exist and are readable
   - Ensure PyPDF2 can parse the PDF format
   - Check file permissions

3. **OpenAI API Error**:
   - Verify OPENAI_API_KEY is set correctly
   - Check API quota and billing
   - Ensure API key has embedding permissions

### Debug Mode

For detailed debugging, modify the logging level:

```python
setup_logging(log_level="DEBUG", log_dir="logs")
```

## Integration with Main Application

Once PDFs are loaded using this script, the main FastAPI application can immediately use them for compliance checking without any additional setup.

## Performance Notes

- **Chunk Size**: 1000 tokens with 200 overlap (configurable)
- **Embedding Model**: OpenAI text-embedding-3-small (1536 dimensions)
- **Processing Speed**: ~2-3 pages per second (depends on content complexity)
- **Memory Usage**: Processes files one at a time to manage memory

## File Structure

```
backend/
├── load_pdfs_to_vector_db.py    # Main loader script
├── setup_database.py            # Database setup script
├── app/
│   ├── services/
│   │   ├── vector_service.py    # Vector database operations
│   │   └── document_processor.py # PDF processing logic
│   └── models/
│       └── database.py          # Database models
└── logs/                        # Log files
``` 