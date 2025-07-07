#!/usr/bin/env python3
"""
Standalone script to load PDF files into the vector database
This script can be run independently to process and store PDF documents
without starting the full FastAPI application.

Usage:
    python load_pdfs_to_vector_db.py
    
    # Or with custom PDF files
    python load_pdfs_to_vector_db.py --pdf-files path/to/file1.pdf path/to/file2.pdf
    
    # Or to reload existing documents
    python load_pdfs_to_vector_db.py --reload
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
load_dotenv()

# Import after path setup
from app.services.vector_service import PostgreSQLVectorService
from app.services.document_processor import DocumentProcessor
from app.utils.logging_config import setup_logging, get_logger

# Setup logging
setup_logging(log_level="INFO", log_dir="logs")
logger = get_logger("pdf_loader")

class PDFLoader:
    def __init__(self):
        self.vector_service = None
        self.document_processor = None
    
    async def initialize(self):
        """Initialize the vector service and document processor"""
        try:
            logger.info("Initializing PDF loader...")
            
            # Initialize vector service
            self.vector_service = PostgreSQLVectorService()
            await self.vector_service.initialize_database()
            
            # Initialize document processor
            self.document_processor = DocumentProcessor()
            
            logger.info("PDF loader initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize PDF loader: {str(e)}")
            raise
    
    async def load_default_pdfs(self):
        """Load the default PDF files (Instructions.pdf and Rules.pdf)"""
        try:
            # Get project root directory
            project_root = Path(__file__).parent.parent
            
            # Default PDF files
            default_pdfs = [
                project_root / "Instructions.pdf",
                project_root / "Rules.pdf"
            ]
            
            # Filter existing files
            existing_files = [str(pdf) for pdf in default_pdfs if pdf.exists()]
            
            if not existing_files:
                logger.warning("No default PDF files found in project root")
                logger.info("Expected files:")
                for pdf in default_pdfs:
                    logger.info(f"  - {pdf}")
                return False
            
            logger.info(f"Found {len(existing_files)} PDF files to process")
            for file in existing_files:
                logger.info(f"  - {file}")
            
            # Load the PDFs
            await self.load_pdfs(existing_files)
            return True
            
        except Exception as e:
            logger.error(f"Error loading default PDFs: {str(e)}")
            raise
    
    async def load_pdfs(self, pdf_files: List[str]):
        """Load specified PDF files into the vector database"""
        try:
            logger.info(f"Processing {len(pdf_files)} PDF files...")
            
            # Validate files exist
            for pdf_file in pdf_files:
                if not os.path.exists(pdf_file):
                    logger.error(f"PDF file not found: {pdf_file}")
                    return False
            
            # Process each PDF
            total_chunks = 0
            for i, pdf_file in enumerate(pdf_files, 1):
                logger.info(f"Processing PDF {i}/{len(pdf_files)}: {os.path.basename(pdf_file)}")
                
                # Check if already processed
                file_hash = self.vector_service._get_file_hash(pdf_file)
                doc_name = os.path.basename(pdf_file)
                
                # Check if document already exists with same hash
                with self.vector_service.SessionLocal() as db:
                    from app.models.database import DBDocumentChunk
                    existing = db.query(DBDocumentChunk).filter(
                        DBDocumentChunk.document_name == doc_name,
                        DBDocumentChunk.file_hash == file_hash
                    ).first()
                    
                    if existing:
                        chunk_count = db.query(DBDocumentChunk).filter(
                            DBDocumentChunk.document_name == doc_name
                        ).count()
                        logger.info(f"  ✅ Already processed: {doc_name} ({chunk_count} chunks)")
                        total_chunks += chunk_count
                        continue
                
                # Process the PDF
                result = await self.vector_service.add_documents([pdf_file])
                
                if result["processed"]:
                    chunk_count = result["processed"][0]["chunk_count"]
                    total_chunks += chunk_count
                    logger.info(f"  ✅ Processed: {doc_name} ({chunk_count} chunks)")
                else:
                    logger.error(f"  ❌ Failed to process: {doc_name}")
                    if result["failed"]:
                        logger.error(f"    Error: {result['failed'][0]['error']}")
            
            logger.info(f"🎉 PDF loading completed! Total chunks: {total_chunks}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading PDFs: {str(e)}")
            raise
    
    async def reload_all_documents(self):
        """Reload all documents (clear existing and reprocess)"""
        try:
            logger.info("Reloading all documents...")
            await self.vector_service.reload_documents()
            logger.info("🎉 All documents reloaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error reloading documents: {str(e)}")
            raise
    
    async def get_status(self):
        """Get current document status"""
        try:
            status = await self.vector_service.get_document_status()
            
            logger.info("📊 Current Document Status:")
            logger.info(f"  Total Documents: {status.total_documents}")
            logger.info(f"  Total Chunks: {status.total_chunks}")
            logger.info(f"  Last Refresh: {status.last_refresh}")
            
            logger.info("\n📋 Document Details:")
            for doc in status.documents:
                logger.info(f"  - {doc.document_name}: {doc.status} ({doc.chunk_count} chunks)")
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting document status: {str(e)}")
            raise
    
    async def close(self):
        """Close connections"""
        if self.vector_service:
            await self.vector_service.close()

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Load PDF files into vector database")
    parser.add_argument("--pdf-files", nargs="+", help="Specific PDF files to load")
    parser.add_argument("--reload", action="store_true", help="Reload all documents")
    parser.add_argument("--status", action="store_true", help="Show current document status")
    
    args = parser.parse_args()
    
    loader = PDFLoader()
    
    try:
        # Initialize the loader
        await loader.initialize()
        
        # Show status if requested
        if args.status:
            await loader.get_status()
            return
        
        # Reload all documents if requested
        if args.reload:
            await loader.reload_all_documents()
            await loader.get_status()
            return
        
        # Load specific PDF files if provided
        if args.pdf_files:
            logger.info(f"Loading custom PDF files: {args.pdf_files}")
            await loader.load_pdfs(args.pdf_files)
        else:
            # Load default PDFs
            logger.info("Loading default PDF files from project root...")
            await loader.load_default_pdfs()
        
        # Show final status
        await loader.get_status()
        
    except Exception as e:
        logger.error(f"Script failed: {str(e)}")
        sys.exit(1)
    finally:
        await loader.close()

if __name__ == "__main__":
    print("🚀 PDF to Vector Database Loader")
    print("=" * 50)
    
    asyncio.run(main()) 