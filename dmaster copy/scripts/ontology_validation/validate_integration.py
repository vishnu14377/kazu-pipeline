#!/usr/bin/env python3

import rdflib
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ontology_validation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class OntologyValidator:
    def __init__(self):
        self.g = Graph()
        self.ns = {
            'rdf': RDF,
            'rdfs': RDFS,
            'owl': OWL,
            'xsd': XSD,
            'disease': Namespace('http://example.org/disease-ontology#'),
            'clinical': Namespace('http://example.org/clinical-ontology#'),
            'snomed': Namespace('http://purl.bioontology.org/ontology/SNOMEDCT/')
        }
        
        # Bind namespaces
        for prefix, namespace in self.ns.items():
            self.g.bind(prefix, namespace)

    def load_ontologies(self):
        """Load all relevant ontology files."""
        try:
            # Load main ontologies
            self.g.parse('../../ontologies/disease/disease_core.ttl', format='turtle')
            self.g.parse('../../ontologies/clinical/clinical_core.ttl', format='turtle')
            self.g.parse('../../ontologies/main_ontology/ontology.ttl', format='turtle')
            logger.info("Successfully loaded ontology files")
        except Exception as e:
            logger.error(f"Error loading ontology files: {str(e)}")
            raise

    def validate_syntax(self):
        """Validate RDF/Turtle syntax."""
        try:
            # Basic syntax validation
            for s, p, o in self.g:
                if not isinstance(s, (rdflib.URIRef, rdflib.BNode)):
                    logger.error(f"Invalid subject type: {type(s)}")
                if not isinstance(p, rdflib.URIRef):
                    logger.error(f"Invalid predicate type: {type(p)}")
                if not isinstance(o, (rdflib.URIRef, rdflib.BNode, rdflib.Literal)):
                    logger.error(f"Invalid object type: {type(o)}")
            logger.info("Syntax validation completed")
        except Exception as e:
            logger.error(f"Error in syntax validation: {str(e)}")
            raise

    def validate_mappings(self):
        """Validate external ontology mappings."""
        try:
            # Check SNOMED CT mappings
            query = """
            SELECT ?disease ?xref
            WHERE {
                ?disease rdf:type disease:Disease .
                ?disease disease:hasDbXref ?xref .
                FILTER(STRSTARTS(STR(?xref), "http://purl.bioontology.org/ontology/SNOMEDCT/"))
            }
            """
            results = self.g.query(query)
            for row in results:
                logger.info(f"Found mapping: {row.disease} -> {row.xref}")
            logger.info("Mapping validation completed")
        except Exception as e:
            logger.error(f"Error in mapping validation: {str(e)}")
            raise

    def validate_cross_references(self):
        """Validate cross-module references."""
        try:
            # Check clinical-disease relationships
            query = """
            SELECT ?disease ?event
            WHERE {
                ?disease rdf:type disease:Disease .
                ?event rdf:type clinical:DiseaseEvent .
                ?disease disease:hasEvent ?event .
            }
            """
            results = self.g.query(query)
            for row in results:
                logger.info(f"Found cross-reference: {row.disease} -> {row.event}")
            logger.info("Cross-reference validation completed")
        except Exception as e:
            logger.error(f"Error in cross-reference validation: {str(e)}")
            raise

    def validate_temporal_relationships(self):
        """Validate temporal relationships in clinical events."""
        try:
            query = """
            SELECT ?event ?time ?duration
            WHERE {
                ?event rdf:type clinical:DiseaseEvent .
                ?event clinical:occursAt ?time .
                ?event clinical:hasDuration ?duration .
            }
            """
            results = self.g.query(query)
            for row in results:
                logger.info(f"Found temporal relationship: {row.event} at {row.time} with duration {row.duration}")
            logger.info("Temporal relationship validation completed")
        except Exception as e:
            logger.error(f"Error in temporal relationship validation: {str(e)}")
            raise

    def detect_duplicate_classes(self):
        """Detect duplicate classes across ontologies."""
        try:
            query = """
            SELECT ?class (COUNT(?class) AS ?count)
            WHERE {
                ?class a owl:Class .
            }
            GROUP BY ?class
            HAVING (COUNT(?class) > 1)
            """
            results = self.g.query(query)
            duplicates = []
            for row in results:
                duplicates.append(str(row[0]))
            if duplicates:
                logger.warning(f"Duplicate classes detected: {duplicates}")
            else:
                logger.info("No duplicate classes detected.")
        except Exception as e:
            logger.error(f"Error detecting duplicate classes: {str(e)}")
            raise

    def detect_conflicting_triples(self):
        """Detect conflicting RDF triples."""
        try:
            # This is a placeholder for actual conflict detection logic
            # For example, check for contradictory property assertions
            # Here, we just log that the check was performed
            logger.info("Conflicting triples detection not yet implemented.")
        except Exception as e:
            logger.error(f"Error detecting conflicting triples: {str(e)}")
            raise

    def run_all_validations(self):
        """Run all validation checks."""
        try:
            self.load_ontologies()
            self.validate_syntax()
            self.validate_mappings()
            self.validate_cross_references()
            self.validate_temporal_relationships()
            self.detect_duplicate_classes()
            self.detect_conflicting_triples()
            logger.info("All validations completed successfully")
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            raise

if __name__ == "__main__":
    validator = OntologyValidator()
    validator.run_all_validations() 