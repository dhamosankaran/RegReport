#!/bin/bash

# Regulatory Compliance RAG System Startup Script

set -e

echo "🚀 Starting Regulatory Compliance RAG System"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Python is installed
print_header "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_status "Python version: $PYTHON_VERSION"

# Check if Node.js is installed
print_header "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

NODE_VERSION=$(node --version)
print_status "Node.js version: $NODE_VERSION"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm."
    exit 1
fi

NPM_VERSION=$(npm --version)
print_status "npm version: $NPM_VERSION"

# Check if required files exist
print_header "Checking required files..."
if [ ! -f "Instructions.pdf" ]; then
    print_error "Instructions.pdf not found in the root directory."
    exit 1
fi

if [ ! -f "Rules.pdf" ]; then
    print_error "Rules.pdf not found in the root directory."
    exit 1
fi

print_status "Required PDF files found"

# Check for OpenAI API key
print_header "Checking environment variables..."
if [ -f "backend/.env" ]; then
    print_status "Found .env file in backend directory"
    # Check if OPENAI_API_KEY is set in the file
    if grep -q "OPENAI_API_KEY=" backend/.env; then
        print_status "OpenAI API key found in .env file"
    else
        print_warning "OPENAI_API_KEY not found in backend/.env file"
        echo "Please add your OpenAI API key to backend/.env file:"
        echo "OPENAI_API_KEY=your-api-key-here"
    fi
elif [ -z "$OPENAI_API_KEY" ]; then
    print_warning "No .env file found and OPENAI_API_KEY environment variable not set."
    echo "Please either:"
    echo "1. Create backend/.env file with your OpenAI API key, or"
    echo "2. Set the environment variable: export OPENAI_API_KEY='your-api-key-here'"
    exit 1
else
    print_status "OpenAI API key is set from environment variable"
fi

# Setup Python virtual environment
print_header "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_status "Virtual environment already exists"
fi

print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_header "Installing Python dependencies..."
pip install -r backend/requirements.txt
if [ $? -eq 0 ]; then
    print_status "Python dependencies installed successfully"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Setup PostgreSQL database
print_header "Setting up PostgreSQL database..."
cd backend
python setup_database.py
if [ $? -eq 0 ]; then
    print_status "Database setup completed"
else
    print_warning "Database setup failed. Please ensure PostgreSQL is running with pgvector extension."
    echo "You can manually run: cd backend && python setup_database.py"
fi
cd ..

# Create data directory for logs
print_header "Setting up data directory..."
mkdir -p data/logs
print_status "Data directory created"

# Setup environment file
print_header "Setting up environment configuration..."
if [ ! -f "backend/.env" ]; then
    cat > backend/.env << EOF
# OpenAI API Configuration
# Set your OpenAI API key here or use environment variable OPENAI_API_KEY
OPENAI_API_KEY=${OPENAI_API_KEY}

# PostgreSQL Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
EOF
    print_status "Environment file created"
    if [ -z "$OPENAI_API_KEY" ]; then
        print_warning "Please add your OpenAI API key to backend/.env file"
    fi
else
    print_status "Environment file already exists"
    # Only update if API key is provided and not already in file
    if [ ! -z "$OPENAI_API_KEY" ] && ! grep -q "OPENAI_API_KEY=" backend/.env; then
        echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> backend/.env
        print_status "Added OpenAI API key to existing environment file"
    fi
    # Add PostgreSQL config if not present
    if ! grep -q "POSTGRES_HOST=" backend/.env; then
        cat >> backend/.env << EOF

# PostgreSQL Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
EOF
        print_status "Added PostgreSQL configuration to existing environment file"
    fi
fi

# Install Node.js dependencies
print_header "Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Function to cleanup on exit
cleanup() {
    print_header "Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then
        print_status "Stopping backend server (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        print_status "Stopping frontend server (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    print_status "Cleanup complete"
}

# Set trap for cleanup
trap cleanup EXIT

# Start backend server
print_header "Starting FastAPI backend server..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

print_status "Backend server started (PID: $BACKEND_PID)"
print_status "Backend URL: http://localhost:8000"

# Wait for backend to start
print_status "Waiting for backend server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Backend server is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Backend server failed to start within 30 seconds"
        exit 1
    fi
    sleep 1
done

# Start frontend server
print_header "Starting React frontend server..."
cd frontend
REACT_APP_API_URL=http://localhost:8000 npm start &
FRONTEND_PID=$!
cd ..

print_status "Frontend server started (PID: $FRONTEND_PID)"
print_status "Frontend URL: http://localhost:3000"

# Display startup completion message
echo ""
echo "🎉 Regulatory Compliance RAG System is now running!"
echo "=================================================="
echo ""
echo "📊 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "🔍 Features:"
echo "  • AI-powered compliance checking"
echo "  • Document processing with PostgreSQL + pgvector"
echo "  • Real-time regulatory analysis"
echo "  • Interactive web interface"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait 
