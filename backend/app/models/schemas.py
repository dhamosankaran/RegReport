from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class ComplianceStatus(str, Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PARTIAL_COMPLIANCE = "partial_compliance"
    REQUIRES_REVIEW = "requires_review"

class ComplianceQuery(BaseModel):
    concern: str = Field(..., description="The regulatory data concern or question to check")
    context: Optional[str] = Field(None, description="Additional context about the concern")

class RelevantDocument(BaseModel):
    document_name: str = Field(..., description="Name of the source document")
    section: str = Field(..., description="Relevant section or page")
    content: str = Field(..., description="Relevant content from the document")
    relevance_score: float = Field(..., description="Relevance score (0-1)")

class ComplianceDetail(BaseModel):
    rule_reference: str = Field(..., description="Reference to specific rule or instruction")
    description: str = Field(..., description="Detailed description of the compliance requirement")
    impact_level: str = Field(..., description="Impact level: high, medium, low")
    required_action: Optional[str] = Field(None, description="Required action to achieve compliance")
    deadline: Optional[str] = Field(None, description="Deadline or schedule if applicable")

class ComplianceResponse(BaseModel):
    status: ComplianceStatus = Field(..., description="Overall compliance status")
    confidence_score: float = Field(..., description="Confidence score of the assessment (0-1)")
    summary: str = Field(..., description="Summary of the compliance assessment")
    
    # Detailed analysis
    impacted_rules: List[str] = Field(default_factory=list, description="List of impacted rules or instructions")
    compliance_details: List[ComplianceDetail] = Field(default_factory=list, description="Detailed compliance analysis")
    
    # Supporting evidence
    relevant_documents: List[RelevantDocument] = Field(default_factory=list, description="Relevant document excerpts")
    
    # Reasoning
    reasoning: str = Field(..., description="Detailed reasoning behind the assessment")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for compliance")
    
    # Metadata
    query_timestamp: datetime = Field(default_factory=datetime.now)
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")

class DocumentStatus(BaseModel):
    document_name: str
    chunk_count: int
    last_updated: datetime
    status: str  # "loaded", "error", "processing"

class DocumentsStatus(BaseModel):
    total_documents: int
    total_chunks: int
    documents: List[DocumentStatus]
    last_refresh: datetime 