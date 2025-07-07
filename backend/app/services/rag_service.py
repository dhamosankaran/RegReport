import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import time
import json
import re

import openai
from openai import AsyncOpenAI

from .vector_service import PostgreSQLVectorService
from ..models.schemas import (
    ComplianceResponse, 
    ComplianceStatus, 
    ComplianceDetail, 
    RelevantDocument
)
from ..utils.logging_config import get_logger

logger = get_logger("rag_service")

# Define the OpenAI function schema for compliance assessment
compliance_function = {
    "name": "compliance_assessment",
    "description": "Return a compliance assessment as a structured JSON object.",
    "parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["compliant", "non_compliant", "partial_compliance", "requires_review"]
            },
            "confidence_score": {"type": "number"},
            "summary": {"type": "string"},
            "impacted_rules": {
                "type": "array",
                "items": {"type": "string"}
            },
            "reasoning": {"type": "string"},
            "compliance_details": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_reference": {"type": "string"},
                        "description": {"type": "string"},
                        "impact_level": {"type": "string"},
                        "required_action": {"type": "string"},
                        "deadline": {"type": "string"}
                    }
                }
            },
            "recommendations": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["status", "confidence_score", "summary", "impacted_rules", "reasoning", "compliance_details", "recommendations"]
    }
}

class RAGService:
    def __init__(self, vector_service: PostgreSQLVectorService):
        self.vector_service = vector_service
        
        # Initialize OpenAI client
        self.openai_client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Configuration
        self.model_name = "gpt-4o-mini"  # Updated to use GPT-4o-mini
        self.max_context_length = 8000
        self.max_retrieved_docs = 10
        
        # Compliance checking prompts
        self.system_prompt = """
        You are a strict JSON API. You must ONLY output a single valid JSON object, and nothing else. Do not include any explanation, markdown, or text outside the JSON object. If you do, your output will be rejected.
        """
        
        self.compliance_prompt_template = """
        Analyze this compliance concern against the provided regulatory documents:

        CONCERN: {concern}
        CONTEXT: {context}

        RELEVANT REGULATORY CONTENT:
        {retrieved_content}
        """
    
    async def check_compliance(self, concern: str, context: Optional[str] = None) -> ComplianceResponse:
        """
        Check regulatory compliance for a given concern
        """
        start_time = time.time()
        
        try:
            logger.debug(f"[DEBUG] Starting compliance check for concern: {concern[:100]}...")
            
            # Step 1: Retrieve relevant documents
            logger.debug(f"[DEBUG] Retrieving relevant documents...")
            retrieved_docs = await self._retrieve_relevant_documents(concern, context)
            logger.debug(f"[DEBUG] Retrieved {len(retrieved_docs)} documents")
            
            # Step 2: Generate LLM response
            logger.debug(f"[DEBUG] Generating LLM response...")
            llm_response = await self._generate_compliance_response(concern, context, retrieved_docs)
            logger.debug(f"[DEBUG] LLM response generated, length: {len(llm_response)}")
            
            # Step 3: Parse and format response
            logger.debug(f"[DEBUG] Parsing LLM response...")
            compliance_response = await self._parse_llm_response(llm_response, retrieved_docs)
            logger.debug(f"[DEBUG] LLM response parsed successfully")
            
            # Add processing time
            processing_time = int((time.time() - start_time) * 1000)
            compliance_response.processing_time_ms = processing_time
            
            return compliance_response
            
        except Exception as e:
            logger.error(f"Error in compliance check: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Return error response
            return ComplianceResponse(
                status=ComplianceStatus.REQUIRES_REVIEW,
                confidence_score=0.0,
                summary=f"Error processing compliance check: {str(e)}",
                reasoning="An error occurred during processing. Please try again.",
                processing_time_ms=int((time.time() - start_time) * 1000)
            )
    
    async def _retrieve_relevant_documents(self, concern: str, context: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from the vector database
        """
        try:
            # Combine concern and context for better retrieval
            query = concern
            if context:
                query += f" {context}"
            
            # Perform hybrid search to get diverse relevant content
            results = await self.vector_service.hybrid_search(
                query=query,
                n_results=self.max_retrieved_docs,
                include_types=["regulatory_rule", "requirement", "procedure", "schedule"]
            )
            
            # If we don't get enough targeted results, do a general search
            if len(results) < 5:
                general_results = await self.vector_service.search_similar_documents(
                    query=query,
                    n_results=self.max_retrieved_docs
                )
                
                # Combine and deduplicate
                combined_results = results + general_results
                seen_ids = set()
                deduplicated_results = []
                
                for result in combined_results:
                    content_hash = hash(result['content'])
                    if content_hash not in seen_ids:
                        seen_ids.add(content_hash)
                        deduplicated_results.append(result)
                
                results = deduplicated_results[:self.max_retrieved_docs]
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    async def _generate_compliance_response(self, concern: str, context: Optional[str], retrieved_docs: List[Dict[str, Any]]) -> dict:
        """
        Generate compliance response using LLM with function calling
        """
        try:
            # Format retrieved content
            retrieved_content = self._format_retrieved_content(retrieved_docs)
            prompt = self.compliance_prompt_template.format(
                concern=concern,
                context=context or "No additional context provided",
                retrieved_content=retrieved_content
            )
            if len(prompt) > self.max_context_length:
                prompt = prompt[:self.max_context_length] + "..."
            response = await self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                functions=[compliance_function],
                function_call={"name": "compliance_assessment"},
                temperature=0.1,
                max_tokens=1500
            )
            # Log the full OpenAI response for debugging
            logger.debug(f"[DEBUG] Full OpenAI API response: {response}")
            # Parse function call arguments
            if response.choices[0].message.function_call:
                args = response.choices[0].message.function_call.arguments
                parsed_response = json.loads(args)
                logger.debug(f"[DEBUG] Parsed function call arguments: {parsed_response}")
                return parsed_response
            else:
                logger.warning("[DEBUG] No function_call in OpenAI response, using fallback.")
                return self._create_fallback_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating LLM response with function calling: {str(e)}")
            raise
    
    def _format_retrieved_content(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        Format retrieved documents for LLM context
        """
        formatted_content = []
        
        for i, doc in enumerate(retrieved_docs):
            metadata = doc.get('metadata', {})
            content = doc.get('content', '')
            
            doc_info = f"Document {i+1}:"
            doc_info += f"\n- Source: {metadata.get('document_name', 'Unknown')}"
            doc_info += f"\n- Page: {metadata.get('page_number', 'Unknown')}"
            doc_info += f"\n- Type: {metadata.get('chunk_type', 'Unknown')}"
            doc_info += f"\n- Relevance Score: {doc.get('relevance_score', 0):.2f}"
            doc_info += f"\n- Content: {content}"
            doc_info += "\n" + "="*50 + "\n"
            
            formatted_content.append(doc_info)
        
        return "\n".join(formatted_content)
    
    async def _parse_llm_response(self, llm_response: dict, retrieved_docs: List[Dict[str, Any]]) -> ComplianceResponse:
        """
        Parse LLM function call response and create ComplianceResponse object
        """
        try:
            parsed_response = llm_response
            # Clean and validate the status field
            status_value = parsed_response.get("status", "requires_review")
            if isinstance(status_value, str):
                status_value = status_value.strip().lower()
                if status_value in ["non-compliant", "non_compliant", "noncompliant"]:
                    status_value = "non_compliant"
                elif status_value in ["compliant", "compliant"]:
                    status_value = "compliant"
                elif status_value in ["partial", "partial_compliance", "partially_compliant"]:
                    status_value = "partial_compliance"
                else:
                    status_value = "requires_review"
            else:
                status_value = "requires_review"
            # Clean and validate confidence score
            confidence_value = parsed_response.get("confidence_score", 0.5)
            try:
                confidence_value = float(confidence_value)
                confidence_value = max(0.0, min(1.0, confidence_value))
            except (ValueError, TypeError):
                confidence_value = 0.5
            compliance_response = ComplianceResponse(
                status=ComplianceStatus(status_value),
                confidence_score=confidence_value,
                summary=parsed_response.get("summary", "Compliance analysis completed"),
                impacted_rules=parsed_response.get("impacted_rules", []),
                reasoning=parsed_response.get("reasoning", "No specific reasoning provided"),
                recommendations=parsed_response.get("recommendations", []),
                relevant_documents=self._create_relevant_documents(retrieved_docs),
                compliance_details=self._create_compliance_details(parsed_response.get("compliance_details", []))
            )
            return compliance_response
        except Exception as e:
            logger.error(f"Error parsing LLM function call response: {str(e)}")
            logger.error(f"LLM response that caused error: {llm_response}")
            return ComplianceResponse(
                status=ComplianceStatus.REQUIRES_REVIEW,
                confidence_score=0.5,
                summary="Could not parse compliance analysis",
                reasoning="Error occurred while parsing the analysis response",
                relevant_documents=self._create_relevant_documents(retrieved_docs)
            )
    
    def _create_fallback_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Create a fallback response when JSON parsing fails
        """
        # Try to extract status from text
        response_lower = llm_response.lower()
        if "non-compliant" in response_lower or "non compliant" in response_lower:
            status = "non_compliant"
        elif "compliant" in response_lower:
            status = "compliant"
        elif "partial" in response_lower:
            status = "partial_compliance"
        else:
            status = "requires_review"
        
        return {
            "status": status,
            "confidence_score": 0.5,
            "summary": "Compliance analysis completed (fallback parsing)",
            "reasoning": llm_response,
            "impacted_rules": [],
            "compliance_details": [],
            "recommendations": []
        }
    
    def _create_relevant_documents(self, retrieved_docs: List[Dict[str, Any]]) -> List[RelevantDocument]:
        """
        Create RelevantDocument objects from retrieved documents
        """
        relevant_docs = []
        for doc in retrieved_docs:
            metadata = doc.get('metadata', {})
            relevant_doc = RelevantDocument(
                document_name=metadata.get('document_name', 'Unknown'),
                section=f"Page {metadata.get('page_number', 'Unknown')}",
                content=doc.get('content', '')[:500] + "..." if len(doc.get('content', '')) > 500 else doc.get('content', ''),
                relevance_score=doc.get('similarity_score', 0.0)
            )
            relevant_docs.append(relevant_doc)
        return relevant_docs
    
    def _create_compliance_details(self, compliance_details_data: List[Dict[str, Any]]) -> List[ComplianceDetail]:
        """
        Create ComplianceDetail objects from parsed data
        """
        compliance_details = []
        
        for detail_data in compliance_details_data:
            detail = ComplianceDetail(
                rule_reference=detail_data.get('rule_reference', 'Unknown'),
                description=detail_data.get('description', 'No description provided'),
                impact_level=detail_data.get('impact_level', 'medium'),
                required_action=detail_data.get('required_action'),
                deadline=detail_data.get('deadline')
            )
            compliance_details.append(detail)
        
        return compliance_details
    
    async def get_service_status(self) -> Dict[str, Any]:
        """
        Get the status of the RAG service
        """
        try:
            # Check vector service status
            vector_status = await self.vector_service.get_document_status()
            
            # Check OpenAI API status (simple test)
            openai_status = "connected"
            try:
                await self.openai_client.models.list()
            except:
                openai_status = "disconnected"
            
            return {
                "vector_service": {
                    "status": "connected",
                    "total_documents": vector_status.total_documents,
                    "total_chunks": vector_status.total_chunks
                },
                "openai_service": {
                    "status": openai_status,
                    "model": self.model_name
                },
                "configuration": {
                    "max_context_length": self.max_context_length,
                    "max_retrieved_docs": self.max_retrieved_docs
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting service status: {str(e)}")
            return {"error": str(e)} 