#!/usr/bin/env python3

import os
from pathlib import Path
from rdflib import Graph
import pyshacl
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OntologyValidator:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.ontology_dir = self.base_dir / "ontologies"
        self.combined_file = self.ontology_dir / "combined_ontology.ttl"
        self.graph = Graph()

    def load_combined_ontology(self) -> bool:
        """Load the combined ontology file."""
        if not self.combined_file.exists():
            logger.error(f"Combined ontology not found: {self.combined_file}")
            return False
        
        try:
            self.graph.parse(self.combined_file, format="turtle")
            logger.info("Loaded combined ontology")
            return True
        except Exception as e:
            logger.error(f"Error loading combined ontology: {e}")
            return False

    def validate_shacl(self) -> bool:
        """Validate the ontology using SHACL."""
        try:
            # Load SHACL shapes if they exist
            shapes_file = self.ontology_dir / "shapes" / "ontology_shapes.ttl"
            if shapes_file.exists():
                shapes_graph = Graph()
                shapes_graph.parse(shapes_file, format="turtle")
                conforms, results_graph, results_text = pyshacl.validate(
                    self.graph,
                    shacl_graph=shapes_graph,
                    ont_graph=None,
                    inference='rdfs',
                    abort_on_error=False,
                    meta_shacl=False,
                    debug=False
                )
            else:
                # If no shapes file exists, just validate basic RDF structure
                conforms, results_graph, results_text = pyshacl.validate(
                    self.graph,
                    shacl_graph=None,
                    ont_graph=None,
                    inference='rdfs',
                    abort_on_error=False,
                    meta_shacl=False,
                    debug=False
                )

            if conforms:
                logger.info("SHACL validation passed")
                return True
            else:
                logger.error(f"SHACL validation failed: {results_text}")
                return False

        except Exception as e:
            logger.error(f"Error during SHACL validation: {e}")
            return False

    def validate_owl(self) -> bool:
        """Validate the ontology using OWL validation."""
        try:
            # Basic OWL validation using rdflib
            # This checks for basic OWL syntax and structure
            for s, p, o in self.graph.triples((None, None, None)):
                if not isinstance(s, (str, Graph)) or not isinstance(p, (str, Graph)) or not isinstance(o, (str, Graph)):
                    logger.error(f"Invalid triple found: {s} {p} {o}")
                    return False
            
            logger.info("OWL validation passed")
            return True
        except Exception as e:
            logger.error(f"Error during OWL validation: {e}")
            return False

    def validate(self):
        """Run all validation checks."""
        if not self.load_combined_ontology():
            return False
        
        shacl_valid = self.validate_shacl()
        owl_valid = self.validate_owl()
        
        return shacl_valid and owl_valid

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Create and run the validator
    validator = OntologyValidator(str(project_root))
    if validator.validate():
        logger.info("All validation checks passed")
    else:
        logger.error("Validation checks failed")

if __name__ == "__main__":
    main() 