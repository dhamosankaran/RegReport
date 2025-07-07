# RegReportRAG E2E Testing Guide

This document provides comprehensive guidance for running and maintaining the E2E testing suite for the RegReportRAG application.

## Table of Contents

1. [Overview](#overview)
2. [Test Architecture](#test-architecture)
3. [Setup Instructions](#setup-instructions)
4. [Running Tests](#running-tests)
5. [Test Categories](#test-categories)
6. [CI/CD Integration](#cicd-integration)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Overview

The RegReportRAG E2E testing suite provides comprehensive testing coverage across multiple layers:

- **Backend API Tests**: FastAPI endpoint testing with pytest
- **Frontend Component Tests**: React component testing with Jest and React Testing Library
- **E2E Browser Tests**: Full browser automation with Playwright
- **Performance Tests**: Load testing with Locust
- **Security Tests**: Vulnerability scanning with Bandit and Safety

## Test Architecture

```
RegReportRAG/
├── backend/
│   └── tests/
│       ├── conftest.py              # Pytest configuration and fixtures
│       ├── test_api_endpoints.py    # API endpoint tests
│       └── test_services.py         # Service layer tests
├── frontend/
│   └── src/__tests__/
│       ├── setupTests.js            # Jest setup configuration
│       └── App.test.js              # React component tests
├── e2e/
│   ├── playwright.config.js         # Playwright configuration
│   ├── global-setup.js              # E2E test setup
│   ├── global-teardown.js           # E2E test cleanup
│   └── tests/
│       └── compliance-checker.spec.js # E2E browser tests
├── performance/
│   └── locustfile.py                # Performance testing configuration
└── .github/workflows/
    └── e2e-tests.yml                # CI/CD pipeline
```

## Setup Instructions

### Prerequisites

1. **Python 3.11+**
2. **Node.js 18+**
3. **Docker and Docker Compose**
4. **PostgreSQL with pgvector extension**

### Backend Testing Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Set up test environment variables
export POSTGRES_DB=rag_system_test
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password
```

### Frontend Testing Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Install testing dependencies (if not already included)
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### E2E Testing Setup

```bash
# Navigate to e2e directory
cd e2e

# Install Playwright
npm install
npx playwright install --with-deps

# Install testing dependencies
npm install @playwright/test
```

### Performance Testing Setup

```bash
# Install Locust
pip install locust

# Navigate to performance directory
cd performance
```

## Running Tests

### Backend Tests

```bash
# Run all backend tests
cd backend
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_api_endpoints.py -v

# Run specific test class
pytest tests/test_api_endpoints.py::TestComplianceCheckEndpoint -v

# Run specific test method
pytest tests/test_api_endpoints.py::TestComplianceCheckEndpoint::test_compliance_check_success -v
```

### Frontend Tests

```bash
# Run all frontend tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage --watchAll=false

# Run specific test file
npm test -- App.test.js

# Run in watch mode
npm test -- --watch
```

### E2E Browser Tests

```bash
# Run all E2E tests
cd e2e
npx playwright test

# Run specific browser
npx playwright test --project=chromium

# Run with UI mode
npx playwright test --ui

# Run with headed mode (visible browser)
npx playwright test --headed

# Run specific test file
npx playwright test compliance-checker.spec.js

# Run specific test
npx playwright test -g "should submit compliance check successfully"
```

### Performance Tests

```bash
# Run performance tests
cd performance
locust -f locustfile.py --host=http://localhost:8000

# Run with specific parameters
locust -f locustfile.py --host=http://localhost:8000 --users=10 --spawn-rate=2 --run-time=60s --headless

# Run with web UI
locust -f locustfile.py --host=http://localhost:8000 --web-host=0.0.0.0 --web-port=8089
```

### Security Tests

```bash
# Install security tools
pip install bandit safety

# Run security scan
cd backend
bandit -r app/ -f json -o security-report.json

# Check for known vulnerabilities
safety check --json --output security-vulnerabilities.json
```

## Test Categories

### 1. Backend API Tests

**Location**: `backend/tests/`

**Coverage**:
- API endpoint functionality
- Request/response validation
- Error handling
- Service layer integration
- Database operations
- Authentication and authorization

**Key Test Files**:
- `test_api_endpoints.py`: API endpoint tests
- `test_services.py`: Service layer tests
- `conftest.py`: Test configuration and fixtures

### 2. Frontend Component Tests

**Location**: `frontend/src/__tests__/`

**Coverage**:
- Component rendering
- User interactions
- State management
- API integration
- Accessibility
- Responsive design

**Key Test Files**:
- `App.test.js`: Main application tests
- `setupTests.js`: Test configuration

### 3. E2E Browser Tests

**Location**: `e2e/tests/`

**Coverage**:
- Complete user journeys
- Cross-browser compatibility
- Mobile responsiveness
- Real API integration
- Performance under load
- Visual regression testing

**Key Test Files**:
- `compliance-checker.spec.js`: Main E2E test scenarios

### 4. Performance Tests

**Location**: `performance/`

**Coverage**:
- API response times
- Concurrent user handling
- Database performance
- Memory usage
- CPU utilization
- Scalability testing

**Key Files**:
- `locustfile.py`: Performance test scenarios

### 5. Security Tests

**Coverage**:
- Code vulnerability scanning
- Dependency security
- Input validation
- Authentication bypass
- Data exposure risks

## CI/CD Integration

The testing suite is integrated with GitHub Actions for automated testing on:

- **Push to main/develop branches**
- **Pull requests**
- **Scheduled daily runs**

### CI/CD Pipeline Jobs

1. **Backend Tests**: API and service layer testing
2. **Frontend Tests**: Component and integration testing
3. **E2E Browser Tests**: Full browser automation
4. **Performance Tests**: Load and stress testing
5. **Security Tests**: Vulnerability scanning
6. **Test Summary**: Consolidated results and reporting

### Local CI/CD Simulation

```bash
# Run the complete test suite locally
./scripts/run-all-tests.sh

# Run specific test categories
./scripts/run-backend-tests.sh
./scripts/run-frontend-tests.sh
./scripts/run-e2e-tests.sh
./scripts/run-performance-tests.sh
```

## Troubleshooting

### Common Issues

#### Backend Tests

**Issue**: Database connection errors
```bash
# Solution: Ensure PostgreSQL is running
docker-compose up -d postgres
```

**Issue**: Import errors
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
```

#### Frontend Tests

**Issue**: Jest configuration errors
```bash
# Solution: Clear Jest cache
npm test -- --clearCache
```

**Issue**: Component rendering errors
```bash
# Solution: Check for missing dependencies
npm install
```

#### E2E Tests

**Issue**: Playwright browser installation
```bash
# Solution: Reinstall browsers
npx playwright install --with-deps
```

**Issue**: Test timeouts
```bash
# Solution: Increase timeout in playwright.config.js
timeout: 60000
```

#### Performance Tests

**Issue**: Locust connection errors
```bash
# Solution: Ensure backend server is running
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Debug Mode

#### Backend Debug
```bash
# Run with debug logging
pytest tests/ -v -s --log-cli-level=DEBUG
```

#### Frontend Debug
```bash
# Run with debug output
npm test -- --verbose --no-coverage
```

#### E2E Debug
```bash
# Run with debug mode
npx playwright test --debug
```

## Best Practices

### Test Development

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear, descriptive test names
3. **Arrange-Act-Assert**: Follow AAA pattern for test structure
4. **Mock External Dependencies**: Avoid external API calls in unit tests
5. **Test Data Management**: Use fixtures and factories for test data

### Test Maintenance

1. **Regular Updates**: Keep test dependencies updated
2. **Test Coverage**: Maintain high test coverage (>80%)
3. **Performance Monitoring**: Track test execution times
4. **Flaky Test Detection**: Identify and fix unreliable tests
5. **Documentation**: Keep test documentation current

### CI/CD Best Practices

1. **Fast Feedback**: Keep test execution times under 10 minutes
2. **Parallel Execution**: Run independent tests in parallel
3. **Artifact Management**: Store and version test artifacts
4. **Failure Analysis**: Provide clear failure information
5. **Rollback Strategy**: Have rollback procedures for failed deployments

### Security Testing

1. **Regular Scans**: Run security scans on every build
2. **Dependency Updates**: Keep dependencies updated
3. **Vulnerability Tracking**: Track and address security issues
4. **Access Control**: Test authentication and authorization
5. **Data Protection**: Verify sensitive data handling

## Test Data Management

### Test Fixtures

```python
# Backend fixtures (conftest.py)
@pytest.fixture
def sample_compliance_query():
    return ComplianceQuery(
        concern="Data privacy compliance",
        context="Customer data processing"
    )

# Frontend fixtures
const mockApiResponse = {
    status: 'compliant',
    confidence: 0.85,
    explanation: 'Test explanation'
};
```

### Test Data Cleanup

```bash
# Clean up test data
./scripts/cleanup-test-data.sh

# Reset test database
docker-compose down
docker-compose up -d postgres
```

## Monitoring and Reporting

### Test Metrics

- **Test Coverage**: Track code coverage percentages
- **Execution Time**: Monitor test performance
- **Failure Rate**: Track test reliability
- **Flaky Tests**: Identify unstable tests
- **Resource Usage**: Monitor CPU and memory usage

### Reporting Tools

- **Coverage Reports**: HTML and XML coverage reports
- **Test Results**: JUnit XML test results
- **Performance Reports**: Locust HTML reports
- **Security Reports**: Bandit and Safety JSON reports
- **E2E Reports**: Playwright HTML reports

### Continuous Monitoring

```bash
# Set up monitoring dashboard
./scripts/setup-monitoring.sh

# View test metrics
./scripts/view-metrics.sh
```

## Conclusion

This comprehensive E2E testing suite ensures the reliability, performance, and security of the RegReportRAG application. Regular execution of these tests helps maintain code quality and provides confidence in the application's functionality.

For additional support or questions, please refer to the project documentation or contact the development team. 