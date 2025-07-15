import os
from dotenv import load_dotenv
import requests
import re

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("BIOPORTAL_API_KEY")

if not API_KEY:
    raise ValueError("BIOPORTAL_API_KEY not found in .env file!")

print(f"Loaded API key: {API_KEY[:6]}... (truncated)")

import argparse
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _search_bioportal_for_term(term: str) -> List[Dict[str, Any]]:
    """Searches BioPortal for a given term and returns potential mappings."""
    search_url = "https://data.bioontology.org/search"
    params = {
        "q": term,
        "ontologies": "DOID,HP,SNOMEDCT", # Limit search to relevant ontologies
        "pagesize": 3 # Get top 3 results
    }
    headers = {"Authorization": f"apikey token={API_KEY}"}

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors
        search_results = response.json()
        return search_results.get("collection", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error searching BioPortal for '{term}': {e}")
        return []

def annotate_text(text):
    url = "https://data.bioontology.org/annotator"
    params = {
        "text": text,
        "ontologies": "DOID,HP,SNOMEDCT",
        "longest_only": "true"
    }
    headers = {"Authorization": f"apikey token={API_KEY}"}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        results = response.json()
        matched_terms = set()
        ontology_ids = set()
        logger.info("\nAnnotation Results:")
        for annotation in results:
            for annot in annotation.get("annotations", []):
                class_id = annotation['annotatedClass']['@id']
                term = annot['text']
                matched_terms.add(term.lower()) # Convert to lowercase for consistent comparison
                logger.info(f"Matched: {term} -> {class_id}")
                # Extract ontology acronym from URI
                match = re.search(r'/obo/([A-Z]+)_', class_id)
                if match:
                    ontology_ids.add(match.group(1))
                else:
                    match = re.search(r'/ontology/([A-Z0-9]+)/', class_id)
                    if match:
                        ontology_ids.add(match.group(1))
        if ontology_ids:
            logger.info("\nOntologies used in annotation results (from URI):")
            for ont in sorted(ontology_ids):
                logger.info(f" - {ont}")

        # Identify unmapped terms (simple heuristic: words in text not matched)
        text_terms = set(re.findall(r'\b\w+\b', text.lower())) # Convert text to lowercase for comparison
        unmapped_terms = text_terms - matched_terms
        
        if unmapped_terms:
            logger.info("\nUnmapped terms detected. Suggesting mappings:")
            for term in sorted(unmapped_terms):
                suggestions = _search_bioportal_for_term(term)
                if suggestions:
                    logger.info(f"  - For '{term}':")
                    for s in suggestions:
                        logger.info(f"    - {s.get('prefLabel')} ({s.get('@id')})")
                else:
                    logger.info(f"  - No suggestions found for '{term}'.")
        else:
            logger.info("All terms mapped successfully.")
    else:
        logger.error(f"Error: {response.status_code} - {response.text}")

def main():
    parser = argparse.ArgumentParser(description="BioPortal Annotator Example with Suggestions")
    parser.add_argument('text', help='Text to annotate')
    args = parser.parse_args()

    annotate_text(args.text)

if __name__ == "__main__":
    main()
