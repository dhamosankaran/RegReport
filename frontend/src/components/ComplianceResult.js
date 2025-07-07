import React, { useState } from 'react';
import { 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Clock, 
  FileText,
  ChevronDown,
  ChevronUp,
  Info,
  Calendar,
  Target,
  BookOpen,
  TrendingUp
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const ComplianceResult = ({ result }) => {
  const [expandedSections, setExpandedSections] = useState({
    details: false,
    documents: false,
    recommendations: false
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle className="w-6 h-6 text-success-600" />;
      case 'non_compliant':
        return <XCircle className="w-6 h-6 text-danger-600" />;
      case 'partial_compliance':
        return <AlertCircle className="w-6 h-6 text-warning-600" />;
      case 'requires_review':
        return <Clock className="w-6 h-6 text-gray-600" />;
      default:
        return <Clock className="w-6 h-6 text-gray-600" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'compliant':
        return 'status-badge-compliant';
      case 'non_compliant':
        return 'status-badge-non-compliant';
      case 'partial_compliance':
        return 'status-badge-partial';
      case 'requires_review':
        return 'status-badge-review';
      default:
        return 'status-badge-review';
    }
  };

  const getStatusBgColor = (status) => {
    switch (status) {
      case 'compliant':
        return 'bg-success-50 border-success-200';
      case 'non_compliant':
        return 'bg-danger-50 border-danger-200';
      case 'partial_compliance':
        return 'bg-warning-50 border-warning-200';
      case 'requires_review':
        return 'bg-gray-50 border-gray-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const formatStatus = (status) => {
    switch (status) {
      case 'compliant':
        return 'Compliant';
      case 'non_compliant':
        return 'Non-Compliant';
      case 'partial_compliance':
        return 'Partial Compliance';
      case 'requires_review':
        return 'Requires Review';
      default:
        return 'Unknown';
    }
  };

  const getImpactLevelColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'high':
        return 'bg-danger-100 text-danger-800';
      case 'medium':
        return 'bg-warning-100 text-warning-800';
      case 'low':
        return 'bg-success-100 text-success-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const confidencePercentage = Math.round((result.confidence_score || 0) * 100);

  return (
    <div className="space-y-6">
      {/* Main Result Card */}
      <div className={`card ${getStatusBgColor(result.status)}`}>
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            {getStatusIcon(result.status)}
            <div>
              <h3 className="text-xl font-semibold text-gray-900">
                {formatStatus(result.status)}
              </h3>
              <p className="text-gray-600 mt-1">{result.summary}</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <div className="text-sm text-gray-500">Confidence</div>
              <div className="text-lg font-semibold text-gray-900">
                {confidencePercentage}%
              </div>
            </div>
            <span className={`status-badge ${getStatusColor(result.status)}`}>
              {formatStatus(result.status)}
            </span>
          </div>
        </div>
      </div>

      {/* Fallback/Parsing Warning */}
      {(result.summary?.toLowerCase().includes('fallback parsing') || result.status === 'requires_review') && (
        <div className="card bg-warning-50 border-warning-200 mt-2">
          <div className="flex items-center space-x-2 text-warning-700">
            <AlertCircle className="w-5 h-5" />
            <span className="font-medium">AI Output Warning</span>
          </div>
          <p className="text-warning-600 mt-1">
            The AI could not produce a fully structured compliance answer for this query. This may be due to an ambiguous question, a system error, or the AI not following strict JSON output instructions. Please try rephrasing your query or contact support if this persists.
          </p>
        </div>
      )}

      {/* Metadata */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card">
          <div className="flex items-center space-x-2 text-gray-600 mb-2">
            <Clock className="w-4 h-4" />
            <span className="text-sm font-medium">Processing Time</span>
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {result.processing_time_ms ? `${result.processing_time_ms}ms` : 'N/A'}
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-2 text-gray-600 mb-2">
            <BookOpen className="w-4 h-4" />
            <span className="text-sm font-medium">Impacted Rules</span>
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {result.impacted_rules?.length || 0}
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-2 text-gray-600 mb-2">
            <FileText className="w-4 h-4" />
            <span className="text-sm font-medium">Source Documents</span>
          </div>
          <div className="text-lg font-semibold text-gray-900">
            {result.relevant_documents?.length || 0}
          </div>
        </div>
      </div>

      {/* Reasoning */}
      <div className="card">
        <div className="flex items-center space-x-2 text-gray-900 mb-3">
          <Info className="w-5 h-5" />
          <h4 className="font-semibold">Analysis Reasoning</h4>
        </div>
        <div className="text-gray-700 leading-relaxed">
          {result.reasoning || 'No detailed reasoning provided.'}
        </div>
      </div>

      {/* Impacted Rules */}
      {result.impacted_rules && result.impacted_rules.length > 0 && (
        <div className="card">
          <div className="flex items-center space-x-2 text-gray-900 mb-3">
            <Target className="w-5 h-5" />
            <h4 className="font-semibold">Impacted Rules</h4>
          </div>
          <div className="space-y-2">
            {result.impacted_rules.map((rule, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-lg">
                <div className="font-medium text-gray-900">{rule}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Compliance Details */}
      {result.compliance_details && result.compliance_details.length > 0 && (
        <div className="card">
          <button
            onClick={() => toggleSection('details')}
            className="flex items-center justify-between w-full text-left"
          >
            <div className="flex items-center space-x-2 text-gray-900">
              <TrendingUp className="w-5 h-5" />
              <h4 className="font-semibold">Compliance Details</h4>
            </div>
            {expandedSections.details ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>
          
          {expandedSections.details && (
            <div className="mt-4 space-y-4">
              {result.compliance_details.map((detail, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-gray-900">
                      {detail.rule_reference}
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactLevelColor(detail.impact_level)}`}>
                      {detail.impact_level || 'Medium'} Impact
                    </span>
                  </div>
                  <p className="text-gray-700 mb-3">{detail.description}</p>
                  
                  {detail.required_action && (
                    <div className="mb-2">
                      <span className="text-sm font-medium text-gray-900">Required Action:</span>
                      <p className="text-sm text-gray-600 mt-1">{detail.required_action}</p>
                    </div>
                  )}
                  
                  {detail.deadline && (
                    <div className="flex items-center space-x-2 text-sm text-gray-600">
                      <Calendar className="w-4 h-4" />
                      <span>Deadline: {detail.deadline}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <div className="card">
          <button
            onClick={() => toggleSection('recommendations')}
            className="flex items-center justify-between w-full text-left"
          >
            <div className="flex items-center space-x-2 text-gray-900">
              <CheckCircle className="w-5 h-5" />
              <h4 className="font-semibold">Recommendations</h4>
            </div>
            {expandedSections.recommendations ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>
          
          {expandedSections.recommendations && (
            <div className="mt-4 space-y-3">
              {result.recommendations.map((recommendation, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-primary-100 rounded-full flex items-center justify-center mt-0.5">
                    <span className="text-xs font-medium text-primary-600">
                      {index + 1}
                    </span>
                  </div>
                  <div className="text-gray-700">{recommendation}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Relevant Documents */}
      {result.relevant_documents && result.relevant_documents.length > 0 && (
        <div className="card">
          <button
            onClick={() => toggleSection('documents')}
            className="flex items-center justify-between w-full text-left"
          >
            <div className="flex items-center space-x-2 text-gray-900">
              <FileText className="w-5 h-5" />
              <h4 className="font-semibold">Relevant Documents</h4>
            </div>
            {expandedSections.documents ? (
              <ChevronUp className="w-5 h-5 text-gray-500" />
            ) : (
              <ChevronDown className="w-5 h-5 text-gray-500" />
            )}
          </button>
          
          {expandedSections.documents && (
            <div className="mt-4 space-y-4">
              {result.relevant_documents.map((doc, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-gray-900">
                      {doc.document_name}
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-500">{doc.section}</span>
                      <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                        {Math.round((doc.relevance_score || 0) * 100)}% relevant
                      </span>
                    </div>
                  </div>
                  <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded border-l-4 border-gray-300">
                    {doc.content}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="card bg-gray-50">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <div>
            Analysis completed at {new Date(result.query_timestamp).toLocaleString()}
          </div>
          <div>
            Powered by RAG Technology
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComplianceResult; 