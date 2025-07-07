import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import ComplianceChecker from './components/ComplianceChecker';
import DocumentStatus from './components/DocumentStatus';
import HowItWorks from './components/HowItWorks';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<ComplianceChecker />} />
            <Route path="/documents" element={<DocumentStatus />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 