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
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <h1 className="text-2xl font-bold text-blue-600">dMaster</h1>
                  <p className="text-sm text-gray-500">Disease Mastery Ontology System</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setCurrentPage('dashboard')}
                  className={`px-4 py-2 rounded-md text-sm font-medium ${
                    currentPage === 'dashboard'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setCurrentPage('ontologies')}
                  className={`px-4 py-2 rounded-md text-sm font-medium ${
                    currentPage === 'ontologies'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Ontologies
                </button>
                <button
                  onClick={() => setCurrentPage('validation')}
                  className={`px-4 py-2 rounded-md text-sm font-medium ${
                    currentPage === 'validation'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Validation
                </button>
                <button
                  onClick={() => setCurrentPage('stats')}
                  className={`px-4 py-2 rounded-md text-sm font-medium ${
                    currentPage === 'stats'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Statistics
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 px-4">
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