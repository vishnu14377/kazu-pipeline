"""
Tests for the Kazu Ontology Converter.
"""

import os
import tempfile
import unittest
from pathlib import Path
import pandas as pd
import rdflib
from kazu_ontology_converter import KazuOntologyConverter, OntologyMetadata
import pytest
from rdflib import Graph, URIRef, RDF, RDFS, OWL, Literal
from kazu_ontology_converter import (
    batch_convert
)

class TestKazuOntologyConverter(unittest.TestCase):
    """Test cases for KazuOntologyConverter."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.metadata = OntologyMetadata(
            entity_class="TestEntity",
            name="TEST_ONTOLOGY",
            data_origin="Test Data"
        )
        self.converter = KazuOntologyConverter(self.metadata)
        
        # Create temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
        
    def create_test_owl(self) -> str:
        """Create a test OWL file."""
        g = rdflib.Graph()
        
        # Add a test class
        test_class = rdflib.URIRef("http://test.org/TestClass")
        g.add((test_class, rdflib.RDF.type, rdflib.OWL.Class))
        g.add((test_class, rdflib.RDFS.label, rdflib.Literal("Test Class")))
        g.add((test_class, rdflib.URIRef("http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"), 
               rdflib.Literal("Test Synonym")))
        
        # Save to file
        owl_path = self.temp_path / "test.owl"
        g.serialize(destination=str(owl_path), format="xml")
        return str(owl_path)
        
    def create_test_csv(self) -> str:
        """Create a test CSV file."""
        data = {
            'entity_id': ['TEST:1', 'TEST:2'],
            'label': ['Test Entity 1', 'Test Entity 2'],
            'synonyms': ['Synonym 1|Synonym 2', 'Synonym 3']
        }
        df = pd.DataFrame(data)
        csv_path = self.temp_path / "test.csv"
        df.to_csv(csv_path, index=False)
        return str(csv_path)
        
    def test_convert_owl(self):
        """Test OWL to Kazu CSV conversion."""
        # Create test OWL file
        owl_path = self.create_test_owl()
        output_path = str(self.temp_path / "test_owl_output.csv")
        
        # Convert
        self.converter.convert_owl(owl_path, output_path)
        
        # Verify output
        df = pd.read_csv(output_path)
        self.assertTrue(len(df) > 0)
        self.assertTrue(all(col in df.columns for col in 
                          ['IDX', 'DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE', 
                           'ENTITY_CLASS', 'ONTOLOGY_NAME']))
        
    def test_convert_csv(self):
        """Test CSV to Kazu CSV conversion."""
        # Create test CSV file
        csv_path = self.create_test_csv()
        output_path = str(self.temp_path / "test_csv_output.csv")
        
        # Convert
        self.converter.convert_csv(csv_path, output_path)
        
        # Verify output
        df = pd.read_csv(output_path)
        self.assertTrue(len(df) > 0)
        self.assertTrue(all(col in df.columns for col in 
                          ['IDX', 'DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE', 
                           'ENTITY_CLASS', 'ONTOLOGY_NAME']))
        
    def test_invalid_csv_columns(self):
        """Test handling of CSV with missing required columns."""
        # Create invalid CSV
        data = {'wrong_column': ['value']}
        df = pd.DataFrame(data)
        csv_path = str(self.temp_path / "invalid.csv")
        df.to_csv(csv_path, index=False)
        
        # Attempt conversion
        output_path = str(self.temp_path / "invalid_output.csv")
        with self.assertRaises(ValueError):
            self.converter.convert_csv(csv_path, output_path)
            
    def test_empty_owl(self):
        """Test handling of empty OWL file."""
        # Create empty OWL file
        g = rdflib.Graph()
        owl_path = str(self.temp_path / "empty.owl")
        g.serialize(destination=owl_path, format="xml")
        
        # Convert
        output_path = str(self.temp_path / "empty_output.csv")
        self.converter.convert_owl(owl_path, output_path)
        
        # Verify no output file was created
        self.assertFalse(os.path.exists(output_path))

@pytest.fixture
def sample_owl_file():
    """Create a sample OWL file for testing."""
    g = Graph()
    
    # Add a class with label and synonyms
    class_uri = URIRef("http://example.org/Disease1")
    g.add((class_uri, RDF.type, OWL.Class))
    g.add((class_uri, RDFS.label, Literal("Test Disease")))
    g.add((class_uri, URIRef("http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"), Literal("Disease One")))
    g.add((class_uri, URIRef("http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym"), Literal("Disease 1")))
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.owl', delete=False) as f:
        g.serialize(f.name, format='xml')
        return f.name

@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing."""
    data = {
        'entity_id': ['Disease1', 'Disease2'],
        'label': ['Test Disease 1', 'Test Disease 2'],
        'synonyms': ['Disease One|Disease 1', 'Disease Two|Disease 2']
    }
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        df.to_csv(f.name, index=False)
        return f.name

@pytest.fixture
def metadata():
    """Create sample metadata for testing."""
    return OntologyMetadata(
        entity_class="Disease",
        name="TestOntology",
        data_origin="Test"
    )

def test_owl_conversion(sample_owl_file, metadata):
    """Test OWL to Kazu CSV conversion."""
    converter = KazuOntologyConverter(metadata)
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        output_path = f.name
    
    try:
        converter.convert_owl(sample_owl_file, output_path)
        
        # Read the output CSV
        df = pd.read_csv(output_path)
        
        # Check required columns
        required_cols = ['IDX', 'DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE', 'ENTITY_CLASS', 'ONTOLOGY_NAME']
        assert all(col in df.columns for col in required_cols)
        
        # Check content
        assert len(df) == 3  # One exact match + two synonyms
        assert df['ENTITY_CLASS'].unique()[0] == 'Disease'
        assert df['ONTOLOGY_NAME'].unique()[0] == 'TestOntology'
        
        # Check exact match
        exact_matches = df[df['MAPPING_TYPE'] == 'exact']
        assert len(exact_matches) == 1
        assert exact_matches['DEFAULT_LABEL'].iloc[0] == 'Test Disease'
        
        # Check synonyms
        synonyms = df[df['MAPPING_TYPE'] == 'synonym']
        assert len(synonyms) == 2
        assert set(synonyms['SYN']) == {'Disease One', 'Disease 1'}
        
    finally:
        os.unlink(output_path)

def test_csv_conversion(sample_csv_file, metadata):
    """Test CSV to Kazu CSV conversion."""
    converter = KazuOntologyConverter(metadata)
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        output_path = f.name
    
    try:
        converter.convert_csv(sample_csv_file, output_path)
        
        # Read the output CSV
        df = pd.read_csv(output_path)
        
        # Check required columns
        required_cols = ['IDX', 'DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE', 'ENTITY_CLASS', 'ONTOLOGY_NAME']
        assert all(col in df.columns for col in required_cols)
        
        # Check content
        assert len(df) == 6  # Two entities, each with one exact match and two synonyms
        assert df['ENTITY_CLASS'].unique()[0] == 'Disease'
        assert df['ONTOLOGY_NAME'].unique()[0] == 'TestOntology'
        
        # Check exact matches
        exact_matches = df[df['MAPPING_TYPE'] == 'exact']
        assert len(exact_matches) == 2
        assert set(exact_matches['DEFAULT_LABEL']) == {'Test Disease 1', 'Test Disease 2'}
        
        # Check synonyms
        synonyms = df[df['MAPPING_TYPE'] == 'synonym']
        assert len(synonyms) == 4
        assert set(synonyms['SYN']) == {'Disease One', 'Disease 1', 'Disease Two', 'Disease 2'}
        
    finally:
        os.unlink(output_path)

def test_batch_conversion(sample_owl_file, sample_csv_file, metadata):
    """Test batch processing of multiple files."""
    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        # Copy test files to input directory with different names
        os.link(sample_owl_file, os.path.join(input_dir, 'test1.owl'))
        os.link(sample_csv_file, os.path.join(input_dir, 'test2.csv'))
        
        # Run batch conversion
        batch_convert(input_dir, output_dir, metadata)
        
        # Check output files
        output_files = os.listdir(output_dir)
        assert len(output_files) == 2
        assert 'test1_kazu.csv' in output_files
        assert 'test2_kazu.csv' in output_files
        
        # Check content of output files
        for output_file in output_files:
            output_path = os.path.join(output_dir, output_file)
            df = pd.read_csv(output_path)
            assert len(df) > 0
            assert all(col in df.columns for col in ['IDX', 'DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE', 'ENTITY_CLASS', 'ONTOLOGY_NAME'])

def test_invalid_input(metadata):
    """Test handling of invalid input files."""
    converter = KazuOntologyConverter(metadata)
    
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
        output_path = f.name
    
    try:
        # Test with non-existent file
        with pytest.raises(Exception):
            converter.convert_owl('nonexistent.owl', output_path)
        
        # Test with invalid CSV format
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            f.write(b'invalid,csv,format\n')
            invalid_csv = f.name
        
        with pytest.raises(ValueError):
            converter.convert_csv(invalid_csv, output_path)
            
    finally:
        os.unlink(output_path)
        if 'invalid_csv' in locals():
            os.unlink(invalid_csv)

if __name__ == '__main__':
    unittest.main() 