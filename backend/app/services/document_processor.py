import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import hashlib
import re

import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import tiktoken

from ..utils.logging_config import get_logger

logger = get_logger("document_processor")

class DocumentChunk:
    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.content = content
        self.metadata = metadata
        self.chunk_id = self._generate_chunk_id()
    
    def _generate_chunk_id(self) -> str:
        """Generate a unique ID for this chunk"""
        content_hash = hashlib.md5(self.content.encode()).hexdigest()
        return f"{self.metadata.get('document_name', 'unknown')}_{self.metadata.get('page_number', 0)}_{content_hash[:8]}"

class DocumentProcessor:
    def __init__(self, max_chunk_size: int = 1000, chunk_overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=self._tiktoken_length,
            separators=[
                "\n\n",  # Paragraph breaks
                "\n",    # Line breaks
                ". ",    # Sentence endings
                "? ",    # Question endings
                "! ",    # Exclamation endings
                "; ",    # Semicolon
                ", ",    # Comma
                " ",     # Space
                ""       # Character level
            ]
        )
        
        # Initialize tokenizer for accurate token counting
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def _tiktoken_length(self, text: str) -> int:
        """Get accurate token count using tiktoken"""
        return len(self.tokenizer.encode(text))
    
    async def process_pdf(self, file_path: str) -> List[DocumentChunk]:
        """
        Process a PDF file and return semantic chunks
        """
        try:
            logger.info(f"Processing PDF: {file_path}")
            
            # Extract text from PDF
            text_content = await self._extract_pdf_text(file_path)
            
            # Clean and preprocess text
            cleaned_text = self._clean_text(text_content)
            
            # Create document for chunking
            document = Document(
                page_content=cleaned_text,
                metadata={
                    "document_name": os.path.basename(file_path),
                    "file_path": file_path,
                    "processed_at": datetime.now().isoformat()
                }
            )
            
            # Split into chunks
            chunks = self._create_semantic_chunks(document)
            
            logger.info(f"Created {len(chunks)} chunks from {file_path}")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise
    
    async def _extract_pdf_text(self, file_path: str) -> Dict[int, str]:
        """Extract text from PDF with page information"""
        text_by_page = {}
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():  # Only store non-empty pages
                        text_by_page[page_num + 1] = text
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {str(e)}")
                    continue
        
        return text_by_page
    
    def _clean_text(self, text_by_page: Dict[int, str]) -> str:
        """Clean and normalize extracted text"""
        cleaned_pages = []
        
        for page_num, text in text_by_page.items():
            # Basic cleaning
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            text = re.sub(r'[^\w\s\.,;:!?()-]', '', text)  # Remove special chars
            text = text.strip()
            
            if text:
                # Add page marker for context
                cleaned_pages.append(f"[PAGE {page_num}]\n{text}")
        
        return "\n\n".join(cleaned_pages)
    
    def _create_semantic_chunks(self, document: Document) -> List[DocumentChunk]:
        """Create semantically meaningful chunks"""
        chunks = []
        
        # Split the document
        text_chunks = self.text_splitter.split_documents([document])
        
        for i, chunk in enumerate(text_chunks):
            # Extract page number from content if available
            page_match = re.search(r'\[PAGE (\d+)\]', chunk.page_content)
            page_number = int(page_match.group(1)) if page_match else 1
            
            # Clean chunk content (remove page markers)
            content = re.sub(r'\[PAGE \d+\]\n?', '', chunk.page_content).strip()
            
            # Skip very short chunks
            if len(content) < 50:
                continue
            
            # Create enhanced metadata
            metadata = {
                **chunk.metadata,
                "chunk_index": i,
                "page_number": page_number,
                "token_count": self._tiktoken_length(content),
                "word_count": len(content.split()),
                "chunk_type": self._classify_chunk_type(content)
            }
            
            # Create document chunk
            doc_chunk = DocumentChunk(content, metadata)
            chunks.append(doc_chunk)
        
        return chunks
    
    def _classify_chunk_type(self, content: str) -> str:
        """Classify the type of content in the chunk"""
        content_lower = content.lower()
        
        # Check for common regulatory patterns
        if any(keyword in content_lower for keyword in ['section', 'article', 'rule', 'regulation']):
            return "regulatory_rule"
        elif any(keyword in content_lower for keyword in ['procedure', 'process', 'step', 'method']):
            return "procedure"
        elif any(keyword in content_lower for keyword in ['requirement', 'must', 'shall', 'mandatory']):
            return "requirement"
        elif any(keyword in content_lower for keyword in ['definition', 'means', 'defined as']):
            return "definition"
        elif any(keyword in content_lower for keyword in ['example', 'instance', 'case study']):
            return "example"
        elif any(keyword in content_lower for keyword in ['schedule', 'timeline', 'deadline', 'date']):
            return "schedule"
        else:
            return "general"
    
    async def process_multiple_pdfs(self, file_paths: List[str]) -> List[DocumentChunk]:
        """Process multiple PDF files concurrently"""
        tasks = [self.process_pdf(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_chunks = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to process {file_paths[i]}: {str(result)}")
            else:
                all_chunks.extend(result)
        
        return all_chunks
    
    def get_chunk_statistics(self, chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """Get statistics about the processed chunks"""
        if not chunks:
            return {"total_chunks": 0}
        
        token_counts = [chunk.metadata.get("token_count", 0) for chunk in chunks]
        word_counts = [chunk.metadata.get("word_count", 0) for chunk in chunks]
        chunk_types = [chunk.metadata.get("chunk_type", "unknown") for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "avg_token_count": sum(token_counts) / len(token_counts) if token_counts else 0,
            "avg_word_count": sum(word_counts) / len(word_counts) if word_counts else 0,
            "max_token_count": max(token_counts) if token_counts else 0,
            "min_token_count": min(token_counts) if token_counts else 0,
            "chunk_type_distribution": {
                chunk_type: chunk_types.count(chunk_type) 
                for chunk_type in set(chunk_types)
            }
        } 