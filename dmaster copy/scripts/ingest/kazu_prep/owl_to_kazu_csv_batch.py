import os
import rdflib
import csv
import multiprocessing
from functools import partial
import rdflib.namespace

# Robust path resolution based on script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
OWL_DIR = os.path.join(PROJECT_ROOT, 'data', 'ontologies')
CSV_DIR = os.path.join(PROJECT_ROOT, 'data', 'dictionaries')

ONTOLOGIES = [
    # ("bao.owl", "BAO", "bao.csv"),  # Commented out: Current bao.owl lacks rdfs:label and synonym annotations. To enable BAO extraction, replace bao.owl with a version that includes rdfs:label and synonym annotations for classes (e.g., bao_core.owl or a full release with labels).
    ("CSOontology.owl", "CSO", "cso.csv"),
    # ("dct.owl", "DCT", "dct.csv"),  # DCT not present
    ("dublin_core_elements.owl", "DC", "dc.csv"),
    ("efo.owl", "EFO", "efo.csv"),
    ("doid.owl", "DOID", "doid.csv"),
    ("hp.owl", "HP", "hp.csv"),
    # ("loinc.owl", "LOINC", "loinc.csv"),  # Skip LOINC OWL, use CSV-based dictionary instead
    ("mondo.owl", "MONDO", "mondo.csv"),
    ("obi.owl", "OBI", "obi.csv"),
    ("obcs.owl", "OBCS", "obcs.csv"),
    # ("time.owl", "TIME", "time.csv"),  # Skipped
    ("provo.owl", "PROVO", "provo.csv"),
    # ("snomedct_us.owl", "SNOMEDCT_US", "snomedct_us.csv"),  # Skipped due to syntax error
    # ("rxnorm.owl", "RXNORM", "rxnorm.csv"),  # Skipped - requires UMLS license
    ("sepio.owl", "SEPIO", "sepio.csv"),
    # ("snomedct.owl", "SNOMEDCT", "snomedct.csv"),  # Skipped due to syntax error
    # ("rdfs.owl", "RDFS", "rdfs.csv"),  # Skipped due to syntax error
]

SYN_PREDICATES = [
    "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym",
    "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym",
    "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym",
    "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym",
    "http://www.w3.org/2004/02/skos/core#altLabel",
]

def process_term(s, g, writer, prefix, allow_any_uri=False):
    """
    Extracts entity_id, label, and synonyms for a given subject s.
    If allow_any_uri is True, uses the full URI as entity_id if prefix is not found.
    """
    try:
        if isinstance(s, rdflib.term.URIRef):
            frag = s.split('/')[-1]
            entity_id = None
            if prefix in frag:
                entity_id = frag.replace('_', ':')
            elif allow_any_uri:
                entity_id = str(s)
            if not entity_id:
                return  # Skip if entity_id invalid
        else:
            return
        # Get label
        label = next((str(o) for o in g.objects(s, rdflib.RDFS.label)), None)
        if not label:
            return
        # Get synonyms
        synonyms = {str(o) for pred_uri in SYN_PREDICATES for o in g.objects(s, rdflib.URIRef(pred_uri))}
        writer.writerow([entity_id, label, '|'.join(synonyms)])
    except Exception as e:
        # Log and skip problematic terms
        print(f"[WARN] Skipping term {s}: {e}")

def extract_terms(owl_path, prefix, output_csv):
    g = rdflib.Graph()
    print(f"Parsing {owl_path} ...")
    g.parse(owl_path)
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Add idx column to CSV header
        writer.writerow(['entity_id', 'label', 'synonyms'])
        allow_any_uri = (prefix == "CSO")
        # Extract owl:Class elements (all ontologies)
        for s in g.subjects(rdflib.RDF.type, rdflib.OWL.Class):
            process_term(s, g, writer, prefix, allow_any_uri)
        # For DC and PROVO, extract additional properties
        if prefix in {"DC", "PROVO"}:
            for prop_type in [rdflib.namespace.RDF.Property, rdflib.OWL.ObjectProperty,
                              rdflib.OWL.DatatypeProperty, rdflib.OWL.AnnotationProperty]:
                for s in g.subjects(rdflib.RDF.type, prop_type):
                    process_term(s, g, writer, prefix, allow_any_uri=True)
        # Legacy support for rdf:Description elements
        for s in g.subjects(None, None):
            if isinstance(s, rdflib.term.URIRef) and 'Description' in str(s):
                process_term(s, g, writer, prefix, allow_any_uri)
    print(f"Wrote {output_csv}")

def process_ontology(ontology_info):
    owl_file, prefix, csv_file = ontology_info
    owl_path = os.path.join(OWL_DIR, owl_file)
    output_csv = os.path.join(CSV_DIR, csv_file)
    if not os.path.exists(owl_path):
        print(f"WARNING: {owl_path} not found, skipping.")
        return
    extract_terms(owl_path, prefix, output_csv)

def main():
    os.makedirs(CSV_DIR, exist_ok=True)
    # Use multiprocessing to process ontologies in parallel
    num_processes = min(multiprocessing.cpu_count(), len(ONTOLOGIES))
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_ontology, ONTOLOGIES)

if __name__ == "__main__":
    main() 