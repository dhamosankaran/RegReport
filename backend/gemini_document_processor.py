import os
import asyncio
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime
import uuid
import PyPDF2
from io import BytesIO

logger = logging.getLogger(__name__)

class DocumentChunk:
    """Represents a chunk of text from a document"""
    def __init__(self, content: str, chunk_id: str, metadata: Dict[str, Any] = None):
        self.content = content
        self.chunk_id = chunk_id
        self.metadata = metadata or {}

class GeminiDocumentProcessor:
    """
    Document processor optimized for Gemini that doesn't rely on tiktoken
    Uses character-based and sentence-aware chunking strategies
    """
    
    def __init__(self, 
                 max_chunk_size: int = 4000,  # Characters, not tokens
                 chunk_overlap: int = 200,     # Character overlap
                 min_chunk_size: int = 100):   # Minimum chunk size
        
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        
        # Sentence endings for better chunking
        self.sentence_endings = re.compile(r'[.!?]+\s+')
        
        # Paragraph breaks
        self.paragraph_breaks = re.compile(r'\n\s*\n')
        
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        
        # Remove very short lines that might be artifacts
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            if len(line.strip()) > 3:  # Skip very short lines
                cleaned_lines.append(line.strip())
        
        return '\n'.join(cleaned_lines).strip()
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Split text into sentences for better chunking boundaries"""
        sentences = self.sentence_endings.split(text)
        # Add back the punctuation except for the last sentence
        result = []
        for i, sentence in enumerate(sentences[:-1]):
            if sentence.strip():
                result.append(sentence.strip() + '.')
        if sentences[-1].strip():
            result.append(sentences[-1].strip())
        return result
    
    def _split_by_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        paragraphs = self.paragraph_breaks.split(text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _create_chunks_from_text(self, text: str, source_metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """Create chunks from text using sentence-aware approach"""
        chunks = []
        
        # First, try to split by paragraphs
        paragraphs = self._split_by_paragraphs(text)
        
        current_chunk = ""
        chunk_number = 1
        
        for paragraph in paragraphs:
            # If paragraph is small enough, add it to current chunk
            if len(current_chunk) + len(paragraph) <= self.max_chunk_size:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
            else:
                # Save current chunk if it exists
                if current_chunk and len(current_chunk) >= self.min_chunk_size:
                    chunk_id = f"{source_metadata.get('document_name', 'unknown')}-page-{source_metadata.get('page_number', 1)}-chunk-{chunk_number}"
                    
                    chunks.append(DocumentChunk(
                        content=current_chunk.strip(),
                        chunk_id=chunk_id,
                        metadata={
                            **source_metadata,
                            'chunk_number': chunk_number,
                            'chunk_method': 'paragraph-aware'
                        }
                    ))
                    chunk_number += 1
                
                # Start new chunk with overlap
                if len(current_chunk) > self.chunk_overlap:
                    # Use last part of current chunk as overlap
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    # Find a good breakpoint for overlap
                    sentences = self._split_by_sentences(overlap_text)
                    if len(sentences) > 1:
                        overlap_text = sentences[-1]  # Use last sentence
                    current_chunk = overlap_text + "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add final chunk
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunk_id = f"{source_metadata.get('document_name', 'unknown')}-page-{source_metadata.get('page_number', 1)}-chunk-{chunk_number}"
            
            chunks.append(DocumentChunk(
                content=current_chunk.strip(),
                chunk_id=chunk_id,
                metadata={
                    **source_metadata,
                    'chunk_number': chunk_number,
                    'chunk_method': 'paragraph-aware'
                }
            ))
        
        return chunks
    
    def _fallback_chunking(self, text: str, source_metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """Fallback chunking when paragraph-based approach doesn't work well"""
        chunks = []
        sentences = self._split_by_sentences(text)
        
        current_chunk = ""
        chunk_number = 1
        
        for sentence in sentences:
            # If adding this sentence would exceed max size, save current chunk
            if len(current_chunk) + len(sentence) > self.max_chunk_size and current_chunk:
                if len(current_chunk) >= self.min_chunk_size:
                    chunk_id = f"{source_metadata.get('document_name', 'unknown')}-page-{source_metadata.get('page_number', 1)}-chunk-{chunk_number}"
                    
                    chunks.append(DocumentChunk(
                        content=current_chunk.strip(),
                        chunk_id=chunk_id,
                        metadata={
                            **source_metadata,
                            'chunk_number': chunk_number,
                            'chunk_method': 'sentence-based'
                        }
                    ))
                    chunk_number += 1
                
                # Start new chunk with overlap
                if len(current_chunk) > self.chunk_overlap:
                    # Use last part for overlap
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    # Find sentence boundary for cleaner overlap
                    sentences_in_overlap = self._split_by_sentences(overlap_text)
                    if len(sentences_in_overlap) > 1:
                        overlap_text = sentences_in_overlap[-1]
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add final chunk
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunk_id = f"{source_metadata.get('document_name', 'unknown')}-page-{source_metadata.get('page_number', 1)}-chunk-{chunk_number}"
            
            chunks.append(DocumentChunk(
                content=current_chunk.strip(),
                chunk_id=chunk_id,
                metadata={
                    **source_metadata,
                    'chunk_number': chunk_number,
                    'method': 'sentence-based'
                }
            ))
        
        return chunks
    
    async def process_pdf(self, file_path: str) -> List[DocumentChunk]:
        """Process PDF file and return chunks"""
        try:
            chunks = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    # Extract text from page
                    text = page.extract_text()
                    
                    if not text.strip():
                        continue
                    
                    # Clean the text
                    cleaned_text = self._clean_text(text)
                    
                    if len(cleaned_text) < self.min_chunk_size:
                        continue
                    
                    # Metadata for this page
                    page_metadata = {
                        'document_name': os.path.basename(file_path),
                        'page_number': page_num,
                        'source_file': file_path,
                        'chunk_type': 'general',
                        'processing_timestamp': datetime.now().isoformat()
                    }
                    
                    # Try paragraph-based chunking first
                    page_chunks = self._create_chunks_from_text(cleaned_text, page_metadata)
                    
                    # If chunks are too large, use sentence-based fallback
                    if any(len(chunk.content) > self.max_chunk_size * 1.2 for chunk in page_chunks):
                        page_chunks = self._fallback_chunking(cleaned_text, page_metadata)
                    
                    chunks.extend(page_chunks)
            
            logger.info(f"Processed {file_path}: {len(chunks)} chunks created")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise
    
    def get_chunk_stats(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """Get statistics about the chunks"""
        if not chunks:
            return {"total_chunks": 0}
        
        sizes = [len(chunk.content) for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "average_size": sum(sizes) / len(sizes),
            "min_size": min(sizes),
            "max_size": max(sizes),
            "chunking_method": "character-based (no tiktoken)",
            "overlap_strategy": "sentence-aware"
        } 