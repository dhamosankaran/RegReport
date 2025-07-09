#!/usr/bin/env python3
"""
Demo script for Gemini Vector Service CLI
Demonstrates the complete workflow from setup to querying
"""

import subprocess
import time
import os
import sys

def run_command(command, description):
    """Run a command and display its output"""
    print(f"\n🔧 {description}")
    print("=" * 60)
    print(f"Command: {command}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def wait_for_user():
    """Wait for user to press Enter"""
    input("\n⏸️  Press Enter to continue...")

def main():
    """Run the complete CLI demonstration"""
    
    print("🚀 Gemini Vector Service CLI - Complete Demo")
    print("=" * 60)
    print("This demo will show you how to:")
    print("  1. Create test PDF files")
    print("  2. Load documents into the vector database")
    print("  3. Query documents using AI")
    print("  4. Search for similar content")
    print("  5. Check database status")
    
    # Check prerequisites
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n❌ Error: GOOGLE_API_KEY environment variable is required")
        print("Please set it before running this demo:")
        print("export GOOGLE_API_KEY='your-api-key-here'")
        return
    
    wait_for_user()
    
    # Step 1: Create test PDFs
    print("\n📋 STEP 1: Creating Test PDF Files")
    success = run_command("python create_test_pdfs.py", "Creating sample regulatory documents")
    if not success:
        print("❌ Failed to create test PDFs. Make sure reportlab is installed.")
        return
    
    wait_for_user()
    
    # Step 2: Check initial status
    print("\n📊 STEP 2: Checking Initial Database Status")
    run_command("python gemini_cli.py status", "Checking empty database")
    
    wait_for_user()
    
    # Step 3: Load documents
    print("\n📄 STEP 3: Loading Documents")
    run_command("python gemini_cli.py load *.pdf --show-chunks", "Loading all PDF files with chunk details")
    
    wait_for_user()
    
    # Step 4: Verify loading
    print("\n✅ STEP 4: Verifying Document Loading")
    run_command("python gemini_cli.py status", "Checking loaded documents")
    
    wait_for_user()
    
    # Step 5: Test queries
    print("\n🤖 STEP 5: Testing AI Queries (RAG)")
    
    queries = [
        "What are the main compliance requirements?",
        "How should risk management be structured?",
        "What are the data governance standards?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i}/3 ---")
        run_command(f'python gemini_cli.py query "{query}"', f"Asking: {query}")
        if i < len(queries):
            wait_for_user()
    
    wait_for_user()
    
    # Step 6: Test search
    print("\n🔍 STEP 6: Testing Semantic Search")
    
    searches = [
        "risk categories",
        "training requirements",
        "regulatory reporting"
    ]
    
    for i, search in enumerate(searches, 1):
        print(f"\n--- Search {i}/3 ---")
        run_command(f'python gemini_cli.py search "{search}" --max-results 3', f"Searching for: {search}")
        if i < len(searches):
            time.sleep(2)  # Brief pause between searches
    
    wait_for_user()
    
    # Step 7: Final status
    print("\n📈 STEP 7: Final Database Status")
    run_command("python gemini_cli.py status", "Final status check")
    
    # Demo complete
    print("\n🎉 Demo Complete!")
    print("=" * 60)
    print("✅ Successfully demonstrated:")
    print("  • PDF document creation")
    print("  • Document loading with Gemini embeddings")
    print("  • RAG queries with Gemini Flash LLM")
    print("  • Semantic search capabilities")
    print("  • Database status monitoring")
    
    print("\n🚀 Next Steps:")
    print("  • Try interactive mode: python gemini_cli.py interactive")
    print("  • Load your own PDF documents")
    print("  • Experiment with different queries")
    print("  • Explore the advanced features")
    
    print("\n📚 Resources:")
    print("  • Quick Start Guide: CLI_QUICK_START.md")
    print("  • Technical Details: README_GEMINI_VECTOR_SERVICE.md")
    print("  • API Reference: vector_service_gemini.py")

if __name__ == "__main__":
    main() 