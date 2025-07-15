#!/usr/bin/env python3

import os
import sys
from pathlib import Path
import pytest
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, OWL

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from ontology_validation.validate_modularity import ModularOntologyValidator, ModuleValidationResult

@pytest.fixture
def validator():
    """Create a validator instance for testing"""
    return ModularOntologyValidator(str(Path(__file__).parent.parent / "ontologies"))

@pytest.fixture
def sample_graph():
    """Create a sample graph for testing"""
    g = Graph()
    # Add some test triples
    g.add((URIRef("http://example.org/clinical-ontology/TestClass"), RDF.type, OWL.Class))
    g.add((URIRef("http://example.org/disease-ontology/TestProperty"), RDF.type, OWL.ObjectProperty))
    return g

def test_load_modules(validator):
    """Test module loading"""
    assert validator.load_modules()
    assert len(validator.graphs) > 0
    assert all(isinstance(g, Graph) for g in validator.graphs.values())

def test_check_module_boundaries(validator, sample_graph):
    """Test module boundary checking"""
    validator.graphs['clinical'] = sample_graph
    results = validator.check_module_boundaries()
    
    assert len(results) > 0
    for result in results:
        assert isinstance(result, ModuleValidationResult)
        assert hasattr(result, 'module_name')
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'warnings')
        assert hasattr(result, 'suggestions')

def test_check_import_dependencies(validator, sample_graph):
    """Test import dependency checking"""
    validator.graphs['clinical'] = sample_graph
    results = validator.check_import_dependencies()
    
    assert len(results) > 0
    for result in results:
        assert isinstance(result, ModuleValidationResult)
        # Check that results contain appropriate fields
        assert all(isinstance(w, str) for w in result.warnings)
        assert all(isinstance(s, str) for s in result.suggestions)

def test_check_circular_dependencies(validator):
    """Test circular dependency detection"""
    # Create a circular dependency
    g1 = Graph()
    g2 = Graph()
    
    g1.add((URIRef("http://example.org/module1"), OWL.imports, 
            URIRef("http://example.org/module2-ontology")))
    g2.add((URIRef("http://example.org/module2"), OWL.imports, 
            URIRef("http://example.org/module1-ontology")))
    
    validator.graphs['module1'] = g1
    validator.graphs['module2'] = g2
    
    cycles = validator.check_circular_dependencies()
    assert len(cycles) > 0
    assert any("module1" in cycle and "module2" in cycle for cycle in cycles)

def test_check_external_alignments(validator, sample_graph):
    """Test external ontology alignment checking"""
    # Add some external references
    sample_graph.add((URIRef("http://purl.obolibrary.org/obo/HP_0000001"), 
                     RDF.type, OWL.Class))
    sample_graph.add((URIRef("http://purl.obolibrary.org/obo/DOID_0000001"), 
                     RDF.type, OWL.Class))
    
    validator.graphs['clinical'] = sample_graph
    results = validator.check_external_alignments()
    
    assert len(results) > 0
    for result in results:
        assert isinstance(result, ModuleValidationResult)
        # Check that external references are detected
        if result.module_name == 'clinical':
            assert any('HPO' in w for w in result.warnings)
            assert any('DOID' in w for w in result.warnings)

def test_validate_integration(validator):
    """Test the complete validation process"""
    results = validator.validate()
    
    assert len(results) > 0
    for result in results:
        assert isinstance(result, ModuleValidationResult)
        # Check that results have appropriate structure
        assert hasattr(result, 'module_name')
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'errors')
        assert hasattr(result, 'warnings')
        assert hasattr(result, 'suggestions')
        
        # Check that lists contain strings
        assert all(isinstance(e, str) for e in result.errors)
        assert all(isinstance(w, str) for w in result.warnings)
        assert all(isinstance(s, str) for s in result.suggestions)

def test_error_handling(validator):
    """Test error handling in validation"""
    # Test with non-existent directory
    bad_validator = ModularOntologyValidator("/nonexistent/path")
    results = bad_validator.validate()
    
    assert len(results) == 1
    assert not results[0].is_valid
    assert len(results[0].errors) > 0
    assert "Failed to load modules" in results[0].errors[0]

def test_module_validation_result():
    """Test ModuleValidationResult class"""
    result = ModuleValidationResult(
        module_name="test",
        is_valid=True,
        errors=["error1"],
        warnings=["warning1"],
        suggestions=["suggestion1"]
    )
    
    assert result.module_name == "test"
    assert result.is_valid
    assert result.errors == ["error1"]
    assert result.warnings == ["warning1"]
    assert result.suggestions == ["suggestion1"] 