# RAG System API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
- No authentication required for local development
- For production: Consider implementing API key authentication

## Content Type
All requests and responses use `application/json`

---

## Endpoints

### 1. Compliance Check

**Endpoint:** `POST /api/v1/compliance/check`

**Description:** Analyze regulatory compliance for a given concern

**Request Body:**
```json
{
  "concern": "string (required)",
  "context": "string (optional)"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{
    "concern": "Can we store customer data in international servers?",
    "context": "We are planning to expand our services globally"
  }'
```

**Response Schema:**
```json
{
  "status": "compliant|non_compliant|partial_compliance|requires_review",
  "confidence_score": 0.85,
  "summary": "Brief summary of the assessment",
  "impacted_rules": ["Rule 1", "Rule 2"],
  "compliance_details": [
    {
      "rule_reference": "Section 4.2",
      "description": "Detailed description",
      "impact_level": "high|medium|low",
      "required_action": "Action needed if applicable",
      "deadline": "Deadline if applicable"
    }
  ],
  "relevant_documents": [
    {
      "document_name": "Instructions.pdf",
      "section": "Page 15",
      "content": "Relevant excerpt...",
      "relevance_score": 0.89
    }
  ],
  "reasoning": "Detailed reasoning for the assessment",
  "recommendations": ["Recommendation 1", "Recommendation 2"],
  "query_timestamp": "2024-01-15T10:30:00Z",
  "processing_time_ms": 3240
}
```

**Response Codes:**
- `200 OK` - Successful analysis
- `400 Bad Request` - Invalid input
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Processing error

---

### 2. Document Status

**Endpoint:** `GET /api/v1/documents/status`

**Description:** Get the status of regulatory documents in the vector database

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/v1/documents/status"
```

**Response Schema:**
```json
{
  "total_documents": 2,
  "total_chunks": 245,
  "documents": [
    {
      "document_name": "Instructions.pdf",
      "chunk_count": 123,
      "last_updated": "2024-01-15T10:30:00Z",
      "status": "loaded|error|processing"
    },
    {
      "document_name": "Rules.pdf", 
      "chunk_count": 122,
      "last_updated": "2024-01-15T10:30:00Z",
      "status": "loaded"
    }
  ],
  "last_refresh": "2024-01-15T10:30:00Z"
}
```

**Response Codes:**
- `200 OK` - Status retrieved successfully
- `500 Internal Server Error` - Database error

---

### 3. Reload Documents

**Endpoint:** `POST /api/v1/documents/reload`

**Description:** Reload regulatory documents into the vector database

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/documents/reload"
```

**Response Schema:**
```json
{
  "message": "Documents reloaded successfully"
}
```

**Response Codes:**
- `200 OK` - Documents reloaded successfully
- `500 Internal Server Error` - Reload failed

---

### 4. Health Check

**Endpoint:** `GET /health`

**Description:** Check system health and connectivity

**Example Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response Schema:**
```json
{
  "status": "healthy",
  "vector_db": "connected|disconnected"
}
```

**Response Codes:**
- `200 OK` - System healthy
- `503 Service Unavailable` - System unhealthy

---

### 5. API Information

**Endpoint:** `GET /`

**Description:** Get API information and version

**Example Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response Schema:**
```json
{
  "message": "Regulatory Compliance RAG API",
  "version": "1.0.0"
}
```

---

## Data Models

### ComplianceQuery
```json
{
  "concern": "string (required, max 2000 chars)",
  "context": "string (optional, max 1000 chars)"
}
```

### ComplianceResponse
```json
{
  "status": "enum: compliant|non_compliant|partial_compliance|requires_review",
  "confidence_score": "float (0.0-1.0)",
  "summary": "string",
  "impacted_rules": ["string"],
  "compliance_details": [ComplianceDetail],
  "relevant_documents": [RelevantDocument],
  "reasoning": "string",
  "recommendations": ["string"],
  "query_timestamp": "datetime (ISO 8601)",
  "processing_time_ms": "integer (optional)"
}
```

### ComplianceDetail
```json
{
  "rule_reference": "string",
  "description": "string", 
  "impact_level": "enum: high|medium|low",
  "required_action": "string (optional)",
  "deadline": "string (optional)"
}
```

### RelevantDocument
```json
{
  "document_name": "string",
  "section": "string",
  "content": "string",
  "relevance_score": "float (0.0-1.0)"
}
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error description"
}
```

### Common Error Scenarios

**400 Bad Request:**
```json
{
  "detail": "Concern field is required"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "concern"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Failed to process compliance check"
}
```

---

## Rate Limiting (Production)

For production deployment, consider implementing:
- Rate limiting: 100 requests per minute per IP
- API key authentication
- Request size limits
- Timeout configurations

---

## Example Workflows

### Basic Compliance Check
```bash
# 1. Check system health
curl -X GET "http://localhost:8000/health"

# 2. Check document status  
curl -X GET "http://localhost:8000/api/v1/documents/status"

# 3. Submit compliance query
curl -X POST "http://localhost:8000/api/v1/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{
    "concern": "Can we implement automated decision making for loan approvals?",
    "context": "We want to use ML models for faster processing"
  }'
```

### Document Management
```bash
# 1. Check current document status
curl -X GET "http://localhost:8000/api/v1/documents/status"

# 2. Reload documents (after updating PDFs)
curl -X POST "http://localhost:8000/api/v1/documents/reload"

# 3. Verify reload completion
curl -X GET "http://localhost:8000/api/v1/documents/status"
```

---

## OpenAPI/Swagger Documentation

Interactive API documentation is available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## Performance Guidelines

### Request Optimization
- Keep concerns concise but specific
- Provide relevant context for better analysis
- Avoid extremely long input text

### Response Handling
- Expect 3-8 second response times for compliance checks
- Implement timeout handling (30 seconds recommended)
- Cache document status for better UX

### Best Practices
- Validate input on client side
- Handle network errors gracefully
- Display loading states during processing
- Show confidence scores to users 