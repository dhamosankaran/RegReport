# RegReportRAG UI Testing Scenarios

## 🧪 Comprehensive Test Plan for UI Testing

### 📋 **Test Setup**
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

---

## ✅ **POSITIVE TEST SCENARIOS**

### 1. **Compliance Checking - Valid Scenarios**

#### 1.1 **Compliant Query**
**Test Case**: Submit a query that should be compliant with regulations
```
Query: "We maintain customer data in encrypted databases with access controls and audit logs as required by data protection regulations."

Expected Result:
- Status: "compliant" (green)
- Confidence Score: High (>0.8)
- Detailed reasoning provided
- Relevant rule references shown
- Recommendations section populated
```

#### 1.2 **Partial Compliance Query**
**Test Case**: Submit a query with some compliance gaps
```
Query: "We collect customer personal information and store it in our database, but we don't have a formal data retention policy."

Expected Result:
- Status: "partial_compliance" (yellow)
- Confidence Score: Medium (0.5-0.8)
- Specific gaps identified
- Action items provided
- Deadline information if applicable
```

#### 1.3 **Complex Regulatory Query**
**Test Case**: Multi-faceted compliance question
```
Query: "Our new mobile banking app collects biometric data, location information, and transaction history. We use third-party analytics providers and cloud storage. What are the compliance requirements?"

Expected Result:
- Status: "requires_review" (blue)
- Multiple rule references
- Comprehensive analysis
- Detailed recommendations
- Impact assessment
```

### 2. **Document Status - Positive Scenarios**

#### 2.1 **Document Loading Verification**
**Test Steps**:
1. Navigate to "Documents" page
2. Verify document status shows:
   - Instructions.pdf: ✅ Loaded (37 chunks)
   - Rules.pdf: ✅ Loaded (108 chunks)
   - Total: 145 chunks processed

#### 2.2 **Document Reload Functionality**
**Test Steps**:
1. Click "Reload Documents" button
2. Verify loading spinner appears
3. Verify success message
4. Verify document counts remain consistent

### 3. **How It Works Page - Navigation**

#### 3.1 **Section Navigation**
**Test Steps**:
1. Navigate to "How It Works" page
2. Test all navigation sections:
   - System Overview
   - Technical Architecture
   - Data Processing Workflow
   - Compliance Checking
   - Technical Implementation
   - Business Requirements
3. Verify content loads correctly for each section

#### 3.2 **Interactive Elements**
**Test Steps**:
1. Test expandable workflow sections
2. Verify system architecture diagram renders
3. Test responsive design on different screen sizes

---

## ❌ **NEGATIVE TEST SCENARIOS**

### 1. **Compliance Checking - Error Scenarios**

#### 1.1 **Empty Query Submission**
**Test Case**: Submit empty or whitespace-only query
```
Query: ""

Expected Result:
- Error message: "Please enter a query"
- No API call made
- Form validation prevents submission
```

#### 1.2 **Extremely Long Query**
**Test Case**: Submit query exceeding reasonable limits
```
Query: [10,000+ character string]

Expected Result:
- Error handling for oversized input
- Graceful degradation
- Appropriate error message
```

#### 1.3 **Special Characters and Injection Attempts**
**Test Case**: Test with potentially problematic input
```
Query: "'; DROP TABLE users; --"
Query: "<script>alert('xss')</script>"
Query: "{{7*7}}"

Expected Result:
- Input sanitization working
- No code execution
- Safe error handling
```

### 2. **API Failure Scenarios**

#### 2.1 **Backend Server Down**
**Test Steps**:
1. Stop the backend server
2. Submit a compliance query
3. Verify error handling:
   - User-friendly error message
   - No application crash
   - Retry mechanism if applicable

#### 2.2 **Network Timeout**
**Test Steps**:
1. Simulate slow network conditions
2. Submit query and wait
3. Verify timeout handling:
   - Loading spinner shows
   - Appropriate timeout message
   - Ability to retry

#### 2.3 **Invalid API Response**
**Test Case**: Test with malformed backend responses
- Verify graceful error handling
- User-friendly error messages
- Application stability maintained

### 3. **OpenAI API Failures**

#### 3.1 **API Key Issues**
**Test Steps**:
1. Temporarily invalidate OpenAI API key
2. Submit compliance query
3. Verify error handling:
   - "Service temporarily unavailable" message
   - No sensitive error details exposed
   - Graceful degradation

#### 3.2 **Rate Limiting**
**Test Steps**:
1. Submit multiple rapid queries
2. Verify rate limit handling:
   - Appropriate delay messages
   - Queue management
   - User feedback

### 4. **Database Connection Issues**

#### 4.1 **Vector Database Unavailable**
**Test Steps**:
1. Temporarily stop PostgreSQL
2. Submit compliance query
3. Verify error handling:
   - Database connection error handling
   - User-friendly error message
   - No application crash

#### 4.2 **Empty Database**
**Test Steps**:
1. Clear document_chunks table
2. Submit compliance query
3. Verify handling:
   - "No documents available" message
   - Prompt to reload documents
   - Graceful degradation

---

## 🔧 **TESTING TOOLS AND COMMANDS**

### Backend API Testing
```bash
# Test compliance endpoint
curl -X POST "http://localhost:8000/api/v1/compliance/check" \
  -H "Content-Type: application/json" \
  -d '{"query": "Test compliance query"}'

# Test document status
curl -X GET "http://localhost:8000/api/v1/documents/status"

# Test document reload
curl -X POST "http://localhost:8000/api/v1/documents/reload"
```

### Database Testing
```bash
# Check document chunks
psql rag_system -c "SELECT COUNT(*) FROM document_chunks;"

# Check specific document
psql rag_system -c "SELECT document_name, COUNT(*) FROM document_chunks GROUP BY document_name;"

# Simulate empty database
psql rag_system -c "DELETE FROM document_chunks;"
```

### Frontend Testing
```bash
# Start frontend with different ports
npm start -- --port 3001

# Build production version
npm run build

# Test build
npx serve -s build
```

---

## 📊 **EXPECTED RESULTS SUMMARY**

### ✅ **Positive Scenarios Should Show:**
- ✅ Fast response times (< 5 seconds)
- ✅ Accurate compliance analysis
- ✅ Proper status indicators
- ✅ Detailed explanations
- ✅ Relevant document references
- ✅ Professional UI/UX
- ✅ Responsive design

### ❌ **Negative Scenarios Should Show:**
- ❌ Graceful error handling
- ❌ User-friendly error messages
- ❌ No application crashes
- ❌ Input validation working
- ❌ Security measures active
- ❌ Proper fallback mechanisms
- ❌ Consistent UI state

---

## 🎯 **TESTING CHECKLIST**

### Before Testing:
- [ ] Backend server running (port 8000)
- [ ] Frontend server running (port 3000)
- [ ] Database connected and populated
- [ ] OpenAI API key valid
- [ ] Network connectivity stable

### During Testing:
- [ ] Document all results
- [ ] Take screenshots of errors
- [ ] Note response times
- [ ] Test on different browsers
- [ ] Test on different screen sizes
- [ ] Test with different user inputs

### After Testing:
- [ ] Compile test results
- [ ] Identify improvement areas
- [ ] Document any bugs found
- [ ] Verify all critical paths work
- [ ] Confirm error handling is robust

---

## 🚀 **QUICK START TESTING**

1. **Start Both Servers**:
   ```bash
   # Terminal 1: Backend
   cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Frontend
   cd frontend && npm start
   ```

2. **Open Browser**: Navigate to http://localhost:3000

3. **Run Test Scenarios**: Follow the test cases above in order

4. **Monitor Logs**: Check both backend and frontend console logs

5. **Document Results**: Note any issues or unexpected behavior

---

## 📝 **TEST RESULT TEMPLATE**

```
Test Case: [Name]
Input: [What was tested]
Expected: [What should happen]
Actual: [What actually happened]
Status: [PASS/FAIL]
Notes: [Additional observations]
Screenshot: [If applicable]
```

This comprehensive test plan will help you verify that your RegReportRAG system handles both successful operations and error conditions gracefully! 