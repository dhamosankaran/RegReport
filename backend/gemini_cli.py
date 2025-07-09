#!/usr/bin/env python3
"""
Gemini Vector Service CLI - Command Line Interface for Testing
Provides easy-to-use commands for loading documents and retrieving information
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add the backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_service_gemini import GeminiVectorService

class GeminiCLI:
    """Command Line Interface for Gemini Vector Service"""
    
    def __init__(self):
        self.service = None
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'purple': '\033[95m',
            'cyan': '\033[96m',
            'bold': '\033[1m',
            'end': '\033[0m'
        }
    
    def print_colored(self, text: str, color: str = 'end'):
        """Print colored text"""
        print(f"{self.colors.get(color, '')}{text}{self.colors['end']}")
    
    def print_header(self, title: str):
        """Print a formatted header"""
        self.print_colored("=" * 60, 'cyan')
        self.print_colored(f" {title} ", 'bold')
        self.print_colored("=" * 60, 'cyan')
    
    def print_success(self, message: str):
        """Print success message"""
        self.print_colored(f"✅ {message}", 'green')
    
    def print_error(self, message: str):
        """Print error message"""
        self.print_colored(f"❌ {message}", 'red')
    
    def print_warning(self, message: str):
        """Print warning message"""
        self.print_colored(f"⚠️  {message}", 'yellow')
    
    def print_info(self, message: str):
        """Print info message"""
        self.print_colored(f"ℹ️  {message}", 'blue')
    
    async def initialize_service(self):
        """Initialize the Gemini Vector Service"""
        try:
            self.print_info("Initializing Gemini Vector Service...")
            
            # Check for API key
            if not os.getenv("GOOGLE_API_KEY"):
                self.print_error("GOOGLE_API_KEY environment variable is required")
                self.print_info("Please set it in your .env file or environment")
                return False
            
            self.service = GeminiVectorService()
            await self.service.initialize_database()
            
            self.print_success("Service initialized successfully")
            self.print_info(f"Embedding model: {self.service.embedding_model}")
            self.print_info(f"LLM model: {self.service.llm_model}")
            self.print_info(f"Chunking: Character-based (no tiktoken)")
            
            return True
            
        except Exception as e:
            self.print_error(f"Failed to initialize service: {str(e)}")
            return False
    
    async def load_documents(self, file_paths: List[str], show_chunks: bool = False):
        """Load documents into the vector database"""
        self.print_header("LOADING DOCUMENTS")
        
        if not file_paths:
            self.print_warning("No file paths provided")
            return
        
        # Validate files
        valid_files = []
        for file_path in file_paths:
            path = Path(file_path)
            if path.exists() and path.suffix.lower() == '.pdf':
                valid_files.append(str(path))
                self.print_info(f"Found: {path.name}")
            else:
                self.print_warning(f"Skipping: {file_path} (not found or not PDF)")
        
        if not valid_files:
            self.print_error("No valid PDF files found")
            return
        
        self.print_info(f"Processing {len(valid_files)} PDF files...")
        
        try:
            # Process documents
            results = await self.service.add_documents(valid_files)
            
            # Display results
            self.print_colored("\n📊 Processing Results:", 'bold')
            self.print_success(f"Successfully processed: {len(results['processed'])} files")
            
            if results['failed']:
                self.print_error(f"Failed to process: {len(results['failed'])} files")
            
            # Show details for each file
            for file_info in results['processed']:
                file_name = Path(file_info['file']).name
                chunk_count = file_info['chunk_count']
                self.print_colored(f"  📄 {file_name}: {chunk_count} chunks", 'green')
                
                if show_chunks:
                    # Show chunk details if requested
                    self.print_info(f"     Chunking method: Character-based (4000 chars max)")
            
            for file_info in results['failed']:
                file_name = Path(file_info['file']).name
                error = file_info['error']
                self.print_colored(f"  ❌ {file_name}: {error}", 'red')
            
        except Exception as e:
            self.print_error(f"Error loading documents: {str(e)}")
    
    async def query_documents(self, query: str, max_results: int = 10, show_sources: bool = True):
        """Query documents using RAG"""
        self.print_header("QUERYING DOCUMENTS")
        
        self.print_info(f"Query: {query}")
        self.print_info(f"Max results: {max_results}")
        
        try:
            # Perform RAG query
            result = await self.service.query_with_rag(query, n_results=max_results)
            
            # Display answer
            self.print_colored("\n🤖 AI Answer:", 'bold')
            self.print_colored("-" * 40, 'cyan')
            print(result['answer'])
            self.print_colored("-" * 40, 'cyan')
            
            # Display sources
            if show_sources and result['sources']:
                self.print_colored(f"\n📚 Sources ({result['context_used']} documents used):", 'bold')
                
                for i, source in enumerate(result['sources'][:5], 1):
                    score = source['similarity_score']
                    doc_name = source['document_name']
                    page_num = source['page_number']
                    preview = source['content_preview']
                    
                    self.print_colored(f"\n  📄 Source {i}: {doc_name} (Page {page_num})", 'blue')
                    self.print_colored(f"     Similarity: {score:.3f}", 'yellow')
                    self.print_colored(f"     Preview: {preview}", 'purple')
            
        except Exception as e:
            self.print_error(f"Error querying documents: {str(e)}")
    
    async def search_similar(self, query: str, max_results: int = 5):
        """Search for similar documents without generating answer"""
        self.print_header("SEMANTIC SEARCH")
        
        self.print_info(f"Search query: {query}")
        
        try:
            results = await self.service.search_similar_documents(query, n_results=max_results)
            
            if not results:
                self.print_warning("No similar documents found")
                return
            
            self.print_colored(f"\n🔍 Found {len(results)} similar documents:", 'bold')
            
            for i, doc in enumerate(results, 1):
                score = doc['similarity_score']
                doc_name = doc['document_name']
                page_num = doc['page_number']
                content = doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
                
                self.print_colored(f"\n  🎯 Result {i}: {doc_name} (Page {page_num})", 'blue')
                self.print_colored(f"     Similarity Score: {score:.3f}", 'yellow')
                self.print_colored(f"     Content: {content}", 'purple')
            
        except Exception as e:
            self.print_error(f"Error searching documents: {str(e)}")
    
    async def show_status(self):
        """Show database status and loaded documents"""
        self.print_header("DATABASE STATUS")
        
        try:
            status = await self.service.get_document_status()
            
            self.print_colored(f"📊 Database Overview:", 'bold')
            self.print_info(f"Total documents: {status['total_documents']}")
            self.print_info(f"Total chunks: {status['total_chunks']}")
            self.print_info(f"Embedding model: {status['embedding_model']}")
            self.print_info(f"LLM model: {status['llm_model']}")
            
            if status['documents']:
                self.print_colored(f"\n📋 Loaded Documents:", 'bold')
                for doc in status['documents']:
                    doc_name = doc['document_name']
                    chunk_count = doc['chunk_count']
                    doc_status = doc['status']
                    
                    status_color = 'green' if doc_status == 'loaded' else 'red'
                    self.print_colored(f"  📄 {doc_name}: {chunk_count} chunks ({doc_status})", status_color)
            else:
                self.print_warning("No documents loaded")
            
        except Exception as e:
            self.print_error(f"Error getting status: {str(e)}")
    
    async def clear_database(self, confirm: bool = False):
        """Clear all documents from database"""
        self.print_header("CLEAR DATABASE")
        
        if not confirm:
            self.print_warning("This will delete ALL documents and chunks from the database")
            response = input("Are you sure? Type 'yes' to confirm: ")
            if response.lower() != 'yes':
                self.print_info("Operation cancelled")
                return
        
        try:
            await self.service.clear_database()
            self.print_success("Database cleared successfully")
            
        except Exception as e:
            self.print_error(f"Error clearing database: {str(e)}")
    
    async def interactive_mode(self):
        """Run in interactive mode"""
        self.print_header("INTERACTIVE MODE")
        self.print_info("Type 'help' for available commands, 'quit' to exit")
        
        while True:
            try:
                command = input(f"\n{self.colors['cyan']}gemini> {self.colors['end']}").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    self.print_info("Goodbye!")
                    break
                
                elif command.lower() == 'help':
                    self.show_interactive_help()
                
                elif command.lower() == 'status':
                    await self.show_status()
                
                elif command.lower() == 'clear':
                    await self.clear_database()
                
                elif command.startswith('load '):
                    file_path = command[5:].strip()
                    if file_path:
                        await self.load_documents([file_path])
                    else:
                        self.print_error("Please provide a file path")
                
                elif command.startswith('query '):
                    query = command[6:].strip()
                    if query:
                        await self.query_documents(query)
                    else:
                        self.print_error("Please provide a query")
                
                elif command.startswith('search '):
                    query = command[7:].strip()
                    if query:
                        await self.search_similar(query)
                    else:
                        self.print_error("Please provide a search query")
                
                else:
                    self.print_warning(f"Unknown command: {command}")
                    self.print_info("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                self.print_info("\nGoodbye!")
                break
            except Exception as e:
                self.print_error(f"Error: {str(e)}")
    
    def show_interactive_help(self):
        """Show help for interactive mode"""
        self.print_colored("\n📖 Available Commands:", 'bold')
        commands = [
            ("help", "Show this help message"),
            ("status", "Show database status and loaded documents"),
            ("load <file.pdf>", "Load a PDF file into the database"),
            ("query <question>", "Ask a question using RAG"),
            ("search <text>", "Search for similar documents"),
            ("clear", "Clear all documents from database"),
            ("quit", "Exit interactive mode")
        ]
        
        for cmd, desc in commands:
            self.print_colored(f"  {cmd:<20} - {desc}", 'blue')
    
    async def cleanup(self):
        """Clean up resources"""
        if self.service:
            await self.service.close()

async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Gemini Vector Service CLI - Load documents and query with AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load documents
  python gemini_cli.py load file1.pdf file2.pdf
  
  # Query documents
  python gemini_cli.py query "What are the compliance requirements?"
  
  # Search similar content
  python gemini_cli.py search "regulatory standards"
  
  # Show status
  python gemini_cli.py status
  
  # Interactive mode
  python gemini_cli.py interactive
  
  # Clear database
  python gemini_cli.py clear
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load PDF documents')
    load_parser.add_argument('files', nargs='+', help='PDF files to load')
    load_parser.add_argument('--show-chunks', action='store_true', help='Show chunk details')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Query documents using RAG')
    query_parser.add_argument('question', help='Question to ask')
    query_parser.add_argument('--max-results', type=int, default=10, help='Maximum results to retrieve')
    query_parser.add_argument('--no-sources', action='store_true', help='Hide source information')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for similar documents')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-results', type=int, default=5, help='Maximum results to show')
    
    # Status command
    subparsers.add_parser('status', help='Show database status')
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear database')
    clear_parser.add_argument('--yes', action='store_true', help='Skip confirmation')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = GeminiCLI()
    
    try:
        # Initialize service
        if not await cli.initialize_service():
            return
        
        # Execute command
        if args.command == 'load':
            await cli.load_documents(args.files, args.show_chunks)
        
        elif args.command == 'query':
            await cli.query_documents(args.question, args.max_results, not args.no_sources)
        
        elif args.command == 'search':
            await cli.search_similar(args.query, args.max_results)
        
        elif args.command == 'status':
            await cli.show_status()
        
        elif args.command == 'clear':
            await cli.clear_database(args.yes)
        
        elif args.command == 'interactive':
            await cli.interactive_mode()
    
    except KeyboardInterrupt:
        cli.print_info("\nOperation cancelled by user")
    
    except Exception as e:
        cli.print_error(f"Unexpected error: {str(e)}")
    
    finally:
        await cli.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 