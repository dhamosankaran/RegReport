-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create database if it doesn't exist
-- (This is handled by Docker environment variables)

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE rag_system TO postgres;

-- Set search path
SET search_path TO public; 