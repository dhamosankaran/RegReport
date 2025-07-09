#!/usr/bin/env python3
"""
Simple example to demonstrate chunking without tiktoken in Gemini Vector Service
"""

import asyncio
from pathlib import Path
from gemini_document_processor import GeminiDocumentProcessor

async def demonstrate_chunking():
    """Demonstrate how chunking works without tiktoken"""
    
    print("🔧 Chunking Demonstration - No tiktoken Required")
    print("=" * 50)
    
    # Initialize the processor
    processor = GeminiDocumentProcessor(
        max_chunk_size=1000,  # Smaller for demo
        chunk_overlap=100,
        min_chunk_size=50
    )
    
    print(f"📋 Configuration:")
    print(f"   • Max chunk size: {processor.max_chunk_size} characters")
    print(f"   • Overlap: {processor.chunk_overlap} characters")
    print(f"   • Min chunk size: {processor.min_chunk_size} characters")
    print(f"   • Method: Character-based (no tiktoken)")
    
    # Create sample text
    sample_text = """
    This is a sample document for demonstration purposes. It contains multiple paragraphs 
    to show how the chunking process works without relying on tiktoken.
    
    The first paragraph discusses the importance of proper document processing in modern 
    AI systems. It explains how chunking affects the quality of embeddings and retrieval.
    
    The second paragraph focuses on the advantages of character-based chunking over 
    token-based approaches. This method is more reliable and doesn't require external 
    tokenization libraries.
    
    The third paragraph describes the implementation details. It shows how sentences 
    and paragraphs are used as natural boundaries for creating meaningful chunks.
    
    This approach ensures that the chunking process is both efficient and accurate, 
    making it ideal for use with Google Gemini's embedding models.
    """
    
    print(f"\n📝 Sample Text ({len(sample_text)} characters):")
    print(sample_text[:200] + "..." if len(sample_text) > 200 else sample_text)
    
    # Process the text
    chunks = processor._create_chunks_from_text(sample_text, {
        'document_name': 'sample_doc.txt',
        'page_number': 1,
        'source_file': 'sample_doc.txt'
    })
    
    print(f"\n📊 Chunking Results:")
    print(f"   • Total chunks created: {len(chunks)}")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"\n   📄 Chunk {i}:")
        print(f"      • ID: {chunk.chunk_id}")
        print(f"      • Size: {len(chunk.content)} characters")
        print(f"      • Method: {chunk.metadata.get('chunk_method', 'unknown')}")
        print(f"      • Content preview: {chunk.content[:100]}...")
        
        # Show overlap with previous chunk
        if i > 1:
            prev_chunk = chunks[i-2]
            overlap = find_overlap(prev_chunk.content, chunk.content)
            if overlap:
                print(f"      • Overlap with previous: {len(overlap)} characters")
    
    # Get statistics
    stats = processor.get_chunk_stats(chunks)
    print(f"\n📈 Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   • {key}: {value:.1f}")
        else:
            print(f"   • {key}: {value}")

def find_overlap(text1: str, text2: str) -> str:
    """Find overlapping text between two chunks"""
    # Simple overlap detection
    for i in range(min(len(text1), len(text2)), 0, -1):
        if text1[-i:] == text2[:i]:
            return text1[-i:]
    return ""

if __name__ == "__main__":
    asyncio.run(demonstrate_chunking()) 