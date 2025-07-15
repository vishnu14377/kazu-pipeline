#!/usr/bin/env python3

import os
from pathlib import Path
from rdflib import Graph, Namespace
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OntologyCombiner:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.ontology_dir = self.base_dir / "ontologies"
        self.output_file = self.ontology_dir / "combined_ontology.ttl"
        self.combined_graph = Graph()
        
        # Define namespaces
        self.namespaces = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'dc': 'http://purl.org/dc/terms/',
            'dct': 'http://purl.org/dc/terms/',
            'sepio': 'http://purl.obolibrary.org/obo/sepio#',
            'obi': 'http://purl.obolibrary.org/obo/OBI_',
            'doid': 'http://purl.obolibrary.org/obo/DOID_',
            'hpo': 'http://purl.obolibrary.org/obo/HP_',
            'snomed': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
            'rxnorm': 'http://purl.bioontology.org/ontology/RXNORM/',
            'loinc': 'http://purl.bioontology.org/ontology/LNC/',
            'efo': 'http://www.ebi.ac.uk/efo/',
            'ncit': 'http://purl.obolibrary.org/ontology/NCIT/',
            'sio': 'http://semanticscience.org/resource/',
            'obo': 'http://purl.obolibrary.org/obo/',
            'skos': 'http://www.w3.org/2004/02/skos/core#',
            'ncit': 'http://purl.obolibrary.org/ontology/NCIT/',
            # Add domain-specific namespaces
            'phenotype': 'http://example.org/phenotype-ontology#',
            'disease': 'http://example.org/disease-ontology#',
            'diagnosis': 'http://example.org/diagnosis-ontology#',
            'pathogenesis': 'http://example.org/pathogenesis-ontology#',
            'clinical': 'http://example.org/clinical-ontology#',
            'commercial': 'http://example.org/commercial-ontology#',
            'metadata': 'http://example.org/metadata-ontology#',
            'population': 'http://example.org/population-ontology#',
            'treatment': 'http://example.org/treatment-ontology#',
            'prov': 'http://example.org/prov-ontology#',
            'skos': 'http://www.w3.org/2004/02/skos/core#'

        }

    def bind_namespaces(self):
        """Bind all namespaces to the combined graph."""
        # Create a new graph to ensure clean namespace bindings
        new_graph = Graph()
        
        # First bind our custom prov namespace to ensure it takes precedence
        new_graph.bind("prov", Namespace("http://example.org/prov-ontology#"), override=True)
        
        # Bind all other namespaces
        for prefix, uri in self.namespaces.items():
            if prefix != "prov":  # Skip prov since we already bound it
                new_graph.bind(prefix, Namespace(uri), override=True)
        
        # Add all triples from the old graph to the new one
        for s, p, o in self.combined_graph:
            new_graph.add((s, p, o))
        
        # Replace the old graph with the new one
        self.combined_graph = new_graph

    def load_core_ontology(self, domain: str) -> bool:
        """Load a core ontology from a domain module."""
        core_file = self.ontology_dir / domain / f"{domain}_core.ttl"
        if not core_file.exists():
            logger.warning(f"Core ontology not found for domain {domain}: {core_file}")
            return False
        
        try:
            # Create a temporary graph to parse the file
            temp_graph = Graph()
            
            # Bind the domain's namespace before parsing
            domain_ns = f"http://example.org/{domain}-ontology#"
            temp_graph.bind(domain, Namespace(domain_ns))
            
            # Parse the file
            temp_graph.parse(core_file, format="turtle")
            
            # Process owl:imports statements
            for s, p, o in temp_graph.triples((None, self.combined_graph.namespace_manager.expand_curie("owl:imports"), None)):
                import_path = str(o)
                if import_path.startswith("http://example.org/"):
                    # Handle internal imports
                    import_domain = import_path.split("/")[-1].split("#")[0].split(".")[0]
                    import_file = self.ontology_dir / import_domain / f"{import_domain}_core.ttl"
                    if import_file.exists():
                        # Bind the imported domain's namespace
                        import_ns = f"http://example.org/{import_domain}-ontology#"
                        temp_graph.bind(import_domain, Namespace(import_ns))
                        temp_graph.parse(import_file, format="turtle")
                        logger.info(f"Loaded imported ontology: {import_domain}")
            
            # Add all triples to the combined graph
            for s, p, o in temp_graph:
                self.combined_graph.add((s, p, o))
            
            logger.info(f"Loaded core ontology: {domain}")
            return True
        except Exception as e:
            logger.error(f"Error loading {domain} core ontology: {e}")
            return False

    def load_main_ontology(self) -> bool:
        """Load the main ontology."""
        main_file = self.ontology_dir / "main_ontology" / "ontology.ttl"
        if not main_file.exists():
            logger.error("Main ontology not found")
            return False
        
        try:
            # Create a temporary graph to parse the file
            temp_graph = Graph()
            
            # Bind all namespaces before parsing
            for prefix, uri in self.namespaces.items():
                temp_graph.bind(prefix, Namespace(uri))
            
            # Parse the file
            temp_graph.parse(main_file, format="turtle")
            
            # Process owl:imports statements
            for s, p, o in temp_graph.triples((None, self.combined_graph.namespace_manager.expand_curie("owl:imports"), None)):
                import_path = str(o)
                if import_path.startswith("http://example.org/"):
                    # Handle internal imports
                    import_domain = import_path.split("/")[-1].split("#")[0].split(".")[0]
                    import_file = self.ontology_dir / import_domain / f"{import_domain}_core.ttl"
                    if import_file.exists():
                        # Bind the imported domain's namespace
                        import_ns = f"http://example.org/{import_domain}-ontology#"
                        temp_graph.bind(import_domain, Namespace(import_ns))
                        temp_graph.parse(import_file, format="turtle")
                        logger.info(f"Loaded imported ontology: {import_domain}")
            
            # Add all triples to the combined graph
            for s, p, o in temp_graph:
                self.combined_graph.add((s, p, o))
            
            logger.info("Loaded main ontology")
            return True
        except Exception as e:
            logger.error(f"Error loading main ontology: {e}")
            return False

    def combine_ontologies(self):
        """Combine all ontologies into a single file."""
        # Bind namespaces first
        self.bind_namespaces()
        
        # Load core ontologies from each domain
        domains = [
            'clinical',
            'commercial',
            'diagnosis',
            'disease',
            'metadata',
            'pathogenesis',
            'phenotype',
            'population',
            'prov',
            'treatment'
        ]
        for domain in domains:
            self.load_core_ontology(domain)
        
        # Load main ontology last (it may reference core ontologies)
        self.load_main_ontology()
        
        # Force final prov namespace binding
        self.combined_graph.bind("prov", Namespace("http://example.org/prov-ontology#"), override=True)
        
        # Serialize the combined graph
        try:
            self.combined_graph.serialize(destination=self.output_file, format="turtle")
            logger.info(f"Successfully combined ontologies into: {self.output_file}")
        except Exception as e:
            logger.error(f"Error serializing combined ontology: {e}")

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Create and run the combiner
    combiner = OntologyCombiner(str(project_root))
    combiner.combine_ontologies()

if __name__ == "__main__":
    main() 
