import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import OntologyManager from './components/OntologyManager';
import ValidationTools from './components/ValidationTools';
import SystemStats from './components/SystemStats';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');

  return (
    <Router>
      <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
        {/* Navigation */}
        <nav style={{ 
          backgroundColor: 'white', 
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)', 
          borderBottom: '1px solid #e5e7eb' 
        }}>
          <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', height: '64px' }}>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <div>
                  <h1 style={{ 
                    fontSize: '24px', 
                    fontWeight: 'bold', 
                    color: '#2563eb', 
                    margin: 0 
                  }}>
                    dMaster
                  </h1>
                  <p style={{ 
                    fontSize: '14px', 
                    color: '#6b7280', 
                    margin: 0 
                  }}>
                    Disease Mastery Ontology System
                  </p>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <button
                  onClick={() => setCurrentPage('dashboard')}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '6px',
                    fontSize: '14px',
                    fontWeight: '500',
                    border: 'none',
                    cursor: 'pointer',
                    backgroundColor: currentPage === 'dashboard' ? '#dbeafe' : 'transparent',
                    color: currentPage === 'dashboard' ? '#1d4ed8' : '#6b7280'
                  }}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setCurrentPage('ontologies')}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '6px',
                    fontSize: '14px',
                    fontWeight: '500',
                    border: 'none',
                    cursor: 'pointer',
                    backgroundColor: currentPage === 'ontologies' ? '#dbeafe' : 'transparent',
                    color: currentPage === 'ontologies' ? '#1d4ed8' : '#6b7280'
                  }}
                >
                  Ontologies
                </button>
                <button
                  onClick={() => setCurrentPage('validation')}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '6px',
                    fontSize: '14px',
                    fontWeight: '500',
                    border: 'none',
                    cursor: 'pointer',
                    backgroundColor: currentPage === 'validation' ? '#dbeafe' : 'transparent',
                    color: currentPage === 'validation' ? '#1d4ed8' : '#6b7280'
                  }}
                >
                  Validation
                </button>
                <button
                  onClick={() => setCurrentPage('stats')}
                  style={{
                    padding: '8px 16px',
                    borderRadius: '6px',
                    fontSize: '14px',
                    fontWeight: '500',
                    border: 'none',
                    cursor: 'pointer',
                    backgroundColor: currentPage === 'stats' ? '#dbeafe' : 'transparent',
                    color: currentPage === 'stats' ? '#1d4ed8' : '#6b7280'
                  }}
                >
                  Statistics
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 16px' }}>
          {currentPage === 'dashboard' && <Dashboard />}
          {currentPage === 'ontologies' && <OntologyManager />}
          {currentPage === 'validation' && <ValidationTools />}
          {currentPage === 'stats' && <SystemStats />}
        </main>
      </div>
    </Router>
  );
}

export default App;