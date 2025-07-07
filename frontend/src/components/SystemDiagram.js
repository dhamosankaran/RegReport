import React from 'react';

const SystemDiagram = () => {
  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-xl font-semibold text-gray-900 mb-4">System Architecture Overview</h3>
      <div className="w-full overflow-x-auto">
        <svg viewBox="0 0 800 600" className="w-full h-auto max-w-4xl mx-auto">
          {/* Background */}
          <rect width="800" height="600" fill="#f8fafc" stroke="#e2e8f0" strokeWidth="2" rx="8"/>
          
          {/* User Layer */}
          <rect x="50" y="50" width="700" height="80" fill="#dbeafe" stroke="#3b82f6" strokeWidth="2" rx="8"/>
          <text x="400" y="80" textAnchor="middle" className="text-lg font-semibold" fill="#1e40af">
            User Interface Layer
          </text>
          <text x="400" y="105" textAnchor="middle" className="text-sm" fill="#3730a3">
            React Frontend • Tailwind CSS • Interactive Compliance Checker
          </text>
          
          {/* API Layer */}
          <rect x="50" y="170" width="700" height="80" fill="#dcfce7" stroke="#16a34a" strokeWidth="2" rx="8"/>
          <text x="400" y="200" textAnchor="middle" className="text-lg font-semibold" fill="#15803d">
            API Gateway Layer
          </text>
          <text x="400" y="225" textAnchor="middle" className="text-sm" fill="#166534">
            FastAPI • RESTful Endpoints • Request Validation • Response Formatting
          </text>
          
          {/* Processing Layer */}
          <rect x="50" y="290" width="700" height="120" fill="#fef3c7" stroke="#d97706" strokeWidth="2" rx="8"/>
          <text x="400" y="320" textAnchor="middle" className="text-lg font-semibold" fill="#92400e">
            AI Processing Layer
          </text>
          
          {/* Sub-components in Processing Layer */}
          <rect x="80" y="340" width="150" height="50" fill="#fed7aa" stroke="#ea580c" strokeWidth="1" rx="4"/>
          <text x="155" y="360" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Document
          </text>
          <text x="155" y="375" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Processor
          </text>
          
          <rect x="250" y="340" width="150" height="50" fill="#fed7aa" stroke="#ea580c" strokeWidth="1" rx="4"/>
          <text x="325" y="360" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Vector
          </text>
          <text x="325" y="375" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Service
          </text>
          
          <rect x="420" y="340" width="150" height="50" fill="#fed7aa" stroke="#ea580c" strokeWidth="1" rx="4"/>
          <text x="495" y="360" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            RAG
          </text>
          <text x="495" y="375" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Service
          </text>
          
          <rect x="590" y="340" width="130" height="50" fill="#fed7aa" stroke="#ea580c" strokeWidth="1" rx="4"/>
          <text x="655" y="360" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Compliance
          </text>
          <text x="655" y="375" textAnchor="middle" className="text-sm font-semibold" fill="#9a3412">
            Engine
          </text>
          
          {/* Data Layer */}
          <rect x="50" y="450" width="340" height="100" fill="#e0e7ff" stroke="#6366f1" strokeWidth="2" rx="8"/>
          <text x="220" y="480" textAnchor="middle" className="text-lg font-semibold" fill="#4338ca">
            Vector Database
          </text>
          <text x="220" y="505" textAnchor="middle" className="text-sm" fill="#3730a3">
            PostgreSQL + pgvector
          </text>
          <text x="220" y="525" textAnchor="middle" className="text-sm" fill="#3730a3">
            Document Chunks • Embeddings • Metadata
          </text>
          
          {/* External Services */}
          <rect x="410" y="450" width="340" height="100" fill="#fce7f3" stroke="#ec4899" strokeWidth="2" rx="8"/>
          <text x="580" y="480" textAnchor="middle" className="text-lg font-semibold" fill="#be185d">
            External AI Services
          </text>
          <text x="580" y="505" textAnchor="middle" className="text-sm" fill="#9d174d">
            OpenAI GPT-4 • Text Embeddings
          </text>
          <text x="580" y="525" textAnchor="middle" className="text-sm" fill="#9d174d">
            Natural Language Processing • Vector Generation
          </text>
          
          {/* Arrows showing data flow */}
          {/* User to API */}
          <path d="M 400 130 L 400 170" stroke="#374151" strokeWidth="2" markerEnd="url(#arrowhead)" fill="none"/>
          
          {/* API to Processing */}
          <path d="M 400 250 L 400 290" stroke="#374151" strokeWidth="2" markerEnd="url(#arrowhead)" fill="none"/>
          
          {/* Processing to Database */}
          <path d="M 300 410 L 250 450" stroke="#374151" strokeWidth="2" markerEnd="url(#arrowhead)" fill="none"/>
          
          {/* Processing to External Services */}
          <path d="M 500 410 L 550 450" stroke="#374151" strokeWidth="2" markerEnd="url(#arrowhead)" fill="none"/>
          
          {/* Arrow marker definition */}
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" 
             refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#374151" />
            </marker>
          </defs>
          
          {/* Data Flow Labels */}
          <text x="420" y="150" className="text-xs" fill="#6b7280">HTTP Requests</text>
          <text x="420" y="270" className="text-xs" fill="#6b7280">API Calls</text>
          <text x="200" y="430" className="text-xs" fill="#6b7280">Vector Storage</text>
          <text x="600" y="430" className="text-xs" fill="#6b7280">AI Processing</text>
        </svg>
      </div>
      
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-blue-50 rounded-lg p-3 text-center">
          <div className="w-4 h-4 bg-blue-500 rounded mx-auto mb-2"></div>
          <div className="text-sm font-semibold text-blue-900">Frontend Layer</div>
          <div className="text-xs text-blue-700">User Interface</div>
        </div>
        <div className="bg-green-50 rounded-lg p-3 text-center">
          <div className="w-4 h-4 bg-green-500 rounded mx-auto mb-2"></div>
          <div className="text-sm font-semibold text-green-900">API Layer</div>
          <div className="text-xs text-green-700">Request Processing</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-3 text-center">
          <div className="w-4 h-4 bg-yellow-500 rounded mx-auto mb-2"></div>
          <div className="text-sm font-semibold text-yellow-900">AI Processing</div>
          <div className="text-xs text-yellow-700">Intelligence Layer</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-3 text-center">
          <div className="w-4 h-4 bg-purple-500 rounded mx-auto mb-2"></div>
          <div className="text-sm font-semibold text-purple-900">Data Layer</div>
          <div className="text-xs text-purple-700">Storage & External APIs</div>
        </div>
      </div>
    </div>
  );
};

export default SystemDiagram; 