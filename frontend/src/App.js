import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const runValidation = async () => {
    try {
      setLoading(true);
      const response = await axios.post('/api/validate');
      alert(response.data.success ? 'Validation passed!' : 'Validation failed!');
    } catch (err) {
      alert('Error running validation');
    } finally {
      setLoading(false);
    }
  };

  const combineOntologies = async () => {
    try {
      setLoading(true);
      const response = await axios.post('/api/combine');
      alert(response.data.success ? 'Ontologies combined successfully!' : 'Failed to combine ontologies!');
    } catch (err) {
      alert('Error combining ontologies');
    } finally {
      setLoading(false);
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
      fontFamily: 'Arial, sans-serif'
    },
    header: {
      backgroundColor: '#2563eb',
      color: 'white',
      padding: '20px',
      textAlign: 'center'
    },
    title: {
      margin: 0,
      fontSize: '28px',
      fontWeight: 'bold'
    },
    subtitle: {
      margin: '5px 0 0 0',
      fontSize: '16px',
      opacity: 0.9
    },
    nav: {
      backgroundColor: 'white',
      padding: '10px 20px',
      borderBottom: '1px solid #ddd',
      textAlign: 'center'
    },
    button: {
      margin: '0 10px',
      padding: '10px 20px',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '14px',
      backgroundColor: '#e5e7eb',
      color: '#374151'
    },
    activeButton: {
      backgroundColor: '#2563eb',
      color: 'white'
    },
    content: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px'
    },
    card: {
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      marginBottom: '20px'
    },
    statsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '20px',
      marginBottom: '20px'
    },
    statCard: {
      backgroundColor: 'white',
      padding: '20px',
      borderRadius: '8px',
      textAlign: 'center',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    },
    statValue: {
      fontSize: '36px',
      fontWeight: 'bold',
      color: '#2563eb',
      margin: '0 0 10px 0'
    },
    statLabel: {
      fontSize: '14px',
      color: '#6b7280',
      margin: 0
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse',
      marginTop: '20px'
    },
    th: {
      backgroundColor: '#f9fafb',
      padding: '12px',
      textAlign: 'left',
      borderBottom: '1px solid #e5e7eb',
      fontWeight: 'bold'
    },
    td: {
      padding: '12px',
      borderBottom: '1px solid #e5e7eb'
    },
    successBadge: {
      backgroundColor: '#dcfce7',
      color: '#166534',
      padding: '4px 8px',
      borderRadius: '4px',
      fontSize: '12px'
    },
    loading: {
      textAlign: 'center',
      padding: '40px',
      fontSize: '16px'
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h1 style={styles.title}>dMaster</h1>
          <p style={styles.subtitle}>Disease Mastery Ontology System</p>
        </div>
        <div style={styles.loading}>Loading...</div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>dMaster</h1>
        <p style={styles.subtitle}>Disease Mastery Ontology System</p>
      </div>

      <nav style={styles.nav}>
        <button 
          style={{...styles.button, ...(currentPage === 'dashboard' ? styles.activeButton : {})}}
          onClick={() => setCurrentPage('dashboard')}
        >
          Dashboard
        </button>
        <button 
          style={{...styles.button, ...(currentPage === 'validation' ? styles.activeButton : {})}}
          onClick={() => setCurrentPage('validation')}
        >
          Validation
        </button>
        <button 
          style={{...styles.button, ...(currentPage === 'actions' ? styles.activeButton : {})}}
          onClick={() => setCurrentPage('actions')}
        >
          Actions
        </button>
      </nav>

      <div style={styles.content}>
        {currentPage === 'dashboard' && (
          <div>
            <h2>System Overview</h2>
            <div style={styles.statsGrid}>
              <div style={styles.statCard}>
                <div style={styles.statValue}>{stats?.total_ontologies || 0}</div>
                <div style={styles.statLabel}>Total Ontologies</div>
              </div>
              <div style={styles.statCard}>
                <div style={styles.statValue}>{stats?.valid_ontologies || 0}</div>
                <div style={styles.statLabel}>Valid Ontologies</div>
              </div>
              <div style={styles.statCard}>
                <div style={styles.statValue}>{stats?.invalid_ontologies || 0}</div>
                <div style={styles.statLabel}>Invalid Ontologies</div>
              </div>
              <div style={styles.statCard}>
                <div style={styles.statValue}>{stats?.total_triples || 0}</div>
                <div style={styles.statLabel}>Total Triples</div>
              </div>
            </div>

            <div style={styles.card}>
              <h3>Ontology Domains</h3>
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Domain</th>
                    <th style={styles.th}>Files</th>
                    <th style={styles.th}>Valid</th>
                    <th style={styles.th}>Triples</th>
                    <th style={styles.th}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {stats?.ontology_domains?.map((domain, index) => (
                    <tr key={index}>
                      <td style={styles.td}>{domain.name}</td>
                      <td style={styles.td}>{domain.count}</td>
                      <td style={styles.td}>{domain.valid}</td>
                      <td style={styles.td}>{domain.triples}</td>
                      <td style={styles.td}>
                        <span style={styles.successBadge}>
                          {domain.valid === domain.count ? 'All Valid' : 'Has Issues'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {currentPage === 'validation' && (
          <div>
            <div style={styles.card}>
              <h2>Validation Tools</h2>
              <p>Run comprehensive validation tests on your ontology files.</p>
              <button 
                style={{...styles.button, backgroundColor: '#2563eb', color: 'white'}}
                onClick={runValidation}
              >
                🔍 Run Validation
              </button>
            </div>
          </div>
        )}

        {currentPage === 'actions' && (
          <div>
            <div style={styles.card}>
              <h2>System Actions</h2>
              <p>Perform various operations on your ontology system.</p>
              <button 
                style={{...styles.button, backgroundColor: '#059669', color: 'white', marginRight: '10px'}}
                onClick={combineOntologies}
              >
                🔗 Combine Ontologies
              </button>
              <button 
                style={{...styles.button, backgroundColor: '#dc2626', color: 'white'}}
                onClick={fetchStats}
              >
                🔄 Refresh Stats
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;