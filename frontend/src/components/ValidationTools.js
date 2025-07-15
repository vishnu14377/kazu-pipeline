import React, { useState } from 'react';
import axios from 'axios';

const ValidationTools = () => {
  const [validationResult, setValidationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runValidation = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post('/api/validate');
      setValidationResult(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="section-title">Validation Tools</h1>
          <p className="text-gray-600">Validate your ontology files</p>
        </div>
        <button
          onClick={runValidation}
          disabled={loading}
          className="btn-primary"
        >
          {loading ? (
            <>
              <div className="inline-block loading-spinner w-4 h-4 mr-2"></div>
              Running...
            </>
          ) : (
            '🔍 Run Validation'
          )}
        </button>
      </div>

      {error && (
        <div className="alert alert-error">
          <p>Error: {error}</p>
        </div>
      )}

      {/* Validation Results */}
      {validationResult && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="section-subtitle">Validation Results</h2>
          
          <div className={`alert mb-4 ${
            validationResult.success ? 'alert-success' : 'alert-error'
          }`}>
            <p className="font-medium">
              {validationResult.success ? 
                '✅ All validation tests passed!' : 
                '❌ Some validation tests failed'
              }
            </p>
          </div>

          {validationResult.stdout && (
            <div className="mb-4">
              <h3 className="font-medium mb-2">Test Output:</h3>
              <pre className="code-block">{validationResult.stdout}</pre>
            </div>
          )}

          {validationResult.stderr && (
            <div className="mb-4">
              <h3 className="font-medium mb-2">Errors:</h3>
              <pre className="code-block bg-red-900 text-red-100">
                {validationResult.stderr}
              </pre>
            </div>
          )}

          <div className="text-sm text-gray-600">
            Exit code: {validationResult.return_code}
          </div>
        </div>
      )}

      {/* Validation Information */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="section-subtitle">About Validation</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-medium text-gray-900">What gets validated:</h3>
            <ul className="mt-2 text-sm text-gray-600 space-y-1">
              <li>• TTL file syntax validation</li>
              <li>• Ontology structure checks</li>
              <li>• Prefix declarations</li>
              <li>• Class definitions</li>
              <li>• Property definitions</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-medium text-gray-900">Validation Process:</h3>
            <ul className="mt-2 text-sm text-gray-600 space-y-1">
              <li>1. Syntax validation using RDFLib parser</li>
              <li>2. Structure validation for core ontologies</li>
              <li>3. Import chain verification</li>
              <li>4. Consistency checking (if available)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ValidationTools;