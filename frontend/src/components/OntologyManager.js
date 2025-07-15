import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OntologyManager = () => {
  const [ontologies, setOntologies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedOntology, setSelectedOntology] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchOntologies();
  }, []);

  const fetchOntologies = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/ontologies');
      setOntologies(response.data.ontologies);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      if (response.data.success) {
        await fetchOntologies();
        event.target.value = '';
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const viewOntology = async (ontologyName) => {
    try {
      const response = await axios.get(`/api/ontology/${ontologyName}`);
      setSelectedOntology(response.data);
      setShowModal(true);
    } catch (err) {
      setError(err.message);
    }
  };

  const combineOntologies = async () => {
    try {
      setLoading(true);
      const response = await axios.post('/api/combine');
      if (response.data.success) {
        await fetchOntologies();
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = async (fileType) => {
    try {
      const response = await axios.get(`/api/download/${fileType}`, {
        responseType: 'blob',
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${fileType}_ontology.ttl`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="section-title">Ontology Manager</h1>
          <p className="text-gray-600">Manage your ontology files</p>
        </div>
        <div className="flex space-x-4">
          <button
            onClick={combineOntologies}
            className="btn-primary"
          >
            🔗 Combine Ontologies
          </button>
          <button
            onClick={() => downloadFile('combined')}
            className="btn-secondary"
          >
            📥 Download Combined
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-error">
          <p>Error: {error}</p>
        </div>
      )}

      {/* Upload Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">Upload New Ontology</h2>
        <div className="upload-area">
          <input
            type="file"
            accept=".ttl"
            onChange={handleFileUpload}
            disabled={uploading}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center justify-center"
          >
            <div className="text-4xl mb-2">📁</div>
            <p className="text-lg font-medium">
              {uploading ? 'Uploading...' : 'Click to upload TTL file'}
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Only .ttl (Turtle) files are supported
            </p>
          </label>
        </div>
      </div>

      {/* Ontologies List */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">Ontology Files</h2>
        <div className="table-container">
          <table className="table">
            <thead className="table-header">
              <tr>
                <th>Name</th>
                <th>Path</th>
                <th>Status</th>
                <th>Triples</th>
                <th>Size</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody className="table-body">
              {ontologies.map((ontology, index) => (
                <tr key={index}>
                  <td className="font-medium">{ontology.name}</td>
                  <td className="text-gray-600">{ontology.path}</td>
                  <td>
                    <span className={`status-badge ${
                      ontology.is_valid ? 'status-valid' : 'status-invalid'
                    }`}>
                      {ontology.is_valid ? 'Valid' : 'Invalid'}
                    </span>
                  </td>
                  <td>{ontology.triple_count}</td>
                  <td>{Math.round(ontology.size / 1024)} KB</td>
                  <td>
                    <button
                      onClick={() => viewOntology(ontology.name)}
                      className="btn-secondary mr-2"
                    >
                      👁️ View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal for viewing ontology content */}
      {showModal && selectedOntology && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-container" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">{selectedOntology.name}</h3>
              <button
                className="modal-close"
                onClick={() => setShowModal(false)}
              >
                ✕
              </button>
            </div>
            <div className="mt-4">
              <pre className="code-block max-h-96 overflow-y-auto">
                {selectedOntology.content}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default OntologyManager;