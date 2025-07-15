#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Optional
import logging
from dataclasses import dataclass
import subprocess
from owlready2 import *
import rdflib
from rdflib import Graph, Namespace
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import OWL, RDF, RDFS, XSD, SKOS, DC, DCTERMS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Class to store validation results"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class OntologyValidator:
    """Main class for ontology validation"""
    
    def __init__(self, ontology_dir: str):
        self.ontology_dir = Path(ontology_dir)
        self.main_ontology = self.ontology_dir / "main_ontology" / "ontology.ttl"
        self.world = World()
        self.g = Graph()
        
        # Load common prefixes
        self.g.bind("owl", OWL)
        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("xsd", XSD)
        
    def load_ontology(self) -> bool:
        """Load the main ontology and all its imports"""
        try:
            logger.info("Loading main ontology...")
            onto = self.world.get_ontology(str(self.main_ontology)).load()
            logger.info("Successfully loaded main ontology")
            return True
        except Exception as e:
            logger.error(f"Failed to load ontology: {str(e)}")
            return False

    def check_consistency(self) -> ValidationResult:
        """Check ontology consistency using HermiT reasoner"""
        try:
            logger.info("Running consistency check...")
            sync_reasoner()
            inconsistent_classes = list(self.world.inconsistent_classes())
            
            if inconsistent_classes:
                errors = [f"Inconsistent class found: {cls.name}" for cls in inconsistent_classes]
                return ValidationResult(False, errors, [], [])
            
            return ValidationResult(True, [], [], [])
            
        except Exception as e:
            return ValidationResult(False, [f"Reasoner error: {str(e)}"], [], [])

    def check_duplicate_classes(self) -> ValidationResult:
        """Check for duplicate class definitions across modules"""
        try:
            logger.info("Checking for duplicate classes...")
            query = """
            SELECT ?class1 ?class2 ?label WHERE {
                ?class1 a owl:Class; rdfs:label ?label.
                ?class2 a owl:Class; rdfs:label ?label.
                FILTER(?class1 != ?class2)
            }
            """
            
            results = self.g.query(query)
            duplicates = list(results)
            
            if duplicates:
                errors = [f"Duplicate classes found: {row.class1} and {row.class2} (label: {row.label})" 
                         for row in duplicates]
                suggestions = [f"Consider adding owl:equivalentClass between {row.class1} and {row.class2}"
                             for row in duplicates]
                return ValidationResult(False, errors, [], suggestions)
            
            return ValidationResult(True, [], [], [])
            
        except Exception as e:
            return ValidationResult(False, [f"Error checking duplicates: {str(e)}"], [], [])

    def check_property_domains(self) -> ValidationResult:
        """Check for property domain conflicts"""
        try:
            logger.info("Checking property domains...")
            query = """
            SELECT ?prop (COUNT(DISTINCT ?domain) as ?domainCount) WHERE {
                ?prop a owl:ObjectProperty.
                ?prop rdfs:domain ?domain.
            } GROUP BY ?prop HAVING (COUNT(DISTINCT ?domain) > 1)
            """
            
            results = self.g.query(query)
            conflicts = list(results)
            
            if conflicts:
                warnings = [f"Property {row.prop} has multiple domains ({row.domainCount})" 
                          for row in conflicts]
                suggestions = [f"Review domain definitions for {row.prop} and consider consolidating"
                             for row in conflicts]
                return ValidationResult(True, [], warnings, suggestions)
            
            return ValidationResult(True, [], [], [])
            
        except Exception as e:
            return ValidationResult(False, [f"Error checking property domains: {str(e)}"], [], [])

    def check_imports(self) -> ValidationResult:
        """Check for missing or broken imports"""
        try:
            logger.info("Checking ontology imports...")
            query = """
            SELECT ?ontology ?import WHERE {
                ?ontology owl:imports ?import .
            }
            """
            
            results = self.g.query(query)
            imports = list(results)
            
            errors = []
            warnings = []
            suggestions = []
            
            for row in imports:
                try:
                    # Try to load the imported ontology
                    imported = self.world.get_ontology(str(row['import'])).load()
                except Exception as e:
                    errors.append(f"Failed to load import {row['import']} for {row['ontology']}")
                    suggestions.append(f"Check if {row['import']} exists and is accessible")
            
            return ValidationResult(len(errors) == 0, errors, warnings, suggestions)
            
        except Exception as e:
            return ValidationResult(False, [f"Error checking imports: {str(e)}"], [], [])

    def run_all_checks(self) -> ValidationResult:
        """Run all validation checks"""
        if not self.load_ontology():
            return ValidationResult(False, ["Failed to load ontology"], [], [])
            
        results = []
        results.append(self.check_consistency())
        results.append(self.check_duplicate_classes())
        results.append(self.check_property_domains())
        results.append(self.check_imports())
        
        # Combine all results
        all_valid = all(r.is_valid for r in results)
        all_errors = [e for r in results for e in r.errors]
        all_warnings = [w for r in results for w in r.warnings]
        all_suggestions = [s for r in results for s in r.suggestions]
        
        return ValidationResult(all_valid, all_errors, all_warnings, all_suggestions)

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python validate_ontology.py <ontology_directory>")
        sys.exit(1)
        
    validator = OntologyValidator(sys.argv[1])
    result = validator.run_all_checks()
    
    if result.is_valid:
        print("✅ Ontology validation passed!")
    else:
        print("❌ Ontology validation failed!")
        
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
            
    sys.exit(0 if result.is_valid else 1)

if __name__ == "__main__":
    main() 