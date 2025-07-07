# RAG System Deployment Guide

## Development Environment (Local)

### Quick Start
```bash
# 1. Set environment variable
export OPENAI_API_KEY="your-openai-api-key-here"

# 2. Make script executable and run
chmod +x start_rag_system.sh
./start_rag_system.sh
```

### Manual Development Setup
```bash
# 1. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Frontend setup  
cd ../frontend
npm install

# 3. Start services
# Terminal 1: Backend
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm start
```

---

## Production Environment

### Docker Deployment

#### 1. Create Dockerfile for Backend
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create Dockerfile for Frontend
```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
      - ./Instructions.pdf:/app/Instructions.pdf
      - ./Rules.pdf:/app/Rules.pdf
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    depends_on:
      - backend

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=rag_system
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
```

### Kubernetes Deployment

#### 1. Backend Deployment
```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-backend
  template:
    metadata:
      labels:
        app: rag-backend
    spec:
      containers:
      - name: backend
        image: rag-system/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: CHROMADB_PERSIST_DIR
          value: "/app/data/chromadb"
        volumeMounts:
        - name: documents
          mountPath: /app/documents
        - name: data
          mountPath: /app/data
      volumes:
      - name: documents
        configMap:
          name: regulatory-documents
      - name: data
        persistentVolumeClaim:
          claimName: chromadb-pvc
```

#### 2. Frontend Deployment
```yaml
# k8s/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rag-frontend
  template:
    metadata:
      labels:
        app: rag-frontend
    spec:
      containers:
      - name: frontend
        image: rag-system/frontend:latest
        ports:
        - containerPort: 80
        env:
        - name: REACT_APP_API_URL
          value: "https://api.yourdomain.com"
```

---

## Cloud Deployment Options

### AWS Deployment

#### 1. ECS with Fargate
```json
{
  "family": "rag-backend-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "rag-backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/rag-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/rag-backend",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 2. Lambda + API Gateway (Serverless)
```python
# lambda_handler.py
import json
from mangum import Mangum
from app.main import app

handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    return handler(event, context)
```

### Google Cloud Deployment

#### Cloud Run Configuration
```yaml
# cloudrun.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: rag-backend
  annotations:
    run.googleapis.com/client-name: cloud-console
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-environment: gen2
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: gcr.io/project-id/rag-backend
        ports:
        - name: http1
          containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              key: api-key
              name: openai-secret
        resources:
          limits:
            cpu: "2"
            memory: "4Gi"
```

---

## Environment Configuration

### Production Environment Variables
```bash
# Backend
OPENAI_API_KEY=your-production-api-key
CHROMADB_PERSIST_DIR=/app/data/chromadb
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
CORS_ORIGINS=["https://yourdomain.com"]

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

### SSL/TLS Configuration

#### Nginx Configuration
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/yourdomain.com.crt;
    ssl_certificate_key /etc/ssl/private/yourdomain.com.key;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring & Logging

### Application Monitoring
```python
# backend/app/monitoring.py
import logging
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
compliance_checks = Counter('compliance_checks_total', 'Total compliance checks')
response_time = Histogram('response_time_seconds', 'Response time')

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response_time.observe(process_time)
    return response
```

### Logging Configuration
```python
# backend/app/logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "json": {
            "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "json",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## Security Considerations

### Production Security Checklist
- [ ] Enable HTTPS/TLS encryption
- [ ] Implement API rate limiting
- [ ] Secure API key storage (environment variables/secrets)
- [ ] Input validation and sanitization
- [ ] CORS policy configuration
- [ ] Regular security updates
- [ ] Network security groups/firewalls
- [ ] Data encryption at rest
- [ ] Access logging and monitoring
- [ ] Vulnerability scanning

### API Security
```python
# backend/app/security.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != os.getenv("API_SECRET_TOKEN"):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    return credentials.credentials
```

---

## Scaling Considerations

### Horizontal Scaling
- Load balancer configuration
- Database connection pooling
- Stateless application design
- Caching strategies (Redis)
- CDN for frontend assets

### Performance Optimization
- Async/await throughout the stack
- Connection pooling for databases
- Caching of embeddings and results
- Batch processing for document updates
- Background task processing

### Cost Optimization
- Use OpenAI API efficiently (batch requests)
- Implement caching to reduce API calls
- Monitor and optimize resource usage
- Use spot instances for non-critical workloads 