import React, { useState } from 'react';
import { 
  ArrowRight, 
  Database, 
  Brain, 
  FileText, 
  Search, 
  Zap, 
  Shield, 
  Settings,
  CheckCircle,
  AlertTriangle,
  Info,
  Code,
  Users,
  Workflow,
  GitBranch,
  Server,
  Eye,
  ChevronDown,
  ChevronRight
} from 'lucide-react';
import SystemDiagram from './SystemDiagram';

const HowItWorks = () => {
  const [activeSection, setActiveSection] = useState('overview');
  const [expandedFlow, setExpandedFlow] = useState(null);

  const sections = [
    { id: 'overview', label: 'System Overview', icon: Eye },
    { id: 'architecture', label: 'Technical Architecture', icon: Server },
    { id: 'workflow', label: 'Data Processing Flow', icon: Workflow },
    { id: 'rag-flow', label: 'RAG Vector Embedding Flow', icon: GitBranch },
    { id: 'compliance', label: 'Compliance Checking', icon: Shield },
    { id: 'technical', label: 'Technical Implementation', icon: Code },
    { id: 'requirements', label: 'Business Requirements', icon: Users }
  ];

  const FlowDiagram = ({ title, steps, type = 'horizontal' }) => {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">{title}</h4>
        <div className={`flex ${type === 'vertical' ? 'flex-col' : 'flex-row items-center'} gap-4`}>
          {steps.map((step, index) => (
            <React.Fragment key={index}>
              <div className="flex-1">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
                  <div className="flex items-center justify-center w-12 h-12 bg-blue-600 rounded-full mx-auto mb-3">
                    <step.icon className="w-6 h-6 text-white" />
                  </div>
                  <h5 className="font-semibold text-gray-900 mb-2">{step.title}</h5>
                  <p className="text-sm text-gray-600">{step.description}</p>
                </div>
              </div>
              {index < steps.length - 1 && (
                <ArrowRight className="w-6 h-6 text-gray-400 flex-shrink-0" />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    );
  };

  const ExpandableSection = ({ title, children, id }) => {
    const isExpanded = expandedFlow === id;
    return (
      <div className="border border-gray-200 rounded-lg mb-4">
        <button
          onClick={() => setExpandedFlow(isExpanded ? null : id)}
          className="w-full flex items-center justify-between p-4 text-left hover:bg-gray-50"
        >
          <span className="font-semibold text-gray-900">{title}</span>
          {isExpanded ? (
            <ChevronDown className="w-5 h-5 text-gray-500" />
          ) : (
            <ChevronRight className="w-5 h-5 text-gray-500" />
          )}
        </button>
        {isExpanded && (
          <div className="px-4 pb-4 border-t border-gray-200">
            {children}
          </div>
        )}
      </div>
    );
  };

  const renderOverview = () => (
    <div>
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg text-white p-8 mb-8">
        <h2 className="text-3xl font-bold mb-4">RegReportRAG System</h2>
        <p className="text-xl text-blue-100 mb-6">
          AI-Powered Regulatory Compliance Analysis using Retrieval-Augmented Generation
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white/10 rounded-lg p-4">
            <Brain className="w-8 h-8 text-blue-200 mb-3" />
            <h3 className="font-semibold mb-2">AI-Powered Analysis</h3>
            <p className="text-sm text-blue-100">
              Uses OpenAI GPT-4 and vector embeddings for intelligent document analysis
            </p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <Database className="w-8 h-8 text-blue-200 mb-3" />
            <h3 className="font-semibold mb-2">Vector Database</h3>
            <p className="text-sm text-blue-100">
              PostgreSQL with pgvector for semantic search and similarity matching
            </p>
          </div>
          <div className="bg-white/10 rounded-lg p-4">
            <Shield className="w-8 h-8 text-blue-200 mb-3" />
            <h3 className="font-semibold mb-2">Compliance Focus</h3>
            <p className="text-sm text-blue-100">
              Specialized for regulatory document analysis and compliance checking
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Key Capabilities</h3>
          <ul className="space-y-3">
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Intelligent document processing with semantic chunking</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Real-time compliance checking against regulatory documents</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Contextual reasoning with detailed explanations</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Vector-based similarity search for relevant content retrieval</span>
            </li>
          </ul>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Use Cases</h3>
          <ul className="space-y-3">
            <li className="flex items-start">
              <Info className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Regulatory compliance auditing and assessment</span>
            </li>
            <li className="flex items-start">
              <Info className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Policy validation against regulatory requirements</span>
            </li>
            <li className="flex items-start">
              <Info className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Risk assessment and gap analysis</span>
            </li>
            <li className="flex items-start">
              <Info className="w-5 h-5 text-blue-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">Automated compliance reporting and documentation</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );

  const renderArchitecture = () => (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Technical Architecture</h2>
      
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">System Components</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-blue-100 rounded-lg p-4 mb-3">
              <FileText className="w-8 h-8 text-blue-600 mx-auto" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Frontend</h4>
            <p className="text-sm text-gray-600">React.js with Tailwind CSS</p>
          </div>
          <div className="text-center">
            <div className="bg-green-100 rounded-lg p-4 mb-3">
              <Server className="w-8 h-8 text-green-600 mx-auto" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Backend API</h4>
            <p className="text-sm text-gray-600">FastAPI with Python</p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 rounded-lg p-4 mb-3">
              <Database className="w-8 h-8 text-purple-600 mx-auto" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Vector DB</h4>
            <p className="text-sm text-gray-600">PostgreSQL + pgvector</p>
          </div>
          <div className="text-center">
            <div className="bg-orange-100 rounded-lg p-4 mb-3">
              <Brain className="w-8 h-8 text-orange-600 mx-auto" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">AI Engine</h4>
            <p className="text-sm text-gray-600">OpenAI GPT-4 + Embeddings</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Technology Stack</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Backend Technologies</h4>
            <ul className="space-y-2 text-gray-700">
              <li>• <strong>FastAPI:</strong> High-performance Python web framework</li>
              <li>• <strong>SQLAlchemy:</strong> Database ORM and query builder</li>
              <li>• <strong>Pydantic:</strong> Data validation and serialization</li>
              <li>• <strong>LangChain:</strong> Document processing and text splitting</li>
              <li>• <strong>PyPDF2:</strong> PDF text extraction</li>
              <li>• <strong>Uvicorn:</strong> ASGI server for production deployment</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Frontend Technologies</h4>
            <ul className="space-y-2 text-gray-700">
              <li>• <strong>React.js:</strong> Component-based UI library</li>
              <li>• <strong>React Router:</strong> Client-side routing</li>
              <li>• <strong>Tailwind CSS:</strong> Utility-first CSS framework</li>
              <li>• <strong>Lucide React:</strong> Modern icon library</li>
              <li>• <strong>Axios:</strong> HTTP client for API communication</li>
            </ul>
          </div>
        </div>
      </div>

      <SystemDiagram />
    </div>
  );

  const renderWorkflow = () => (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Data Processing Workflow</h2>
      
      <ExpandableSection title="1. Document Ingestion & Processing" id="ingestion">
        <FlowDiagram
          title="Document Processing Pipeline"
          steps={[
            {
              icon: FileText,
              title: "PDF Upload",
              description: "Regulatory documents (Instructions.pdf, Rules.pdf) are processed"
            },
            {
              icon: Search,
              title: "Text Extraction",
              description: "PyPDF2 extracts text content from each page"
            },
            {
              icon: GitBranch,
              title: "Semantic Chunking",
              description: "LangChain splits text into meaningful chunks with overlap"
            },
            {
              icon: Brain,
              title: "Classification",
              description: "AI categorizes chunks by type (rules, procedures, definitions)"
            }
          ]}
        />
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <h5 className="font-semibold text-blue-900 mb-2">Processing Details:</h5>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Chunk size: 1000 tokens with 200 token overlap</li>
            <li>• Automatic content classification (regulatory_rule, procedure, requirement, etc.)</li>
            <li>• Metadata extraction (page numbers, document names, file hashes)</li>
            <li>• Change detection using MD5 hashing</li>
          </ul>
        </div>
      </ExpandableSection>

      <ExpandableSection title="2. Vector Embedding Generation" id="embedding">
        <FlowDiagram
          title="Embedding Pipeline"
          steps={[
            {
              icon: FileText,
              title: "Text Chunks",
              description: "Processed document chunks ready for embedding"
            },
            {
              icon: Brain,
              title: "OpenAI API",
              description: "text-embedding-3-small model generates 1536-dim vectors"
            },
            {
              icon: Database,
              title: "Vector Storage",
              description: "Embeddings stored in PostgreSQL with pgvector"
            },
            {
              icon: Search,
              title: "Index Creation",
              description: "Vector similarity indexes for fast retrieval"
            }
          ]}
        />
        <div className="mt-4 p-4 bg-green-50 rounded-lg">
          <h5 className="font-semibold text-green-900 mb-2">Embedding Specifications:</h5>
          <ul className="text-sm text-green-800 space-y-1">
            <li>• Model: OpenAI text-embedding-3-small</li>
            <li>• Dimensions: 1536 per vector</li>
            <li>• Storage: PostgreSQL ARRAY(Float) with pgvector extension</li>
            <li>• Similarity: Cosine similarity for semantic matching</li>
          </ul>
        </div>
      </ExpandableSection>

      <ExpandableSection title="3. Query Processing & Retrieval" id="retrieval">
        <FlowDiagram
          title="Query Processing Flow"
          steps={[
            {
              icon: Search,
              title: "User Query",
              description: "Compliance question or concern submitted"
            },
            {
              icon: Brain,
              title: "Query Embedding",
              description: "Convert query to vector using same embedding model"
            },
            {
              icon: Database,
              title: "Similarity Search",
              description: "Find most relevant document chunks using vector similarity"
            },
            {
              icon: Zap,
              title: "Context Assembly",
              description: "Combine retrieved chunks with user query for LLM"
            }
          ]}
        />
        <div className="mt-4 p-4 bg-purple-50 rounded-lg">
          <h5 className="font-semibold text-purple-900 mb-2">Retrieval Strategy:</h5>
          <ul className="text-sm text-purple-800 space-y-1">
            <li>• Hybrid search combining semantic similarity and metadata filtering</li>
            <li>• Top-k retrieval (configurable, default 10 chunks)</li>
            <li>• Content type filtering (regulatory_rule, procedure, etc.)</li>
            <li>• Relevance scoring and ranking</li>
          </ul>
        </div>
      </ExpandableSection>

      <ExpandableSection title="4. AI Analysis & Response Generation" id="analysis">
        <FlowDiagram
          title="AI Analysis Pipeline"
          steps={[
            {
              icon: Brain,
              title: "Context Formation",
              description: "Combine query with retrieved regulatory content"
            },
            {
              icon: Settings,
              title: "LLM Processing",
              description: "GPT-4 analyzes compliance against regulations"
            },
            {
              icon: CheckCircle,
              title: "Structured Response",
              description: "Generate compliance status, reasoning, and recommendations"
            },
            {
              icon: Shield,
              title: "Validation",
              description: "Confidence scoring and response validation"
            }
          ]}
        />
        <div className="mt-4 p-4 bg-orange-50 rounded-lg">
          <h5 className="font-semibold text-orange-900 mb-2">Analysis Components:</h5>
          <ul className="text-sm text-orange-800 space-y-1">
            <li>• Compliance status determination (compliant/non-compliant/partial/review)</li>
            <li>• Confidence scoring (0-1 scale)</li>
            <li>• Detailed reasoning with specific rule references</li>
            <li>• Actionable recommendations for compliance</li>
          </ul>
        </div>
      </ExpandableSection>
    </div>
  );

  const renderRAGFlow = () => (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">RAG Vector Embedding Flow</h2>
      
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg text-white p-6 mb-8">
        <h3 className="text-2xl font-bold mb-4">Understanding RAG: From Document to Answer</h3>
        <p className="text-lg mb-4">
          Retrieval-Augmented Generation (RAG) combines the power of vector embeddings with large language models 
          to provide accurate, contextual answers based on your documents.
        </p>
        <div className="bg-white/10 rounded-lg p-4">
          <p className="text-sm">
            <strong>The Process:</strong> Documents → Chunks → Embeddings → Vector Database → Query → Retrieval → AI Analysis → Response
          </p>
        </div>
      </div>

      <ExpandableSection title="Step 1: Document Chunking Strategy" id="chunking">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Intelligent Text Segmentation</h4>
          <p className="text-gray-700 mb-4">
            Our system doesn't simply split documents randomly. Instead, it uses advanced semantic chunking 
            to preserve meaning and context across document segments.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h5 className="font-semibold text-blue-900 mb-3">Chunking Parameters</h5>
              <ul className="text-sm text-blue-800 space-y-2">
                <li>• <strong>Chunk Size:</strong> 1000 tokens (≈750 words)</li>
                <li>• <strong>Overlap:</strong> 200 tokens (≈150 words)</li>
                <li>• <strong>Tokenizer:</strong> tiktoken (cl100k_base)</li>
                <li>• <strong>Splitter:</strong> RecursiveCharacterTextSplitter</li>
              </ul>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h5 className="font-semibold text-green-900 mb-3">Splitting Hierarchy</h5>
              <ul className="text-sm text-green-800 space-y-2">
                <li>1. <strong>Paragraph breaks</strong> (\\n\\n)</li>
                <li>2. <strong>Line breaks</strong> (\\n)</li>
                <li>3. <strong>Sentence endings</strong> (. ? !)</li>
                <li>4. <strong>Punctuation</strong> (; ,)</li>
                <li>5. <strong>Spaces</strong> ( )</li>
                <li>6. <strong>Character level</strong> (last resort)</li>
              </ul>
            </div>
          </div>
          
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h5 className="font-semibold text-yellow-900 mb-2">🧠 Why Overlap Matters</h5>
            <p className="text-sm text-yellow-800">
              The 200-token overlap ensures that important context isn't lost at chunk boundaries. 
              This means regulatory rules that span multiple chunks remain coherent and searchable.
            </p>
          </div>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Step 2: Semantic Classification" id="classification">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Automatic Content Categorization</h4>
          <p className="text-gray-700 mb-4">
            Each chunk is automatically classified to improve retrieval accuracy and enable targeted searches.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
              <Shield className="w-8 h-8 text-red-600 mx-auto mb-2" />
              <h5 className="font-semibold text-red-900 mb-2">Regulatory Rules</h5>
              <p className="text-sm text-red-800">Sections, articles, rules, regulations</p>
            </div>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-center">
              <Settings className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <h5 className="font-semibold text-blue-900 mb-2">Procedures</h5>
              <p className="text-sm text-blue-800">Processes, steps, methods</p>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
              <AlertTriangle className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <h5 className="font-semibold text-green-900 mb-2">Requirements</h5>
              <p className="text-sm text-green-800">Must, shall, mandatory items</p>
            </div>
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 text-center">
              <Info className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <h5 className="font-semibold text-purple-900 mb-2">Definitions</h5>
              <p className="text-sm text-purple-800">Terms, meanings, glossary</p>
            </div>
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4 text-center">
              <FileText className="w-8 h-8 text-orange-600 mx-auto mb-2" />
              <h5 className="font-semibold text-orange-900 mb-2">Examples</h5>
              <p className="text-sm text-orange-800">Case studies, instances</p>
            </div>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center">
              <Zap className="w-8 h-8 text-gray-600 mx-auto mb-2" />
              <h5 className="font-semibold text-gray-900 mb-2">Schedules</h5>
              <p className="text-sm text-gray-800">Timelines, deadlines, dates</p>
            </div>
          </div>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Step 3: Vector Embedding Generation" id="embeddings">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Converting Text to Mathematical Vectors</h4>
          <p className="text-gray-700 mb-4">
            Each text chunk is converted into a high-dimensional vector that captures its semantic meaning. 
            This allows the system to understand context and find related content even when exact words don't match.
          </p>
          
          <FlowDiagram
            title="Embedding Generation Process"
            steps={[
              {
                icon: FileText,
                title: "Text Chunk",
                description: "Clean, classified document segment"
              },
              {
                icon: Brain,
                title: "OpenAI API",
                description: "text-embedding-3-small model"
              },
              {
                icon: Database,
                title: "1536-D Vector",
                description: "Mathematical representation of meaning"
              },
              {
                icon: Search,
                title: "Similarity Index",
                description: "Optimized for fast retrieval"
              }
            ]}
          />
          
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h5 className="font-semibold text-blue-900 mb-3">Technical Specifications</h5>
              <ul className="text-sm text-blue-800 space-y-2">
                <li>• <strong>Model:</strong> text-embedding-3-small</li>
                <li>• <strong>Dimensions:</strong> 1536 per vector</li>
                <li>• <strong>Context Length:</strong> 8192 tokens</li>
                <li>• <strong>Similarity Metric:</strong> Cosine similarity</li>
                <li>• <strong>Performance:</strong> 62.3% on MTEB benchmark</li>
              </ul>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h5 className="font-semibold text-green-900 mb-3">Vector Properties</h5>
              <ul className="text-sm text-green-800 space-y-2">
                <li>• <strong>Semantic Similarity:</strong> Similar concepts have similar vectors</li>
                <li>• <strong>Dimension Reduction:</strong> Complex ideas → 1536 numbers</li>
                <li>• <strong>Language Agnostic:</strong> Captures meaning beyond exact words</li>
                <li>• <strong>Contextual:</strong> Same word, different contexts = different vectors</li>
              </ul>
            </div>
          </div>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Step 4: PostgreSQL Vector Database Storage" id="storage">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Efficient Vector Storage & Indexing</h4>
          <p className="text-gray-700 mb-4">
            We use PostgreSQL with the pgvector extension for storing and querying high-dimensional vectors. 
            This provides both relational data management and vector similarity search in one system.
          </p>
          
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
            <h5 className="font-semibold text-gray-900 mb-3">Database Schema</h5>
            <div className="bg-white rounded border p-3 font-mono text-sm">
              <div className="text-blue-600">CREATE TABLE document_chunks (</div>
              <div className="ml-4 text-gray-700">
                <div>chunk_id VARCHAR PRIMARY KEY,</div>
                <div>document_name VARCHAR NOT NULL,</div>
                <div>content TEXT NOT NULL,</div>
                <div>chunk_type VARCHAR,</div>
                <div>page_number INTEGER,</div>
                <div>file_hash VARCHAR,</div>
                <div><span className="text-red-600">embedding VECTOR(1536)</span> NOT NULL,</div>
                <div>chunk_metadata JSONB,</div>
                <div>created_at TIMESTAMP DEFAULT NOW()</div>
              </div>
              <div className="text-blue-600">);</div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h5 className="font-semibold text-purple-900 mb-3">Vector Operations</h5>
              <ul className="text-sm text-purple-800 space-y-2">
                <li>• <strong>Cosine Distance:</strong> embedding &lt;=&gt; query_vector</li>
                <li>• <strong>Euclidean Distance:</strong> embedding &lt;-&gt; query_vector</li>
                <li>• <strong>Inner Product:</strong> embedding &lt;#&gt; query_vector</li>
                <li>• <strong>Indexing:</strong> HNSW for approximate search</li>
              </ul>
            </div>
            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <h5 className="font-semibold text-orange-900 mb-3">Performance Features</h5>
              <ul className="text-sm text-orange-800 space-y-2">
                <li>• <strong>HNSW Index:</strong> Hierarchical Navigable Small World</li>
                <li>• <strong>Parallel Search:</strong> Multi-core vector operations</li>
                <li>• <strong>Memory Efficiency:</strong> Optimized storage format</li>
                <li>• <strong>ACID Compliance:</strong> Full transactional support</li>
              </ul>
            </div>
          </div>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Step 5: Query Processing & Retrieval" id="query-retrieval">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Semantic Search & Context Retrieval</h4>
          <p className="text-gray-700 mb-4">
            When you ask a question, the system converts your query into a vector and finds the most semantically 
            similar document chunks to provide relevant context for the AI analysis.
          </p>
          
          <FlowDiagram
            title="Query Processing Pipeline"
            type="vertical"
            steps={[
              {
                icon: Search,
                title: "User Query",
                description: "Natural language compliance question"
              },
              {
                icon: Brain,
                title: "Query Embedding",
                description: "Convert query to 1536-dimensional vector"
              },
              {
                icon: Database,
                title: "Vector Similarity Search",
                description: "Find top-k most similar document chunks"
              },
              {
                icon: Settings,
                title: "Hybrid Filtering",
                description: "Combine semantic search with metadata filters"
              },
              {
                icon: Zap,
                title: "Context Assembly",
                description: "Rank and combine relevant chunks"
              }
            ]}
          />
          
          <div className="mt-6 bg-indigo-50 border border-indigo-200 rounded-lg p-4">
            <h5 className="font-semibold text-indigo-900 mb-3">🔍 Search Strategy</h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h6 className="font-medium text-indigo-800 mb-2">Semantic Search</h6>
                <ul className="text-sm text-indigo-700 space-y-1">
                  <li>• Cosine similarity matching</li>
                  <li>• Context-aware retrieval</li>
                  <li>• Handles synonyms and paraphrases</li>
                  <li>• Relevance scoring</li>
                </ul>
              </div>
              <div>
                <h6 className="font-medium text-indigo-800 mb-2">Metadata Filtering</h6>
                <ul className="text-sm text-indigo-700 space-y-1">
                  <li>• Content type filtering</li>
                  <li>• Document source filtering</li>
                  <li>• Page number constraints</li>
                  <li>• Custom metadata queries</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Step 6: AI Analysis & Response Generation" id="ai-analysis">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Contextual AI Reasoning</h4>
          <p className="text-gray-700 mb-4">
            The retrieved context is combined with your query and sent to GPT-4 for analysis. 
            The AI provides structured compliance assessments with detailed reasoning.
          </p>
          
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 mb-4">
            <h5 className="font-semibold text-gray-900 mb-3">Prompt Engineering</h5>
            <div className="bg-white rounded border p-3 font-mono text-sm">
              <div className="text-green-600">// System Prompt</div>
              <div className="text-gray-700 mb-2">You are a regulatory compliance expert...</div>
              <div className="text-green-600">// User Query</div>
              <div className="text-gray-700 mb-2">CONCERN: {'{user_question}'}</div>
              <div className="text-green-600">// Retrieved Context</div>
              <div className="text-gray-700">RELEVANT REGULATIONS: {'{retrieved_chunks}'}</div>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h5 className="font-semibold text-blue-900 mb-3">Structured Response</h5>
              <ul className="text-sm text-blue-800 space-y-2">
                <li>• <strong>Compliance Status:</strong> Compliant/Non-compliant/Partial/Review</li>
                <li>• <strong>Confidence Score:</strong> 0-1 numerical confidence</li>
                <li>• <strong>Summary:</strong> Executive summary of findings</li>
                <li>• <strong>Reasoning:</strong> Detailed analysis and logic</li>
              </ul>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h5 className="font-semibold text-green-900 mb-3">Actionable Insights</h5>
              <ul className="text-sm text-green-800 space-y-2">
                <li>• <strong>Impacted Rules:</strong> Specific regulatory references</li>
                <li>• <strong>Recommendations:</strong> Steps to achieve compliance</li>
                <li>• <strong>Risk Assessment:</strong> Impact levels and priorities</li>
                <li>• <strong>Deadlines:</strong> Time-sensitive requirements</li>
              </ul>
            </div>
          </div>
        </div>
      </ExpandableSection>

      <ExpandableSection title="Complete RAG Flow Example" id="example">
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">Real-World Example</h4>
          <p className="text-gray-700 mb-4">
            Let's trace through a complete RAG flow with a real compliance question:
          </p>
          
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h5 className="font-semibold text-blue-900 mb-2">1. User Query</h5>
              <div className="bg-white rounded border p-3 italic text-gray-700">
                "Do I need to conduct background checks on all employees who handle financial data?"
              </div>
            </div>
            
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h5 className="font-semibold text-green-900 mb-2">2. Vector Search Results</h5>
              <div className="bg-white rounded border p-3 text-sm">
                <div className="mb-2"><strong>Chunk 1 (0.89 similarity):</strong> "Section 4.2: Employee Screening Requirements - All personnel with access to sensitive financial information must undergo comprehensive background verification..."</div>
                <div className="mb-2"><strong>Chunk 2 (0.84 similarity):</strong> "Background Check Procedures - The organization shall implement screening protocols for positions involving financial data access..."</div>
                <div><strong>Chunk 3 (0.78 similarity):</strong> "Data Access Controls - Personnel authorized to handle financial records must meet security clearance requirements..."</div>
              </div>
            </div>
            
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h5 className="font-semibold text-purple-900 mb-2">3. AI Analysis Response</h5>
              <div className="bg-white rounded border p-3 text-sm">
                <div className="mb-2"><strong>Status:</strong> <span className="text-red-600">Non-Compliant</span></div>
                <div className="mb-2"><strong>Confidence:</strong> 0.92</div>
                <div className="mb-2"><strong>Summary:</strong> Background checks are mandatory for all employees handling financial data per Section 4.2.</div>
                <div><strong>Recommendation:</strong> Implement comprehensive background verification procedures for all relevant personnel within 30 days.</div>
              </div>
            </div>
          </div>
        </div>
      </ExpandableSection>
    </div>
  );

  const renderCompliance = () => (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Compliance Checking Process</h2>
      
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Compliance Analysis Framework</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="border border-green-200 rounded-lg p-4 bg-green-50">
              <div className="flex items-center mb-2">
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                <span className="font-semibold text-green-900">Compliant</span>
              </div>
              <p className="text-sm text-green-800">
                Query fully aligns with regulatory requirements. No violations detected.
              </p>
            </div>
            <div className="border border-red-200 rounded-lg p-4 bg-red-50">
              <div className="flex items-center mb-2">
                <AlertTriangle className="w-5 h-5 text-red-600 mr-2" />
                <span className="font-semibold text-red-900">Non-Compliant</span>
              </div>
              <p className="text-sm text-red-800">
                Clear violations of regulatory requirements identified with specific rule references.
              </p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="border border-yellow-200 rounded-lg p-4 bg-yellow-50">
              <div className="flex items-center mb-2">
                <Info className="w-5 h-5 text-yellow-600 mr-2" />
                <span className="font-semibold text-yellow-900">Partial Compliance</span>
              </div>
              <p className="text-sm text-yellow-800">
                Some requirements met, but gaps or ambiguities exist requiring attention.
              </p>
            </div>
            <div className="border border-blue-200 rounded-lg p-4 bg-blue-50">
              <div className="flex items-center mb-2">
                <Search className="w-5 h-5 text-blue-600 mr-2" />
                <span className="font-semibold text-blue-900">Requires Review</span>
              </div>
              <p className="text-sm text-blue-800">
                Insufficient information or complex scenarios requiring human expert review.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Analysis Output Structure</h3>
        <div className="bg-gray-50 rounded-lg p-4">
          <pre className="text-sm text-gray-800 overflow-x-auto">
{`{
  "status": "compliant|non_compliant|partial_compliance|requires_review",
  "confidence_score": 0.95,
  "summary": "Brief assessment summary",
  "impacted_rules": ["Rule 1.2.3", "Section 4.5"],
  "reasoning": "Detailed analysis explanation",
  "compliance_details": [
    {
      "rule_reference": "Section 1.2.3",
      "description": "Specific requirement description",
      "impact_level": "high|medium|low",
      "required_action": "Action needed if applicable",
      "deadline": "Compliance deadline if applicable"
    }
  ],
  "recommendations": ["List of actionable recommendations"],
  "relevant_documents": [
    {
      "document_name": "Instructions.pdf",
      "section": "Page 15",
      "content": "Relevant regulatory text",
      "relevance_score": 0.89
    }
  ]
}`}
          </pre>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Quality Assurance</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
              <Brain className="w-8 h-8 text-blue-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">AI Confidence Scoring</h4>
            <p className="text-sm text-gray-600">
              Each analysis includes confidence metrics to indicate reliability
            </p>
          </div>
          <div className="text-center">
            <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Source Attribution</h4>
            <p className="text-sm text-gray-600">
              All conclusions linked to specific regulatory document sections
            </p>
          </div>
          <div className="text-center">
            <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
              <Shield className="w-8 h-8 text-purple-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Audit Trail</h4>
            <p className="text-sm text-gray-600">
              Complete processing logs and decision rationale maintained
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTechnical = () => (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Technical Implementation</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">API Endpoints</h3>
          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-sm font-semibold">POST /api/v1/compliance/check</span>
                <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Primary</span>
              </div>
              <p className="text-sm text-gray-600">Main compliance checking endpoint</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-sm font-semibold">GET /api/v1/documents/status</span>
                <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">Status</span>
              </div>
              <p className="text-sm text-gray-600">Document processing status and statistics</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-sm font-semibold">POST /api/v1/documents/reload</span>
                <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded">Admin</span>
              </div>
              <p className="text-sm text-gray-600">Reload and reprocess documents</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Database Schema</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-semibold text-gray-900 mb-2">document_chunks</h4>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• <strong>id:</strong> Primary key</li>
              <li>• <strong>chunk_id:</strong> Unique chunk identifier</li>
              <li>• <strong>document_name:</strong> Source document</li>
              <li>• <strong>content:</strong> Text content</li>
              <li>• <strong>chunk_type:</strong> Content classification</li>
              <li>• <strong>page_number:</strong> Source page</li>
              <li>• <strong>embedding:</strong> 1536-dim vector</li>
              <li>• <strong>chunk_metadata:</strong> Additional metadata</li>
              <li>• <strong>file_hash:</strong> Change detection</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Performance Characteristics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">~2-5s</div>
            <div className="text-sm text-gray-600">Average query response time</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">145</div>
            <div className="text-sm text-gray-600">Document chunks processed</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">1536</div>
            <div className="text-sm text-gray-600">Vector dimensions per chunk</div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Deployment & Scaling</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Development Setup</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Local PostgreSQL with pgvector extension</li>
              <li>• Python virtual environment with FastAPI</li>
              <li>• React development server</li>
              <li>• Environment-based configuration</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-3">Production Considerations</h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Docker containerization support</li>
              <li>• Database connection pooling</li>
              <li>• API rate limiting and caching</li>
              <li>• Comprehensive logging and monitoring</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRequirements = () => (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Business Requirements & Use Cases</h2>
      
      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Primary Business Objectives</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <Shield className="w-5 h-5 text-blue-600 mr-2" />
              Compliance Assurance
            </h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Automated compliance checking against regulatory documents</li>
              <li>• Real-time validation of policies and procedures</li>
              <li>• Gap analysis and risk identification</li>
              <li>• Audit trail maintenance for regulatory reviews</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
              <Zap className="w-5 h-5 text-green-600 mr-2" />
              Operational Efficiency
            </h4>
            <ul className="text-sm text-gray-700 space-y-2">
              <li>• Reduce manual compliance review time by 80%</li>
              <li>• Instant access to relevant regulatory information</li>
              <li>• Standardized compliance assessment process</li>
              <li>• Scalable analysis across multiple documents</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Target User Personas</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="border border-gray-200 rounded-lg p-4">
            <div className="bg-blue-100 rounded-full w-12 h-12 flex items-center justify-center mb-3">
              <Users className="w-6 h-6 text-blue-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Compliance Officers</h4>
            <p className="text-sm text-gray-600 mb-3">
              Primary users responsible for regulatory compliance oversight
            </p>
            <ul className="text-xs text-gray-600 space-y-1">
              <li>• Daily compliance monitoring</li>
              <li>• Audit preparation and response</li>
              <li>• Policy validation and updates</li>
            </ul>
          </div>
          <div className="border border-gray-200 rounded-lg p-4">
            <div className="bg-green-100 rounded-full w-12 h-12 flex items-center justify-center mb-3">
              <Shield className="w-6 h-6 text-green-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Risk Managers</h4>
            <p className="text-sm text-gray-600 mb-3">
              Assess and mitigate regulatory and operational risks
            </p>
            <ul className="text-xs text-gray-600 space-y-1">
              <li>• Risk assessment and analysis</li>
              <li>• Regulatory change impact evaluation</li>
              <li>• Compliance gap identification</li>
            </ul>
          </div>
          <div className="border border-gray-200 rounded-lg p-4">
            <div className="bg-purple-100 rounded-full w-12 h-12 flex items-center justify-center mb-3">
              <FileText className="w-6 h-6 text-purple-600" />
            </div>
            <h4 className="font-semibold text-gray-900 mb-2">Legal Teams</h4>
            <p className="text-sm text-gray-600 mb-3">
              Ensure legal compliance and regulatory adherence
            </p>
            <ul className="text-xs text-gray-600 space-y-1">
              <li>• Legal document review</li>
              <li>• Regulatory interpretation</li>
              <li>• Compliance documentation</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Use Case Scenarios</h3>
        <div className="space-y-6">
          <div className="border-l-4 border-blue-500 pl-4">
            <h4 className="font-semibold text-gray-900 mb-2">Scenario 1: Policy Validation</h4>
            <p className="text-gray-700 mb-2">
              <strong>Context:</strong> A new internal policy is being developed for data handling procedures.
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Process:</strong> The policy text is submitted to the system for compliance checking against regulatory requirements.
            </p>
            <p className="text-gray-700">
              <strong>Outcome:</strong> System identifies specific regulatory sections that apply, highlights potential gaps, and provides recommendations for compliance.
            </p>
          </div>
          
          <div className="border-l-4 border-green-500 pl-4">
            <h4 className="font-semibold text-gray-900 mb-2">Scenario 2: Audit Preparation</h4>
            <p className="text-gray-700 mb-2">
              <strong>Context:</strong> Preparing for a regulatory audit requiring evidence of compliance with specific regulations.
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Process:</strong> Audit questions and current practices are analyzed against the regulatory database.
            </p>
            <p className="text-gray-700">
              <strong>Outcome:</strong> Comprehensive compliance report with supporting documentation and identified areas for improvement.
            </p>
          </div>
          
          <div className="border-l-4 border-purple-500 pl-4">
            <h4 className="font-semibold text-gray-900 mb-2">Scenario 3: Regulatory Change Impact</h4>
            <p className="text-gray-700 mb-2">
              <strong>Context:</strong> New regulatory requirements are introduced, requiring assessment of current compliance status.
            </p>
            <p className="text-gray-700 mb-2">
              <strong>Process:</strong> Updated regulatory documents are processed, and existing policies are re-evaluated.
            </p>
            <p className="text-gray-700">
              <strong>Outcome:</strong> Gap analysis report identifying what changes are needed to maintain compliance.
            </p>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Success Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 mb-1">80%</div>
            <div className="text-sm text-gray-600">Reduction in manual review time</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600 mb-1">95%</div>
            <div className="text-sm text-gray-600">Accuracy in compliance detection</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600 mb-1">24/7</div>
            <div className="text-sm text-gray-600">Availability for compliance checks</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600 mb-1">100%</div>
            <div className="text-sm text-gray-600">Audit trail completeness</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderContent = () => {
    switch (activeSection) {
      case 'overview': return renderOverview();
      case 'architecture': return renderArchitecture();
      case 'workflow': return renderWorkflow();
      case 'rag-flow': return renderRAGFlow();
      case 'compliance': return renderCompliance();
      case 'technical': return renderTechnical();
      case 'requirements': return renderRequirements();
      default: return renderOverview();
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">How RegReportRAG Works</h1>
        <p className="text-lg text-gray-600">
          Comprehensive guide to understanding the AI-powered regulatory compliance analysis system
        </p>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Navigation Sidebar */}
        <div className="lg:w-64 flex-shrink-0">
          <div className="bg-white rounded-lg border border-gray-200 p-4 sticky top-4">
            <h3 className="font-semibold text-gray-900 mb-4">Navigation</h3>
            <nav className="space-y-1">
              {sections.map((section) => {
                const Icon = section.icon;
                return (
                  <button
                    key={section.id}
                    onClick={() => setActiveSection(section.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      activeSection === section.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{section.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default HowItWorks; 