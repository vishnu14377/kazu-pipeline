import rdflib
from rdflib.namespace import OWL, RDF, RDFS
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_ontology_integrity(ontology_path):
    g = rdflib.Graph()
    try:
        g.parse(ontology_path, format='ttl')
    except Exception as e:
        logger.error(f"Failed to parse ontology file {ontology_path}: {e}")
        sys.exit(1)

    # Check for duplicate classes by label
    labels = {}
    duplicates = []
    for s, p, o in g.triples((None, RDFS.label, None)):
        if o in labels:
            duplicates.append((labels[o], s, o))
        else:
            labels[o] = s

    if duplicates:
        logger.warning("Duplicate class labels found:")
        for dup in duplicates:
            logger.warning(f"Label '{dup[2]}' found in {dup[0]} and {dup[1]}")

    # Check for conflicting triples (same subject and predicate with different objects)
    conflicts = []
    for s, p in g.subject_predicates():
        objs = set(o for o in g.objects(s, p))
        if len(objs) > 1:
            conflicts.append((s, p, objs))

    if conflicts:
        logger.warning("Conflicting triples found:")
        for conflict in conflicts:
            logger.warning(f"Subject {conflict[0]}, Predicate {conflict[1]} has multiple objects: {conflict[2]}")

    logger.info("Ontology integrity validation completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_ontology_integrity.py <ontology_file.ttl>")
        sys.exit(1)
    ontology_file = sys.argv[1]
    validate_ontology_integrity(ontology_file)
