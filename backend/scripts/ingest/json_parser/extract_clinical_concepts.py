"""
extract_clinical_concepts.py

Extracts concepts and relationships from the clinical_description field of a cohort definition JSON file.
This module implements the following steps:
1. Text Preprocessing: Cleans the text, removes citations, normalizes unicode, and tokenizes sentences.
2. Concept Extraction: Uses biomedical NER to identify diseases, symptoms, anatomy, risk factors, etc.
3. Ontology Alignment: Maps extracted terms to canonical URIs (e.g., DOID, SNOMED CT, HPO) using both NER and NCBO BioPortal Annotator API.
4. Relationship Extraction: Uses dependency parsing and rule-based patterns to extract relationships.
5. Triple Generation: Generates RDF/OWL triples for each concept and relationship, with provenance metadata.

Usage:
    python extract_clinical_concepts.py <cohort_json_file>
"""

import os
import re
import json
from datetime import datetime
from kazu.pipeline import Pipeline
import kazu
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig, OmegaConf

from kazu.data import Document, Entity, Section
from kazu.utils.constants import HYDRA_VERSION_BASE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_text(text):
    """
    Preprocess the clinical description text:
    - Remove citations (e.g., [1-3], [4]).
    - Normalize unicode (e.g., "–" to "-").
    - Expand contractions (e.g., "isn't" to "is not").
    - Remove extra whitespace.
    Returns the cleaned text.
    """
    # Remove citations
    text = re.sub(r'\[\d+(-\d+)?\]', '', text)
    # Normalize unicode
    text = text.replace('–', '-').replace('—', '-')
    # Expand contractions (simplified example)
    text = text.replace("isn't", "is not").replace("don't", "do not")
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_concepts(text):
    """
    Extract concepts from the preprocessed text using biomedical NER.
    Returns a list of extracted entities (e.g., diseases, symptoms, anatomy, risk factors).
    """
    # Placeholder: In practice, use a biomedical NER model
    return []

def annotate_with_ncbo(text, api_key):
    """
    Call the NCBO BioPortal Annotator API to extract ontology IDs from the text.
    Returns a dictionary mapping extracted terms to their ontology IDs.
    """
    url = "https://data.bioontology.org/annotator"
    headers = {
        "Authorization": f"apikey token={api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "ontologies": ["DOID", "SNOMEDCT", "HPO", "MESH"]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        annotations = response.json()
        ontology_map = {}
        for annotation in annotations:
            term = annotation.get("annotatedText")
            ontology_id = annotation.get("annotations", [{}])[0].get("class", {}).get("@id")
            if term and ontology_id:
                ontology_map[term] = ontology_id
        return ontology_map
    else:
        print(f"Error calling NCBO API: {response.status_code}")
        return {}

def align_to_ontology(entities, ncbo_map):
    """
    Align extracted entities to canonical URIs (e.g., DOID, SNOMED CT, HPO).
    Merges results from NER and NCBO BioPortal Annotator API.
    Returns a dictionary mapping entities to URIs.
    """
    # Placeholder: In practice, use a lookup service or API
    ontology_map = {
        "Crohn's disease": "DOID:8778",
        "chronic inflammation": "HPO:0002722",
        "smoking": "SNOMEDCT:449868002",
        # Add more mappings as needed
    }
    # Merge NER and NCBO results
    for entity in entities:
        if entity not in ontology_map and entity in ncbo_map:
            ontology_map[entity] = ncbo_map[entity]
    return {entity: ontology_map.get(entity, None) for entity in entities}

def extract_relationships(text, entities):
    """
    Extract relationships between concepts using dependency parsing and rule-based patterns.
    Returns a list of (subject, predicate, object) tuples.
    """
    # Placeholder: In practice, use a dependency parser
    return []

def generate_triples(entities, relationships, cohort_id):
    """
    Generate RDF/OWL triples for each concept and relationship, with provenance metadata.
    Returns a list of Turtle-style triples.
    """
    triples = []
    cohort_uri = f":Cohort{cohort_id}"
    timestamp = datetime.now().isoformat()

    # Generate triples for entities
    for entity, uri in entities.items():
        if uri:
            triples.append(f":{entity.replace(' ', '')} a :Concept ; rdfs:label \"{entity}\" ; owl:sameAs <{uri}> .")

    # Generate triples for relationships
    for subj, pred, obj in relationships:
        triple = f":{subj.replace(' ', '')} :{pred} :{obj.replace(' ', '')} ."
        # Add provenance metadata using RDF-star
        triples.append(f"<< {triple} >> prov:wasDerivedFrom {cohort_uri} ; prov:generatedAtTime \"{timestamp}\"^^xsd:dateTime .")

    return triples

def load_cohort_definition(file_path: str) -> dict:
    """Load a cohort definition JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def extract_text_from_cohort(cohort_data: dict) -> str:
    """Extract relevant text from cohort definition."""
    text_parts = []
    
    # Extract name and description
    if 'name' in cohort_data:
        text_parts.append(cohort_data['name'])
    if 'description' in cohort_data:
        text_parts.append(cohort_data['description'])
        
    # Extract criteria text
    if 'expression' in cohort_data:
        expression = cohort_data['expression']
        if isinstance(expression, dict):
            # Handle different types of expressions
            if 'text' in expression:
                text_parts.append(expression['text'])
            elif 'criteria' in expression:
                for criterion in expression['criteria']:
                    if isinstance(criterion, dict) and 'text' in criterion:
                        text_parts.append(criterion['text'])
    
    return ' '.join(text_parts)

def create_document(text: str, doc_id: str) -> Document:
    """Create a Kazu Document from text."""
    section = Section(text=text, name="main")
    return Document(sections=[section], idx=doc_id)

def process_cohort_definition(file_path: str, pipeline: Pipeline) -> Tuple[Document, List[Entity]]:
    """Process a cohort definition file through the Kazu pipeline."""
    # Load and extract text
    cohort_data = load_cohort_definition(file_path)
    text = extract_text_from_cohort(cohort_data)
    
    # Create document
    doc_id = os.path.basename(file_path).replace('.json', '')
    doc = create_document(text, doc_id)
    
    # Process through pipeline
    pipeline(doc)
    
    # Extract entities
    entities = doc.get_entities()
    
    return doc, entities

import argparse

def main():
    parser = argparse.ArgumentParser(description="Extract clinical concepts from cohort JSON")
    parser.add_argument('input_file', help='Path to cohort JSON file')
    args = parser.parse_args()

    # Use Hydra to load the default Kazu pipeline config and instantiate the pipeline
    conf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "conf"))
    hydra.initialize_config_dir(config_dir=conf_dir, version_base=HYDRA_VERSION_BASE)
    cfg = hydra.compose(config_name="config")
    pipeline = hydra.utils.instantiate(cfg.Pipeline)
    logger.info("Kazu pipeline loaded successfully.")

    # Process input file
    input_file = args.input_file
    doc, entities = process_cohort_definition(input_file, pipeline)
    
    # Print results
    print(f"\nProcessed document: {doc.idx}")
    print(f"Found {len(entities)} entities:")
    for entity in entities:
        print(f"- {entity.match} ({entity.entity_class})")
        if entity.mappings:
            for mapping in entity.mappings:
                print(f"  Mapped to: {mapping.default_label} ({mapping.source}:{mapping.idx})")

if __name__ == "__main__":
    main()
