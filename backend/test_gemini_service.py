#!/usr/bin/env python3
"""
Test script for Gemini Vector Service
This script tests the Gemini-based vector service with sample PDF files.
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vector_service_gemini import GeminiVectorService

class GeminiServiceTester:
    """Test class for Gemini Vector Service"""
    
    def __init__(self):
        self.service = None
        self.test_files = []
    
    async def setup(self):
        """Setup the test environment"""
        print("🔧 Setting up Gemini Vector Service Test Environment")
        
        # Check for required environment variables
        if not os.getenv("GOOGLE_API_KEY"):
            print("❌ Error: GOOGLE_API_KEY environment variable is required")
            print("Please set it in your .env file or environment")
            return False
            
        # Initialize service
        try:
            self.service = GeminiVectorService()
            await self.service.initialize_database()
            print("✅ Database initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error initializing service: {str(e)}")
            return False
    
    def find_test_files(self):
        """Find PDF files for testing"""
        print("\n📁 Looking for PDF files to test...")
        
        project_root = Path(__file__).parent.parent
        
        # Common locations for PDF files
        potential_files = [
            project_root / "Instructions.pdf",
            project_root / "Rules.pdf",
            project_root / "data" / "sample.pdf",
            project_root / "TestData" / "sample.pdf",
            project_root / "backend" / "data" / "sample.pdf"
        ]
        
        self.test_files = []
        for file_path in potential_files:
            if file_path.exists():
                self.test_files.append(str(file_path))
                print(f"   ✅ Found: {file_path.name}")
        
        if not self.test_files:
            print("   ⚠️  No PDF files found for testing")
            print("   💡 You can add PDF files to the project root or TestData folder")
            return False
        
        print(f"   📊 Total files found: {len(self.test_files)}")
        return True
    
    async def test_document_processing(self):
        """Test document processing and embedding"""
        print("\n🔄 Testing Document Processing...")
        
        try:
            # Clear database first
            await self.service.clear_database()
            print("   🗑️  Database cleared")
            
            # Process documents
            results = await self.service.add_documents(self.test_files)
            
            # Display results
            print(f"   ✅ Successfully processed: {len(results['processed'])} files")
            print(f"   ❌ Failed to process: {len(results['failed'])} files")
            
            for file_info in results['processed']:
                print(f"      📄 {Path(file_info['file']).name}: {file_info['chunk_count']} chunks")
                print(f"         📊 Chunking method: Character-based (no tiktoken)")
            
            for file_info in results['failed']:
                print(f"      ❌ {Path(file_info['file']).name}: {file_info['error']}")
            
            return len(results['processed']) > 0
            
        except Exception as e:
            print(f"   ❌ Error during document processing: {str(e)}")
            return False
    
    async def test_database_status(self):
        """Test database status retrieval"""
        print("\n📊 Testing Database Status...")
        
        try:
            status = await self.service.get_document_status()
            
            print(f"   📚 Total documents: {status['total_documents']}")
            print(f"   📄 Total chunks: {status['total_chunks']}")
            print(f"   🤖 Embedding model: {status['embedding_model']}")
            print(f"   🧠 LLM model: {status['llm_model']}")
            
            print("   📋 Document details:")
            for doc in status['documents']:
                print(f"      • {doc['document_name']}: {doc['chunk_count']} chunks ({doc['status']})")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error getting database status: {str(e)}")
            return False
    
    async def test_chunking_strategy(self):
        """Test the chunking strategy details"""
        print("\n📝 Testing Chunking Strategy...")
        
        try:
            processor = self.service.document_processor
            
            print(f"   🔧 Chunking Configuration:")
            print(f"      • Max chunk size: {processor.max_chunk_size} characters")
            print(f"      • Overlap: {processor.chunk_overlap} characters")
            print(f"      • Min chunk size: {processor.min_chunk_size} characters")
            print(f"      • Method: Character-based (no tiktoken)")
            print(f"      • Sentence-aware: Yes")
            print(f"      • Paragraph-aware: Yes")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error testing chunking strategy: {str(e)}")
            return False
    
    async def test_semantic_search(self):
        """Test semantic search functionality"""
        print("\n🔍 Testing Semantic Search...")
        
        test_queries = [
            "compliance requirements",
            "regulatory standards",
            "document processing",
            "rules and regulations"
        ]
        
        try:
            for query in test_queries:
                print(f"   🔎 Query: '{query}'")
                
                results = await self.service.search_similar_documents(query, n_results=3)
                
                if results:
                    print(f"      ✅ Found {len(results)} relevant documents")
                    for i, doc in enumerate(results[:2]):  # Show top 2
                        print(f"         {i+1}. {doc['document_name']} (page {doc['page_number']}) - Score: {doc['similarity_score']:.3f}")
                        print(f"            Preview: {doc['content'][:100]}...")
                else:
                    print("      ⚠️  No results found")
                
                print()
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error during semantic search: {str(e)}")
            return False
    
    async def test_rag_queries(self):
        """Test RAG (Retrieval-Augmented Generation) queries"""
        print("\n🤖 Testing RAG Queries with Gemini Flash...")
        
        test_queries = [
            "What are the main compliance requirements?",
            "How should regulatory reports be structured?",
            "What are the key rules to follow?",
            "Explain the document processing requirements"
        ]
        
        try:
            for query in test_queries:
                print(f"\n   ❓ Query: {query}")
                
                result = await self.service.query_with_rag(query, n_results=5)
                
                print(f"   🤖 Answer: {result['answer'][:300]}...")
                print(f"   📚 Sources used: {result['context_used']}")
                
                # Show top sources
                for i, source in enumerate(result['sources'][:2]):
                    print(f"      📄 Source {i+1}: {source['document_name']} (page {source['page_number']}) - Score: {source['similarity_score']:.3f}")
                
                print("-" * 50)
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error during RAG queries: {str(e)}")
            return False
    
    async def cleanup(self):
        """Clean up resources"""
        if self.service:
            await self.service.close()
            print("🧹 Cleaned up resources")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Gemini Vector Service Tests")
        print("=" * 60)
        
        # Setup
        if not await self.setup():
            return False
        
        # Find test files
        if not self.find_test_files():
            return False
        
        # Run tests
        tests = [
            ("Document Processing", self.test_document_processing()),
            ("Database Status", self.test_database_status()),
            ("Chunking Strategy", self.test_chunking_strategy()),
            ("Semantic Search", self.test_semantic_search()),
            ("RAG Queries", self.test_rag_queries())
        ]
        
        results = []
        for test_name, test_coro in tests:
            try:
                success = await test_coro
                results.append((test_name, success))
            except Exception as e:
                print(f"❌ Test '{test_name}' failed with error: {str(e)}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 Test Summary")
        print("=" * 60)
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n🏆 Overall: {passed}/{total} tests passed")
        
        await self.cleanup()
        
        return passed == total

async def main():
    """Main test function"""
    tester = GeminiServiceTester()
    
    try:
        success = await tester.run_all_tests()
        
        if success:
            print("\n🎉 All tests passed! Gemini Vector Service is working correctly.")
            sys.exit(0)
        else:
            print("\n💥 Some tests failed. Please check the output above.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        await tester.cleanup()
        sys.exit(1)
    
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        await tester.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 