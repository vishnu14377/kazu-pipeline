"""
Add Kazu metadata columns to ontology CSV files.

This script adds the required ENTITY_CLASS and ONTOLOGY_NAME columns to CSV files
that are already in Kazu-compatible format.
"""

import pandas as pd
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define ontology metadata
ONTOLOGY_METADATA = {
    'bao': {'entity_class': 'BioAssay', 'name': 'BAO'},
    'cso': {'entity_class': 'ClinicalStudy', 'name': 'CSO'},
    'dc': {'entity_class': 'Metadata', 'name': 'DC'},
    'doid': {'entity_class': 'Disease', 'name': 'DOID'},
    'efo': {'entity_class': 'ExperimentalFactor', 'name': 'EFO'},
    'hp': {'entity_class': 'Phenotype', 'name': 'HPO'},
    'loinc': {'entity_class': 'LaboratoryTest', 'name': 'LOINC'},
    'mondo': {'entity_class': 'Disease', 'name': 'MONDO'},
    'obcs': {'entity_class': 'StatisticalMethod', 'name': 'OBCS'},
    'obi': {'entity_class': 'Investigation', 'name': 'OBI'},
    'provo': {'entity_class': 'Provenance', 'name': 'PROV-O'},
    'sepio': {'entity_class': 'Evidence', 'name': 'SEPIO'}
}

def add_metadata(input_dir: Path, output_dir: Path):
    """Add Kazu metadata columns to all CSV files in input_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for csv_file in input_dir.glob('*.csv'):
        ontology_name = csv_file.stem
        if ontology_name not in ONTOLOGY_METADATA:
            logger.warning(f"No metadata defined for {ontology_name}, skipping")
            continue
            
        logger.info(f"Processing {csv_file}")
        try:
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Add metadata columns
            metadata = ONTOLOGY_METADATA[ontology_name]
            df['ENTITY_CLASS'] = metadata['entity_class']
            df['ONTOLOGY_NAME'] = metadata['name']
            
            # Drop 'IDX' column if it exists
            if 'IDX' in df.columns:
                df = df.drop(columns=['IDX'])
            
            # Save to output directory
            output_file = output_dir / f"{ontology_name}_kazu.csv"
            df.to_csv(output_file, index=False)
            logger.info(f"Wrote {len(df)} rows to {output_file}")
            
        except Exception as e:
            logger.error(f"Error processing {csv_file}: {str(e)}")

def main():
    # Get the absolute path to the project root (2 levels up from this script)
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent.parent.parent
    
    input_dir = project_root / 'data' / 'tabular_ontologies'
    output_dir = project_root / 'data' / 'kazu_formatted_ontologies'
    
    add_metadata(input_dir, output_dir)

if __name__ == '__main__':
    main() 