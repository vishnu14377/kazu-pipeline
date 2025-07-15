#!/usr/bin/env python3

import os
from pathlib import Path
from typing import List, Dict, Set, Optional
import logging
from dataclasses import dataclass
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, OWL
import networkx as nx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ModuleValidationResult:
    """Class to store module validation results"""
    module_name: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class ModularOntologyValidator:
    """Validator for modular ontology structure"""
    
    def __init__(self, ontology_dir: str):
        self.ontology_dir = Path(ontology_dir)
        self.modules = {
            'clinical': self.ontology_dir / "clinical" / "clinical_core.ttl",
            'diagnosis': self.ontology_dir / "diagnosis" / "diagnosis_core.ttl",
            'disease': self.ontology_dir / "disease" / "disease_core.ttl",
            'phenotype': self.ontology_dir / "phenotype" / "phenotype_core.ttl",
            'treatment': self.ontology_dir / "treatment" / "treatment_core.ttl",
            'population': self.ontology_dir / "population" / "population_core.ttl",
            'pathogenesis': self.ontology_dir / "pathogenesis" / "pathogenesis_core.ttl"
        }
        self.graphs = {}
        self.import_graph = nx.DiGraph()
        
    def load_modules(self) -> bool:
        """Load all module ontologies"""
        try:
            for module_name, file_path in self.modules.items():
                if not file_path.exists():
                    logger.error(f"Module file not found: {file_path}")
                    continue
                    
                g = Graph()
                g.parse(file_path, format="turtle")
                self.graphs[module_name] = g
                logger.info(f"Loaded module: {module_name}")
                
            return len(self.graphs) > 0
        except Exception as e:
            logger.error(f"Error loading modules: {str(e)}")
            return False

    def check_module_boundaries(self) -> List[ModuleValidationResult]:
        """Check that modules respect their boundaries"""
        results = []
        
        for module_name, graph in self.graphs.items():
            result = ModuleValidationResult(module_name, True, [], [], [])
            
            # Check for classes defined in other modules
            for s, p, o in graph.triples((None, RDF.type, OWL.Class)):
                if not str(s).startswith(f"http://example.org/{module_name}-ontology"):
                    result.warnings.append(
                        f"Class {s} is defined in {module_name} but has different namespace"
                    )
                    result.suggestions.append(
                        f"Consider moving {s} to its proper module or adding owl:imports"
                    )
            
            # Check for properties used across modules
            for s, p, o in graph.triples((None, RDF.type, OWL.ObjectProperty)):
                if not str(s).startswith(f"http://example.org/{module_name}-ontology"):
                    result.warnings.append(
                        f"Property {s} is used in {module_name} but defined elsewhere"
                    )
                    result.suggestions.append(
                        f"Consider importing the module that defines {s}"
                    )
            
            results.append(result)
            
        return results

    def check_import_dependencies(self) -> List[ModuleValidationResult]:
        """Check module import dependencies"""
        results = []
        
        for module_name, graph in self.graphs.items():
            result = ModuleValidationResult(module_name, True, [], [], [])
            
            # Get all imports
            imports = [o for s, p, o in graph.triples((None, OWL.imports, None))]
            
            # Check for missing imports
            for s, p, o in graph.triples((None, None, None)):
                if isinstance(o, URIRef) and str(o).startswith("http://example.org/"):
                    module = str(o).split("/")[-1].split("-")[0]
                    if module in self.modules and module != module_name:
                        if not any(str(imp).endswith(f"{module}-ontology") for imp in imports):
                            result.warnings.append(
                                f"Module uses {o} but doesn't import {module} ontology"
                            )
                            result.suggestions.append(
                                f"Add owl:imports for {module} ontology"
                            )
            
            results.append(result)
            
        return results

    def check_circular_dependencies(self) -> List[str]:
        """Check for circular dependencies between modules"""
        # Add test modules to self.modules if they don't exist
        for module_name in self.graphs.keys():
            if module_name not in self.modules:
                self.modules[module_name] = None
        
        # Build import graph
        for module_name, graph in self.graphs.items():
            imports = [o for s, p, o in graph.triples((None, OWL.imports, None))]
            for imp in imports:
                imp_module = str(imp).split("/")[-1].split("-")[0]
                if imp_module in self.modules:
                    self.import_graph.add_edge(module_name, imp_module)
                    logger.info(f"Added edge: {module_name} -> {imp_module}")
        
        # Check for cycles
        cycles = list(nx.simple_cycles(self.import_graph))
        if cycles:
            return [f"Circular dependency found: {' -> '.join(cycle)}" for cycle in cycles]
        return []

    def check_external_alignments(self) -> List[ModuleValidationResult]:
        """Check alignment with external ontologies"""
        results = []
        
        for module_name, graph in self.graphs.items():
            result = ModuleValidationResult(module_name, True, [], [], [])
            
            # Check for external ontology references
            external_refs = {
                'SNOMED': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
                'HPO': 'http://purl.obolibrary.org/obo/HP_',
                'DOID': 'http://purl.obolibrary.org/obo/DOID_'
            }
            
            for ref_name, ref_uri in external_refs.items():
                refs = [s for s, p, o in graph.triples((None, None, None)) 
                       if str(s).startswith(ref_uri)]
                if refs:
                    result.warnings.append(
                        f"Found {len(refs)} references to {ref_name}"
                    )
                    result.suggestions.append(
                        f"Consider adding owl:equivalentClass or skos:exactMatch for {ref_name} terms"
                    )
            
            results.append(result)
            
        return results

    def validate(self) -> List[ModuleValidationResult]:
        """Run all modularity validation checks"""
        if not self.load_modules():
            return [ModuleValidationResult("all", False, ["Failed to load modules"], [], [])]
            
        results = []
        
        # Run all checks
        results.extend(self.check_module_boundaries())
        results.extend(self.check_import_dependencies())
        results.extend(self.check_external_alignments())
        
        # Check for circular dependencies
        cycles = self.check_circular_dependencies()
        if cycles:
            results.append(ModuleValidationResult(
                "dependencies", False, cycles, [], 
                ["Review and break circular dependencies between modules"]
            ))
        
        return results

def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python validate_modularity.py <ontology_directory>")
        sys.exit(1)
        
    validator = ModularOntologyValidator(sys.argv[1])
    results = validator.validate()
    
    # Print results
    for result in results:
        print(f"\nModule: {result.module_name}")
        if result.is_valid:
            print("✅ Module validation passed")
        else:
            print("❌ Module validation failed")
            
        if result.errors:
            print("\nErrors:")
            for error in result.errors:
                print(f"  - {error}")
                
        if result.warnings:
            print("\nWarnings:")
            for warning in result.warnings:
                print(f"  - {warning}")
                
        if result.suggestions:
            print("\nSuggestions:")
            for suggestion in result.suggestions:
                print(f"  - {suggestion}")

if __name__ == "__main__":
    main() 