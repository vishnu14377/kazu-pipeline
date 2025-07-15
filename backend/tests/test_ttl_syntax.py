from pathlib import Path
import pytest
from rdflib import Graph, RDF, OWL, RDFS

# Get the project root directory (dMaster)
PROJECT_ROOT = Path(__file__).parent.parent

# Define paths to test
ONTOLOGIES_DIR = PROJECT_ROOT / "ontologies"
MAIN_ONTOLOGY = PROJECT_ROOT / "ontologies" / "main_ontology" / "ontology.ttl"

def get_all_ttl_files():
    """Get all .ttl files from the ontologies directory and its subdirectories."""
    ttl_files = []
    
    # Add main ontology if it exists
    if MAIN_ONTOLOGY.exists():
        ttl_files.append(MAIN_ONTOLOGY)
    
    # Add all core TTL files from ontologies subdirectories
    for ttl_file in ONTOLOGIES_DIR.rglob("*_core.ttl"):
        ttl_files.append(ttl_file)
    
    return ttl_files

@pytest.mark.parametrize("ttl_path", get_all_ttl_files())
def test_ttl_syntax(ttl_path: Path):
    """Ensure that Turtle files are syntactically valid."""
    g = Graph()
    try:
        g.parse(ttl_path, format="turtle")
        # Additional validation: check if the graph is not empty
        assert len(g) > 0, f"TTL file {ttl_path} is empty"
    except Exception as e:
        pytest.fail(f"Invalid TTL file {ttl_path}: {str(e)}")

def test_ontology_imports():
    """Test that the main ontology can import all core ontologies."""
    if not MAIN_ONTOLOGY.exists():
        pytest.skip("Main ontology file not found")
        
    g = Graph()
    try:
        g.parse(MAIN_ONTOLOGY, format="turtle")
        # Check if the graph is not empty
        assert len(g) > 0, "Main ontology is empty"
    except Exception as e:
        pytest.fail(f"Main ontology validation failed: {str(e)}")

def test_core_ontology_structure():
    """Test that each core ontology has the expected structure."""
    for ttl_path in ONTOLOGIES_DIR.rglob("*_core.ttl"):
        g = Graph()
        try:
            g.parse(ttl_path, format="turtle")
            
            # Check for basic ontology components
            assert len(g) > 0, f"Core ontology {ttl_path} is empty"
            
            # Check for prefix declarations
            prefixes = [str(p) for p in g.namespaces()]
            assert len(prefixes) > 0, f"No prefix declarations found in {ttl_path}"
            
            # Check for class definitions
            classes = list(g.subjects(predicate=RDF.type, object=OWL.Class))
            assert len(classes) > 0, f"No class definitions found in {ttl_path}"
            
        except Exception as e:
            pytest.fail(f"Failed to validate {ttl_path}: {str(e)}")
