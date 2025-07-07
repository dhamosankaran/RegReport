#!/usr/bin/env python3
"""
RegReportRAG API Testing Script
Tests both positive and negative scenarios for the compliance API
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
COMPLIANCE_ENDPOINT = f"{BASE_URL}/api/v1/compliance/check"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/api/v1/documents/status"
RELOAD_ENDPOINT = f"{BASE_URL}/api/v1/documents/reload"

def print_test_header(test_name: str):
    """Print formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_result(test_case: str, status: str, details: str = ""):
    """Print test result"""
    emoji = "✅" if status == "PASS" else "❌"
    print(f"{emoji} {test_case}: {status}")
    if details:
        print(f"   Details: {details}")

def test_api_connectivity():
    """Test if API is accessible"""
    print_test_header("API Connectivity Test")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print_result("API Server", "PASS", "Backend is running and accessible")
            return True
        else:
            print_result("API Server", "FAIL", f"HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_result("API Server", "FAIL", f"Connection error: {e}")
        return False

def test_positive_scenarios():
    """Test positive compliance scenarios"""
    print_test_header("Positive Scenarios")
    
    test_cases = [
        {
            "name": "Compliant Query",
            "query": "We maintain customer data in encrypted databases with access controls and audit logs as required by data protection regulations.",
            "expected_status": ["compliant", "partial_compliance"]
        },
        {
            "name": "Partial Compliance Query", 
            "query": "We collect customer personal information and store it in our database, but we don't have a formal data retention policy.",
            "expected_status": ["partial_compliance", "non_compliant", "requires_review"]
        },
        {
            "name": "Complex Regulatory Query",
            "query": "Our new mobile banking app collects biometric data, location information, and transaction history. We use third-party analytics providers and cloud storage. What are the compliance requirements?",
            "expected_status": ["requires_review", "partial_compliance"]
        }
    ]
    
    for test_case in test_cases:
        try:
            start_time = time.time()
            response = requests.post(
                COMPLIANCE_ENDPOINT,
                json={"concern": test_case["query"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_time = end_time - start_time
                
                # Check if response has expected structure
                required_fields = ["status", "confidence_score", "reasoning", "compliance_details"]
                has_required_fields = all(field in result for field in required_fields)
                
                if has_required_fields and result["status"] in test_case["expected_status"]:
                    print_result(
                        test_case["name"], 
                        "PASS", 
                        f"Status: {result['status']}, Confidence: {result['confidence_score']:.2f}, Time: {response_time:.2f}s"
                    )
                else:
                    print_result(
                        test_case["name"], 
                        "PARTIAL", 
                        f"Unexpected status: {result.get('status', 'Unknown')}"
                    )
            else:
                print_result(
                    test_case["name"], 
                    "FAIL", 
                    f"HTTP {response.status_code}: {response.text[:100]}"
                )
                
        except requests.exceptions.RequestException as e:
            print_result(test_case["name"], "FAIL", f"Request error: {e}")

def test_negative_scenarios():
    """Test negative scenarios and error handling"""
    print_test_header("Negative Scenarios")
    
    test_cases = [
        {
            "name": "Empty Query",
            "query": "",
            "expected_error": True
        },
        {
            "name": "Whitespace Only Query",
            "query": "   \n\t   ",
            "expected_error": True
        },
        {
            "name": "Extremely Long Query",
            "query": "A" * 10000,
            "expected_error": False  # Should handle gracefully
        },
        {
            "name": "Special Characters",
            "query": "'; DROP TABLE users; --",
            "expected_error": False  # Should sanitize
        },
        {
            "name": "HTML/Script Injection",
            "query": "<script>alert('xss')</script>",
            "expected_error": False  # Should sanitize
        },
        {
            "name": "Template Injection",
            "query": "{{7*7}}",
            "expected_error": False  # Should handle safely
        }
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                COMPLIANCE_ENDPOINT,
                json={"concern": test_case["query"]},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if test_case["expected_error"]:
                if response.status_code == 400:
                    print_result(test_case["name"], "PASS", "Properly rejected invalid input")
                else:
                    print_result(test_case["name"], "FAIL", f"Should have rejected input but got HTTP {response.status_code}")
            else:
                if response.status_code == 200:
                    result = response.json()
                    print_result(test_case["name"], "PASS", f"Handled safely, Status: {result.get('status', 'Unknown')}")
                else:
                    print_result(test_case["name"], "FAIL", f"HTTP {response.status_code}: {response.text[:100]}")
                    
        except requests.exceptions.RequestException as e:
            print_result(test_case["name"], "FAIL", f"Request error: {e}")

def test_malformed_requests():
    """Test malformed request handling"""
    print_test_header("Malformed Request Tests")
    
    test_cases = [
        {
            "name": "Missing Concern Field",
            "data": {"not_concern": "test"},
            "expected_status": 422
        },
        {
            "name": "Invalid JSON",
            "data": "invalid json",
            "expected_status": 400
        },
        {
            "name": "Wrong Content Type",
            "data": {"concern": "test"},
            "headers": {"Content-Type": "text/plain"},
            "expected_status": 422
        }
    ]
    
    for test_case in test_cases:
        try:
            headers = test_case.get("headers", {"Content-Type": "application/json"})
            
            if isinstance(test_case["data"], str):
                response = requests.post(COMPLIANCE_ENDPOINT, data=test_case["data"], headers=headers, timeout=10)
            else:
                response = requests.post(COMPLIANCE_ENDPOINT, json=test_case["data"], headers=headers, timeout=10)
            
            if response.status_code == test_case["expected_status"]:
                print_result(test_case["name"], "PASS", f"Correctly returned HTTP {response.status_code}")
            else:
                print_result(test_case["name"], "FAIL", f"Expected HTTP {test_case['expected_status']}, got {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print_result(test_case["name"], "FAIL", f"Request error: {e}")

def test_document_endpoints():
    """Test document-related endpoints"""
    print_test_header("Document Endpoints")
    
    # Test document status
    try:
        response = requests.get(DOCUMENTS_ENDPOINT, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if "total_documents" in result and "total_chunks" in result:
                print_result(
                    "Document Status", 
                    "PASS", 
                    f"Total documents: {result['total_documents']}, Total chunks: {result['total_chunks']}"
                )
            else:
                print_result("Document Status", "FAIL", "Missing expected fields in response")
        else:
            print_result("Document Status", "FAIL", f"HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_result("Document Status", "FAIL", f"Request error: {e}")
    
    # Test document reload (if available)
    try:
        response = requests.post(RELOAD_ENDPOINT, timeout=30)
        if response.status_code in [200, 202]:
            print_result("Document Reload", "PASS", "Reload endpoint accessible")
        else:
            print_result("Document Reload", "FAIL", f"HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print_result("Document Reload", "FAIL", f"Request error: {e}")

def main():
    """Main test runner"""
    print("🚀 RegReportRAG API Testing Suite")
    print("=" * 60)
    
    # Check if API is accessible
    if not test_api_connectivity():
        print("\n❌ Cannot connect to API. Please ensure the backend is running on http://localhost:8000")
        sys.exit(1)
    
    # Run all test suites
    test_positive_scenarios()
    test_negative_scenarios()
    test_malformed_requests()
    test_document_endpoints()
    
    print("\n" + "=" * 60)
    print("🏁 Testing Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Review the test results above")
    print("2. Test the frontend UI at http://localhost:3000")
    print("3. Use the test scenarios in test_scenarios.md")
    print("4. Check both backend and frontend logs for any errors")

if __name__ == "__main__":
    main() 