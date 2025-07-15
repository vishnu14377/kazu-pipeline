import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SystemStats = () => {
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
        <p>Error loading statistics: {error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="section-title">System Statistics</h1>
          <p className="text-gray-600">Detailed metrics about your ontology system</p>
        </div>
        <button
          onClick={fetchStats}
          className="btn-primary"
        >
          🔄 Refresh Stats
        </button>
      </div>

      {/* Overview Cards */}
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

      {/* Health Score */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">System Health</h2>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mr-4">
              <span className="text-2xl">
                {stats?.valid_ontologies === stats?.total_ontologies ? '✅' : '⚠️'}
              </span>
            </div>
            <div>
              <h3 className="text-lg font-medium">
                {stats?.valid_ontologies === stats?.total_ontologies 
                  ? 'All Systems Operational' 
                  : 'Issues Detected'}
              </h3>
              <p className="text-gray-600">
                {stats?.valid_ontologies}/{stats?.total_ontologies} ontologies are valid
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-green-600">
              {stats?.total_ontologies > 0 
                ? Math.round((stats?.valid_ontologies / stats?.total_ontologies) * 100)
                : 0}%
            </div>
            <div className="text-sm text-gray-500">Health Score</div>
          </div>
        </div>
      </div>

      {/* Domain Breakdown */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">Domain Breakdown</h2>
        <div className="table-container">
          <table className="table">
            <thead className="table-header">
              <tr>
                <th>Domain</th>
                <th>Total Files</th>
                <th>Valid Files</th>
                <th>Total Triples</th>
                <th>Avg Triples/File</th>
                <th>Health</th>
              </tr>
            </thead>
            <tbody className="table-body">
              {stats?.ontology_domains?.map((domain, index) => (
                <tr key={index}>
                  <td className="font-medium">{domain.name}</td>
                  <td>{domain.count}</td>
                  <td>{domain.valid}</td>
                  <td>{domain.triples}</td>
                  <td>{domain.count > 0 ? Math.round(domain.triples / domain.count) : 0}</td>
                  <td>
                    <div className="flex items-center">
                      <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-green-600 h-2 rounded-full"
                          style={{ 
                            width: `${domain.count > 0 ? (domain.valid / domain.count) * 100 : 0}%` 
                          }}
                        ></div>
                      </div>
                      <span className="text-sm">
                        {domain.count > 0 ? Math.round((domain.valid / domain.count) * 100) : 0}%
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* System Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">System Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium text-gray-900 mb-2">Storage</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Ontology Files:</span>
                <span>{stats?.total_ontologies || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>RDF Triples:</span>
                <span>{stats?.total_triples || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Domains:</span>
                <span>{stats?.ontology_domains?.length || 0}</span>
              </div>
            </div>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-900 mb-2">Quality</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Valid Files:</span>
                <span className="text-green-600">{stats?.valid_ontologies || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Invalid Files:</span>
                <span className="text-red-600">{stats?.invalid_ontologies || 0}</span>
              </div>
              <div className="flex justify-between">
                <span>Success Rate:</span>
                <span className="text-blue-600">
                  {stats?.total_ontologies > 0 
                    ? Math.round((stats?.valid_ontologies / stats?.total_ontologies) * 100)
                    : 0}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemStats;