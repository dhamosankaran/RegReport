import React, { useState, useEffect } from 'react';
import { 
  RefreshCw, 
  FileText, 
  CheckCircle, 
  XCircle, 
  Clock, 
  AlertCircle,
  Database,
  Calendar,
  BarChart3
} from 'lucide-react';
import LoadingSpinner from './LoadingSpinner';
import { getDocumentStatus, reloadDocuments } from '../services/api';

const DocumentStatus = () => {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reloading, setReloading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDocumentStatus();
  }, []);

  const fetchDocumentStatus = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getDocumentStatus();
      setStatus(response);
    } catch (err) {
      setError(err.message || 'Failed to fetch document status');
    } finally {
      setLoading(false);
    }
  };

  const handleReload = async () => {
    try {
      setReloading(true);
      setError(null);
      await reloadDocuments();
      // Refresh status after reload
      await fetchDocumentStatus();
    } catch (err) {
      setError(err.message || 'Failed to reload documents');
    } finally {
      setReloading(false);
    }
  };

  const getStatusIcon = (docStatus) => {
    switch (docStatus) {
      case 'loaded':
        return <CheckCircle className="w-5 h-5 text-success-600" />;
      case 'error':
        return <XCircle className="w-5 h-5 text-danger-600" />;
      case 'processing':
        return <Clock className="w-5 h-5 text-warning-600" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-600" />;
    }
  };

  const getStatusColor = (docStatus) => {
    switch (docStatus) {
      case 'loaded':
        return 'status-badge-compliant';
      case 'error':
        return 'status-badge-non-compliant';
      case 'processing':
        return 'status-badge-partial';
      default:
        return 'status-badge-review';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <LoadingSpinner size="large" />
        <span className="ml-3 text-gray-600">Loading document status...</span>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Document Status</h2>
          <p className="text-gray-600">
            Monitor the status of regulatory documents in the vector database
          </p>
        </div>
        <button
          onClick={handleReload}
          disabled={reloading}
          className="btn btn-primary"
        >
          {reloading ? (
            <>
              <LoadingSpinner />
              <span className="ml-2">Reloading...</span>
            </>
          ) : (
            <>
              <RefreshCw className="w-4 h-4 mr-2" />
              <span>Reload Documents</span>
            </>
          )}
        </button>
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

      {/* Summary Cards */}
      {status && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="card">
            <div className="flex items-center space-x-2 text-gray-600 mb-2">
              <FileText className="w-4 h-4" />
              <span className="text-sm font-medium">Total Documents</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {status.total_documents}
            </div>
          </div>

          <div className="card">
            <div className="flex items-center space-x-2 text-gray-600 mb-2">
              <Database className="w-4 h-4" />
              <span className="text-sm font-medium">Total Chunks</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">
              {status.total_chunks}
            </div>
          </div>

          <div className="card">
            <div className="flex items-center space-x-2 text-gray-600 mb-2">
              <Calendar className="w-4 h-4" />
              <span className="text-sm font-medium">Last Refresh</span>
            </div>
            <div className="text-sm text-gray-900">
              {formatDate(status.last_refresh)}
            </div>
          </div>
        </div>
      )}

      {/* Document Details */}
      {status && status.documents && (
        <div className="card">
          <div className="flex items-center space-x-2 text-gray-900 mb-4">
            <BarChart3 className="w-5 h-5" />
            <h3 className="font-semibold">Document Details</h3>
          </div>
          
          <div className="space-y-4">
            {status.documents.map((doc, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    {getStatusIcon(doc.status)}
                    <div>
                      <h4 className="font-medium text-gray-900">
                        {doc.document_name}
                      </h4>
                      <p className="text-sm text-gray-500">
                        {doc.chunk_count} chunks
                      </p>
                    </div>
                  </div>
                  <span className={`status-badge ${getStatusColor(doc.status)}`}>
                    {doc.status}
                  </span>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Chunks:</span>
                    <span className="ml-2 text-gray-600">{doc.chunk_count}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Last Updated:</span>
                    <span className="ml-2 text-gray-600">
                      {formatDate(doc.last_updated)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="flex items-center space-x-2 text-blue-700 mb-3">
          <FileText className="w-5 h-5" />
          <span className="font-medium">About Document Processing</span>
        </div>
        <ul className="text-blue-600 space-y-1 text-sm">
          <li>• Documents are automatically processed when the system starts</li>
          <li>• Each document is split into semantic chunks for better retrieval</li>
          <li>• Use "Reload Documents" to reprocess after document updates</li>
          <li>• Processing time depends on document size and complexity</li>
        </ul>
      </div>
    </div>
  );
};

export default DocumentStatus; 