"""
Performance testing with Locust for RegReportRAG API
"""
import json
import random
from locust import HttpUser, task, between, events
from typing import Dict, Any

class RegReportRAGUser(HttpUser):
    """Simulates a user interacting with the RegReportRAG API."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts."""
        # Health check to ensure API is available
        try:
            response = self.client.get("/health")
            if response.status_code != 200:
                raise Exception(f"Health check failed: {response.status_code}")
        except Exception as e:
            self.environment.runner.quit()
            raise e
    
    @task(3)
    def health_check(self):
        """Health check endpoint - high frequency."""
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")
    
    @task(2)
    def get_document_status(self):
        """Get document status - medium frequency."""
        with self.client.get("/api/v1/documents/status", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if "total_documents" in data and "total_chunks" in data:
                    response.success()
                else:
                    response.failure("Invalid response format")
            else:
                response.failure(f"Document status failed: {response.status_code}")
    
    @task(1)
    def compliance_check(self):
        """Compliance check - lower frequency due to complexity."""
        # Sample compliance queries for testing
        test_queries = [
            {
                "concern": "Data privacy compliance for customer information handling",
                "context": "Processing customer data for financial services including personal information and transaction records"
            },
            {
                "concern": "Security requirements for data protection",
                "context": "Implementing access controls and encryption for sensitive customer data"
            },
            {
                "concern": "Audit trail maintenance requirements",
                "context": "Tracking data access and modifications for compliance reporting"
            },
            {
                "concern": "GDPR compliance for data processing",
                "context": "Handling European customer data according to GDPR regulations"
            },
            {
                "concern": "Financial regulatory compliance",
                "context": "Ensuring compliance with financial services regulations and reporting requirements"
            }
        ]
        
        query = random.choice(test_queries)
        
        with self.client.post(
            "/api/v1/compliance/check",
            json=query,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if "status" in data and "confidence" in data:
                    response.success()
                else:
                    response.failure("Invalid compliance response format")
            else:
                response.failure(f"Compliance check failed: {response.status_code}")
    
    @task(1)
    def reload_documents(self):
        """Reload documents - low frequency."""
        with self.client.post("/api/v1/documents/reload", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "reloaded" in data["message"]:
                    response.success()
                else:
                    response.failure("Invalid reload response format")
            else:
                response.failure(f"Document reload failed: {response.status_code}")

class ComplianceCheckUser(HttpUser):
    """Specialized user for intensive compliance checking."""
    
    wait_time = between(0.5, 1.5)  # Faster requests for load testing
    
    @task(10)
    def rapid_compliance_checks(self):
        """Rapid compliance checks for load testing."""
        # Generate random compliance queries
        concerns = [
            "Data encryption requirements",
            "Access control implementation",
            "Audit trail maintenance",
            "Data retention policies",
            "Security assessment procedures",
            "Incident response protocols",
            "Compliance monitoring systems",
            "Risk assessment frameworks",
            "Regulatory reporting requirements",
            "Data protection measures"
        ]
        
        contexts = [
            "Financial services data processing",
            "Healthcare information management",
            "E-commerce customer data handling",
            "Government compliance systems",
            "Educational institution data management",
            "Manufacturing quality control",
            "Transportation safety systems",
            "Energy sector compliance",
            "Telecommunications data handling",
            "Insurance claims processing"
        ]
        
        query = {
            "concern": random.choice(concerns),
            "context": random.choice(contexts)
        }
        
        with self.client.post(
            "/api/v1/compliance/check",
            json=query,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Rapid compliance check failed: {response.status_code}")

class DocumentManagementUser(HttpUser):
    """Specialized user for document management operations."""
    
    wait_time = between(2, 5)  # Slower requests for document operations
    
    @task(5)
    def document_status_checks(self):
        """Frequent document status checks."""
        with self.client.get("/api/v1/documents/status", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Document status check failed: {response.status_code}")
    
    @task(1)
    def document_reload(self):
        """Document reload operations."""
        with self.client.post("/api/v1/documents/reload", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Document reload failed: {response.status_code}")

# Custom event handlers for monitoring
@events.request.add_listener
def my_request_handler(request_type, name, response_time, response_length, response, context, exception, start_time, url, **kwargs):
    """Custom request handler for detailed monitoring."""
    if exception:
        print(f"Request failed: {name} - {exception}")
    elif response.status_code >= 400:
        print(f"Request error: {name} - {response.status_code}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when the test starts."""
    print("Performance test starting...")
    print(f"Target host: {environment.host}")
    print(f"Number of users: {environment.runner.user_count}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when the test stops."""
    print("Performance test completed.")

# Custom metrics collection
class CustomMetrics:
    """Custom metrics collection for detailed performance analysis."""
    
    def __init__(self):
        self.response_times = []
        self.error_counts = {}
        self.success_counts = {}
    
    def record_response(self, name: str, response_time: float, success: bool):
        """Record response metrics."""
        self.response_times.append(response_time)
        
        if success:
            self.success_counts[name] = self.success_counts.get(name, 0) + 1
        else:
            self.error_counts[name] = self.error_counts.get(name, 0) + 1
    
    def get_average_response_time(self) -> float:
        """Get average response time."""
        return sum(self.response_times) / len(self.response_times) if self.response_times else 0
    
    def get_error_rate(self) -> Dict[str, float]:
        """Get error rates by endpoint."""
        error_rates = {}
        for name in set(list(self.success_counts.keys()) + list(self.error_counts.keys())):
            total = self.success_counts.get(name, 0) + self.error_counts.get(name, 0)
            if total > 0:
                error_rates[name] = self.error_counts.get(name, 0) / total
        return error_rates

# Global metrics instance
metrics = CustomMetrics()

@events.request.add_listener
def metrics_handler(request_type, name, response_time, response_length, response, context, exception, start_time, url, **kwargs):
    """Handler for collecting custom metrics."""
    success = response.status_code < 400 and exception is None
    metrics.record_response(name, response_time, success)

@events.test_stop.add_listener
def print_metrics(environment, **kwargs):
    """Print custom metrics at test end."""
    print("\n=== Custom Performance Metrics ===")
    print(f"Average Response Time: {metrics.get_average_response_time():.2f}ms")
    print("Error Rates by Endpoint:")
    for endpoint, rate in metrics.get_error_rate().items():
        print(f"  {endpoint}: {rate:.2%}")
    print("================================\n") 