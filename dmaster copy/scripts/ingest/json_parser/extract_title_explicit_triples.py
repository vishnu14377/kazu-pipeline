"""
extract_title_explicit_triples.py

Extracts explicit RDF/OWL triples from a cohort definition JSON file, focusing on disease, temporal concepts, and edit URL in the cohort title.

- Usage: python extract_title_explicit_triples.py <cohort_json_file>
  - <cohort_json_file> can be just the filename (searched in the default cohort directory) or an absolute path.
- The script parses the title to extract disease and temporal constraints.
- Temporal constraints (e.g., 'Earliest event', 'First occurrence') are modeled as time:TemporalEntity and linked to the cohort with :hasTemporalConstraint.
- The cohort ID is emitted as a data property triple (dct:identifier) with integer type.
- The edit_url is emitted as both an rdfs:seeAlso and foaf:page triple linking the cohort to the URL (if present).
- Output is printed as Turtle-style triples.

"""
import os
import re
import json

# Directory containing cohort definition JSON files
COHORT_DIR = os.path.join(os.path.dirname(__file__), '../../example_input/cohortDefinitionOutputs')
COHORT_DIR = os.path.abspath(COHORT_DIR)

# Helper: extract disease and temporal from title
def parse_title(title):
    """
    Extracts disease and temporal constraint from the cohort title.
    - Disease: text after 'of'
    - Temporal: matches known temporal phrases (e.g., 'Earliest event')
    Returns (disease, temporal) tuple.
    """
    disease = None
    temporal = None
    # Extract disease (after 'of')
    m = re.search(r'of (.+)', title, re.IGNORECASE)
    if m:
        disease = m.group(1).strip()
    # Extract temporal (before 'of')
    m2 = re.search(r'(Earliest event|First occurrence|Latest event|Initial diagnosis)', title, re.IGNORECASE)
    if m2:
        temporal = m2.group(1).strip()
    return disease, temporal

# Main script logic
import sys
if len(sys.argv) < 2:
    print("Usage: python extract_title_explicit_triples.py <cohort_json_file>")
    sys.exit(1)

fname = sys.argv[1]
# Accept both absolute path and just filename
if not os.path.isabs(fname):
    fname = os.path.join(COHORT_DIR, fname)

with open(fname, encoding='utf-8') as f:
    data = json.load(f)
    cohort_id = data.get('id', 'Unknown')
    title = data.get('name', '')
    edit_url = data.get('edit_url', None)
    print(f"# Cohort ID: {cohort_id}")
    print(f"# Title: {title}")
    disease, temporal = parse_title(title)
    cohort_uri = f":Cohort{cohort_id}"
    print(f"\n{cohort_uri} rdfs:label \"{title}\" .")
    # Emit cohort ID as a data property triple (dct:identifier)
    if cohort_id != 'Unknown':
        print(f"{cohort_uri} dct:identifier \"{cohort_id}\"^^xsd:integer .")
    # Emit edit_url as both rdfs:seeAlso and foaf:page if present
    if edit_url:
        print(f"{cohort_uri} rdfs:seeAlso <{edit_url}> .")
        print(f"{cohort_uri} foaf:page <{edit_url}> .")
    if disease:
        # In real use, map to ontology URI (e.g., DOID, SNOMED). Here, just show as a comment.
        print(f"{cohort_uri} dct:subject :{disease.replace(' ', '')} .  # {disease}")
    if temporal:
        # Model temporal constraint as a time:TemporalEntity and link to cohort
        print(f"{cohort_uri} :hasTemporalConstraint :{temporal.replace(' ', '')} .")
        print(f":{temporal.replace(' ', '')} a time:TemporalEntity ; rdfs:label \"{temporal}\" .") 