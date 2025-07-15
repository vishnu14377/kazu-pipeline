import os
import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kazu_to_ttl(input_file: str, output_file: str):
    g = Graph()

    # Define namespaces
    KAZU = Namespace("http://example.org/kazu/")
    ONT = Namespace("http://example.org/ontology/")
    g.bind("kazu", KAZU)
    g.bind("ont", ONT)

    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        logger.error(f"Failed to read input CSV file {input_file}: {e}")
        return

    if df.empty:
        logger.warning(f"Input file {input_file} is empty. No triples will be generated.")
        return

    # Validate required columns
    required_cols = ['DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE']
    if not all(col in df.columns for col in required_cols):
        logger.error(f"Missing required columns in {input_file}. Expected: {required_cols}")
        return

    for _, row in df.iterrows():
        default_label = str(row['DEFAULT_LABEL'])
        synonym = str(row['SYN'])
        mapping_type = str(row['MAPPING_TYPE'])

        # Create a URI for the concept based on its default label
        # Sanitize the label to create a valid URI part
        concept_uri = ONT[default_label.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace("/", "_")]

        # Add the concept as a class or individual
        g.add((concept_uri, RDF.type, RDFS.Class)) # Assuming concepts are classes for now
        g.add((concept_uri, RDFS.label, Literal(default_label, lang="en")))

        # Add synonyms based on mapping type
        if mapping_type == 'exact':
            # If the synonym is the same as the default label, it's already added as rdfs:label
            if synonym.lower() != default_label.lower():
                g.add((concept_uri, KAZU.hasExactSynonym, Literal(synonym, lang="en")))
        elif mapping_type == 'synonym':
            g.add((concept_uri, KAZU.hasSynonym, Literal(synonym, lang="en")))
        else:
            logger.warning(f"Unknown mapping type '{mapping_type}' for synonym '{synonym}' of '{default_label}'. Skipping.")

    try:
        g.serialize(destination=output_file, format='turtle')
        logger.info(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        logger.error(f"Failed to write output TTL file {output_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert Kazu tabular CSV to TTL.")
    parser.add_argument("input_file", help="Path to the input Kazu tabular CSV file.")
    parser.add_argument("output_file", help="Path to the output TTL file.")
    args = parser.parse_args()

    kazu_to_ttl(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
