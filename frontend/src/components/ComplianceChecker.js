import React, { useState } from 'react';
import { 
  Send, 
  AlertCircle, 
  CheckCircle, 
  XCircle, 
  Clock, 
  FileText,
  TrendingUp,
  Calendar,
  Target
} from 'lucide-react';
import ComplianceResult from './ComplianceResult';
import LoadingSpinner from './LoadingSpinner';
import { checkCompliance } from '../services/api';

const ComplianceChecker = () => {
  const [concern, setConcern] = useState('');
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!concern.trim()) {
      setError('Please enter a concern to check');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await checkCompliance(concern, context);
      setResult(response);
    } catch (err) {
      setError(err.message || 'Failed to check compliance. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setConcern('');
    setContext('');
    setResult(null);
    setError(null);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle className="w-5 h-5 text-success-600" />;
      case 'non_compliant':
        return <XCircle className="w-5 h-5 text-danger-600" />;
      case 'partial_compliance':
        return <AlertCircle className="w-5 h-5 text-warning-600" />;
      case 'requires_review':
        return <Clock className="w-5 h-5 text-gray-600" />;
      default:
        return <Clock className="w-5 h-5 text-gray-600" />;
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

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-gray-900">
          Regulatory Compliance Checker
        </h2>
        <p className="text-lg text-gray-600">
          Check your regulatory data concerns against Instructions.pdf and Rules.pdf
        </p>
      </div>

      {/* Input Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="concern" className="form-label">
              Regulatory Concern *
            </label>
            <textarea
              id="concern"
              value={concern}
              onChange={(e) => setConcern(e.target.value)}
              placeholder="Describe your regulatory data concern or question..."
              className="form-textarea h-32"
              required
            />
            <p className="text-sm text-gray-500 mt-1">
              Be specific about your concern to get the most accurate compliance assessment.
            </p>
          </div>

          <div>
            <label htmlFor="context" className="form-label">
              Additional Context (Optional)
            </label>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Provide any additional context that might help with the assessment..."
              className="form-textarea h-24"
            />
          </div>

          <div className="flex items-center justify-between">
            <button
              type="button"
              onClick={handleReset}
              className="btn btn-secondary"
              disabled={loading}
            >
              Reset
            </button>
            <button
              type="submit"
              disabled={loading || !concern.trim()}
              className="btn btn-primary"
            >
              {loading ? (
                <>
                  <LoadingSpinner />
                  <span className="ml-2">Checking Compliance...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  <span>Check Compliance</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Error Message */}
      {error && (
        <div className="card bg-danger-50 border-danger-200">
          <div className="flex items-center space-x-2 text-danger-700">
            <AlertCircle className="w-5 h-5" />
            <span className="font-medium">Error</span>
          </div>
          <p className="text-danger-600 mt-1">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="fade-in">
          <ComplianceResult result={result} />
        </div>
      )}

      {/* Usage Instructions */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="flex items-center space-x-2 text-blue-700 mb-3">
          <FileText className="w-5 h-5" />
          <span className="font-medium">How to Use</span>
        </div>
        <ul className="text-blue-600 space-y-1 text-sm">
          <li>• Enter your regulatory concern or question in the text area above</li>
          <li>• Add any additional context that might help with the assessment</li>
          <li>• Click "Check Compliance" to get an AI-powered analysis</li>
          <li>• Review the detailed results including impacted rules and recommendations</li>
        </ul>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mx-auto mb-3">
            <TrendingUp className="w-6 h-6 text-primary-600" />
          </div>
          <h3 className="font-semibold text-gray-900 mb-2">AI-Powered Analysis</h3>
          <p className="text-sm text-gray-600">
            Advanced RAG technology provides accurate compliance assessments
          </p>
        </div>

        <div className="card text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-success-100 rounded-lg mx-auto mb-3">
            <Target className="w-6 h-6 text-success-600" />
          </div>
          <h3 className="font-semibold text-gray-900 mb-2">Precise Results</h3>
          <p className="text-sm text-gray-600">
            Get specific rule references and detailed compliance recommendations
          </p>
        </div>

        <div className="card text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-warning-100 rounded-lg mx-auto mb-3">
            <Calendar className="w-6 h-6 text-warning-600" />
          </div>
          <h3 className="font-semibold text-gray-900 mb-2">Deadline Tracking</h3>
          <p className="text-sm text-gray-600">
            Identify important schedules and deadlines for compliance
          </p>
        </div>
      </div>
    </div>
  );
};

export default ComplianceChecker; 