import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/stats');
      setStats(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-error">
        <p>Error loading dashboard: {error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="section-title">
        <h1>Dashboard</h1>
        <p className="text-gray-600 mt-2">Overview of your ontology system</p>
      </div>

      {/* Key Metrics */}
      <div className="stats-grid">
        <div className="metric-card">
          <div className="metric-value">{stats?.total_ontologies || 0}</div>
          <div className="metric-label">Total Ontologies</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{stats?.valid_ontologies || 0}</div>
          <div className="metric-label">Valid Ontologies</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{stats?.invalid_ontologies || 0}</div>
          <div className="metric-label">Invalid Ontologies</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{stats?.total_triples || 0}</div>
          <div className="metric-label">Total Triples</div>
        </div>
      </div>

      {/* Ontology Domains */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">Ontology Domains</h2>
        <div className="table-container">
          <table className="table">
            <thead className="table-header">
              <tr>
                <th>Domain</th>
                <th>Files</th>
                <th>Valid</th>
                <th>Triples</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody className="table-body">
              {stats?.ontology_domains?.map((domain, index) => (
                <tr key={index}>
                  <td className="font-medium">{domain.name}</td>
                  <td>{domain.count}</td>
                  <td>{domain.valid}</td>
                  <td>{domain.triples}</td>
                  <td>
                    <span className={`status-badge ${
                      domain.valid === domain.count ? 'status-valid' : 'status-invalid'
                    }`}>
                      {domain.valid === domain.count ? 'All Valid' : 'Has Issues'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn-primary">
            <span className="mr-2">🔍</span>
            Run Validation
          </button>
          <button className="btn-primary">
            <span className="mr-2">🔗</span>
            Combine Ontologies
          </button>
          <button className="btn-primary">
            <span className="mr-2">📊</span>
            View Statistics
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">System Status</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
            <span className="text-green-800">✅ All ontology syntax tests passed</span>
            <span className="text-green-600 text-sm">Just now</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
            <span className="text-blue-800">📊 System statistics updated</span>
            <span className="text-blue-600 text-sm">1 min ago</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span className="text-gray-800">🔄 Combined ontology available</span>
            <span className="text-gray-600 text-sm">5 min ago</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;