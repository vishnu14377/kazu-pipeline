import os
import pytest
from rdflib import Graph, Literal
from rdflib.namespace import RDF, RDFS, OWL
import owlready2
from pyshacl import validate
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from utils.ontology_utils import find_entities_by_label

@pytest.fixture(scope="module")
def ontology_graph():
    """Load the combined ontology file."""
    g = Graph()
    g.parse("ontologies/combined_ontology.ttl", format="turtle")
    return g

def test_essential_classes_present(ontology_graph):
    """Test that essential classes are defined."""
    essential_classes = [
        "Patient",
        "Cohort Definition",
        "Diagnosis Assertion",
        "Observation Period End"
    ]
    for label in essential_classes:
        matches = find_entities_by_label(ontology_graph, label, OWL.Class)
        assert matches, f"Ontology is missing an owl:Class with label '{label}'"

def test_essential_object_properties_present(ontology_graph):
    """Test that essential properties are defined."""
    essential_props = [
        "has entry criterion",
        "has exit criterion",
        "diagnoses",
        "hasDiagnosis",
        "includes patient"
    ]
    for label in essential_props:
        matches = find_entities_by_label(ontology_graph, label, OWL.ObjectProperty)
        assert matches, f"Ontology is missing an owl:ObjectProperty with label '{label}'"

def test_ontology_consistency(ontology_graph):
    """Test that the ontology is consistent."""
    # Convert the RDFLib graph to a temporary file in Turtle format
    temp_file = "temp_ontology.ttl"
    ontology_graph.serialize(destination=temp_file, format="turtle")
    
    try:
        # Load the ontology with owlready2
        onto = owlready2.get_ontology(temp_file).load()
        
        # Run the reasoner and catch any errors
        try:
            with onto:
                owlready2.sync_reasoner()
                assert True, "Ontology is consistent"
        except Exception as e:
            assert False, f"Ontology consistency check failed: {str(e)}"
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_shacl_validation(ontology_graph):
    """Test that the ontology passes SHACL validation."""
    shapes_graph = Graph()
    shapes_graph.parse("ontologies/shapes/shapes.ttl", format="turtle")
    conforms, results_graph, results_text = validate(ontology_graph, shacl_graph=shapes_graph)
    assert conforms, f"SHACL validation failed: {results_text}" 