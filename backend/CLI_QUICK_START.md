# Gemini Vector Service CLI - Quick Start Guide

This guide will help you quickly get started with the Gemini Vector Service CLI for loading documents and retrieving information.

## 🚀 Prerequisites

### 1. Environment Setup
```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies (if not already done)
pip install -r requirements.txt

# Set your Google API key
export GOOGLE_API_KEY="your-google-api-key-here"
```

### 2. Create Test Data (Optional)
```bash
# Create sample PDF files for testing
python create_test_pdfs.py
```

## 🎯 Quick Start Commands

### 📋 Show Help
```bash
# See all available commands
python gemini_cli.py --help

# Get help for a specific command
python gemini_cli.py load --help
```

### 📊 Check Status
```bash
# Check database status and loaded documents
python gemini_cli.py status
```

### 📄 Load Documents
```bash
# Load a single PDF
python gemini_cli.py load document.pdf

# Load multiple PDFs
python gemini_cli.py load file1.pdf file2.pdf file3.pdf

# Load all PDFs in current directory
python gemini_cli.py load *.pdf

# Load with detailed chunk information
python gemini_cli.py load document.pdf --show-chunks
```

### 🤖 Query Documents (RAG)
```bash
# Ask questions about your documents
python gemini_cli.py query "What are the compliance requirements?"

# Query with more context
python gemini_cli.py query "How should risk management be implemented?" --max-results 15

# Query without showing sources
python gemini_cli.py query "What is data governance?" --no-sources
```

### 🔍 Search Documents
```bash
# Search for similar content
python gemini_cli.py search "regulatory reporting"

# Search with more results
python gemini_cli.py search "risk assessment" --max-results 10
```

### 🗑️ Clear Database
```bash
# Clear all documents (with confirmation)
python gemini_cli.py clear

# Force clear without confirmation
python gemini_cli.py clear --yes
```

### 💬 Interactive Mode
```bash
# Enter interactive mode for multiple operations
python gemini_cli.py interactive
```

## 🎮 Interactive Mode Commands

Once in interactive mode, you can use these commands:

```
gemini> help                           # Show available commands
gemini> status                         # Check database status
gemini> load document.pdf              # Load a document
gemini> query What are the main risks? # Ask a question
gemini> search compliance              # Search for content
gemini> clear                          # Clear database
gemini> quit                           # Exit interactive mode
```

## 📚 Complete Workflow Example

Here's a complete workflow from start to finish:

### Step 1: Create Test Data
```bash
# Create sample PDFs
python create_test_pdfs.py
```

### Step 2: Check Initial Status
```bash
# Should show empty database
python gemini_cli.py status
```

### Step 3: Load Documents
```bash
# Load all the created PDFs
python gemini_cli.py load *.pdf
```

### Step 4: Verify Loading
```bash
# Should now show loaded documents
python gemini_cli.py status
```

### Step 5: Test Queries
```bash
# Test different types of queries
python gemini_cli.py query "What are the main compliance requirements?"
python gemini_cli.py query "How is risk management structured?"
python gemini_cli.py query "What are the data governance standards?"
```

### Step 6: Test Search
```bash
# Test semantic search
python gemini_cli.py search "risk categories"
python gemini_cli.py search "training requirements"
```

## 🎯 Example Output

### Loading Documents
```
============================================================
 LOADING DOCUMENTS 
============================================================
ℹ️  Found: Compliance_Guide.pdf
ℹ️  Found: Risk_Management_Policy.pdf
ℹ️  Found: Data_Governance_Manual.pdf
ℹ️  Processing 3 PDF files...

📊 Processing Results:
✅ Successfully processed: 3 files
  📄 Compliance_Guide.pdf: 8 chunks
  📄 Risk_Management_Policy.pdf: 7 chunks
  📄 Data_Governance_Manual.pdf: 5 chunks
```

### Querying Documents
```
============================================================
 QUERYING DOCUMENTS 
============================================================
ℹ️  Query: What are the compliance requirements?
ℹ️  Max results: 10

🤖 AI Answer:
----------------------------------------
Based on the regulatory documents provided, the main compliance requirements include:

1. **Documentation Requirements:**
   - Document retention period of minimum 7 years
   - Proper version control for all documents
   - Secured access controls with appropriate permissions
   - Annual reviews for accuracy and relevance

2. **Monitoring and Assessment:**
   - Quarterly compliance assessments
   - Key risk indicator (KRI) monitoring
   - Internal audit programs
   - Exception reporting and remediation tracking

3. **Reporting Standards:**
   - Monthly reports due by 15th of following month
   - Quarterly reports within 45 days of quarter end
   - Annual reports within 90 days of year end

4. **Training and Awareness:**
   - New employee orientation within 30 days
   - Annual refresher training for all staff
   - Role-specific specialized training
   - Maintained training records
----------------------------------------

📚 Sources (3 documents used):

  📄 Source 1: Compliance_Guide.pdf (Page 1)
     Similarity: 0.892
     Preview: This document outlines the essential compliance requirements for regulatory reporting...

  📄 Source 2: Compliance_Guide.pdf (Page 2)
     Similarity: 0.845
     Preview: All regulatory documents must be maintained in accordance with the following standards...
```

### Database Status
```
============================================================
 DATABASE STATUS 
============================================================
📊 Database Overview:
ℹ️  Total documents: 3
ℹ️  Total chunks: 20
ℹ️  Embedding model: models/text-embedding-004
ℹ️  LLM model: gemini-1.5-flash

📋 Loaded Documents:
  📄 Compliance_Guide.pdf: 8 chunks (loaded)
  📄 Risk_Management_Policy.pdf: 7 chunks (loaded)
  📄 Data_Governance_Manual.pdf: 5 chunks (loaded)
```

## 🔧 Advanced Usage Tips

### 1. **Optimizing Queries**
- Be specific in your questions for better results
- Use domain-specific terminology
- Ask follow-up questions to dive deeper

### 2. **Loading Strategy**
- Load related documents together for better context
- Use `--show-chunks` to understand how documents are processed
- Monitor the status regularly to track your document library

### 3. **Search vs Query**
- Use **search** to find specific content or passages
- Use **query** to get AI-generated answers with citations
- Combine both for comprehensive research

### 4. **Interactive Mode Benefits**
- Faster for multiple operations
- No need to reinitialize the service each time
- Great for exploratory work

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ GOOGLE_API_KEY environment variable is required
   ```
   **Solution**: Set your Google API key in environment or .env file

2. **No PDF Files Found**
   ```
   ❌ No valid PDF files found
   ```
   **Solution**: Check file paths and ensure files are PDFs

3. **Database Connection Error**
   ```
   ❌ Failed to initialize service
   ```
   **Solution**: Ensure PostgreSQL is running and properly configured

### Performance Tips

- Start with smaller documents to test the system
- Use appropriate `--max-results` values
- Monitor chunk counts to understand processing
- Clear database periodically to maintain performance

## 🚀 Next Steps

Once you're comfortable with the CLI:

1. **Explore Advanced Features**: Try different chunking configurations
2. **Integration**: Use the service in your own applications
3. **Scaling**: Load larger document collections
4. **Customization**: Modify the CLI for your specific needs

## 📞 Getting Help

- Use `python gemini_cli.py --help` for command reference
- Check the logs for detailed error information
- Review the README_GEMINI_VECTOR_SERVICE.md for technical details 