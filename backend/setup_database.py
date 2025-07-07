#!/usr/bin/env python3
"""
Database setup script for PostgreSQL with pgvector extension
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Setup PostgreSQL database with pgvector extension"""
    
    # Get database connection details
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "rag_system")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    
    # Create database URL
    database_url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            print(f"✅ Connected to PostgreSQL at {host}:{port}")
            
            # Enable pgvector extension
            print("📦 Enabling pgvector extension...")
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            print("✅ pgvector extension enabled")
            
            # Create tables
            print("🏗️  Creating database tables...")
            from app.models.database import Base
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created")
            
            # Verify setup
            result = conn.execute(text("SELECT version()"))
            pg_version = result.fetchone()[0]
            print(f"📊 PostgreSQL version: {pg_version}")
            
            # Check pgvector
            result = conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector'"))
            if result.fetchone():
                print("✅ pgvector extension is active")
            else:
                print("❌ pgvector extension not found")
                return False
                
        print("\n🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        print("\n📋 Troubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Verify your database credentials in .env file")
        print("3. Ensure pgvector extension is installed in PostgreSQL")
        print("4. Check if the database 'rag_system' exists")
        return False

if __name__ == "__main__":
    print("🚀 Setting up PostgreSQL database with pgvector...")
    print("=" * 50)
    
    success = setup_database()
    
    if success:
        print("\n✅ Setup completed! You can now run the application.")
        sys.exit(0)
    else:
        print("\n❌ Setup failed! Please check the error messages above.")
        sys.exit(1) 