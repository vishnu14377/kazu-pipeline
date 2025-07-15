"""
Kazu Ontology Converter

This script provides a unified interface for converting ontologies (both OWL and CSV formats)
to Kazu-compatible tabular format. It supports:
- OWL to Kazu CSV conversion
- CSV to Kazu CSV conversion
- Proper metadata handling for Kazu's TabularOntologyParser
- Multiprocessing for batch processing

Usage:
    python kazu_ontology_converter.py --input <input_file> --output <output_file> --format <owl|csv> --entity-class <class_name> --name <ontology_name> [--data-origin <origin>]
"""

import os
import rdflib
import pandas as pd
import multiprocessing
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the absolute path to the project root (2 levels up from this script)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent

@dataclass
class OntologyMetadata:
    """Metadata required by Kazu's TabularOntologyParser."""
    entity_class: str
    name: str
    data_origin: Optional[str] = None

class KazuOntologyConverter:
    """Converts ontologies to Kazu-compatible tabular format."""
    
    SYNONYM_PREDICATES = [
        "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym",
        "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym",
        "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym",
        "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym",
        "http://www.w3.org/2004/02/skos/core#altLabel",
    ]

    def __init__(self, metadata: OntologyMetadata):
        """Initialize converter with ontology metadata."""
        self.metadata = metadata
        
    def convert_owl(self, owl_path: Union[str, Path], output_path: Union[str, Path]) -> None:
        """
        Convert OWL file to Kazu-compatible CSV format.
        
        Args:
            owl_path: Path to input OWL file
            output_path: Path to output CSV file
        """
        owl_path = Path(owl_path)
        output_path = Path(output_path)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Converting OWL file: {owl_path}")
        g = rdflib.Graph()
        g.parse(str(owl_path))
        
        rows = []
        for s in g.subjects(rdflib.RDF.type, rdflib.OWL.Class):
            entity_id = self._extract_entity_id(s)
            label = self._extract_label(g, s)
            synonyms = self._extract_synonyms(g, s)
            
            if entity_id and label:
                # Add main label as exact match
                rows.append({
                    'DEFAULT_LABEL': label,
                    'SYN': label,
                    'MAPPING_TYPE': 'exact',
                    'ENTITY_CLASS': self.metadata.entity_class,
                    'ONTOLOGY_NAME': self.metadata.name
                })
                
                # Add synonyms
                for syn in synonyms:
                    if syn != label:
                        rows.append({
                            'DEFAULT_LABEL': label,
                            'SYN': syn,
                            'MAPPING_TYPE': 'synonym',
                            'ENTITY_CLASS': self.metadata.entity_class,
                            'ONTOLOGY_NAME': self.metadata.name
                        })
        
        if not rows:
            logger.warning(f"No valid entities found in {owl_path}")
            return
            
        df = pd.DataFrame(rows)
        df.to_csv(output_path, index=False)
        logger.info(f"Wrote {len(rows)} rows to {output_path}")
        
    def convert_csv(self, csv_path: Union[str, Path], output_path: Union[str, Path]) -> None:
        """
        Convert existing CSV to Kazu-compatible format.
        
        Args:
            csv_path: Path to input CSV file
            output_path: Path to output CSV file
        """
        csv_path = Path(csv_path)
        output_path = Path(output_path)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Converting CSV file: {csv_path}")
        df = pd.read_csv(csv_path, low_memory=False)
        
        # Handle LOINC format specifically
        if 'LOINC_NUM' in df.columns:
            logger.info("Detected LOINC format, using LOINC-specific column mapping")
            required_cols = ['LOINC_NUM', 'LONG_COMMON_NAME']
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"LOINC CSV must contain columns: {required_cols}")
            
            rows = []
            for _, row in df.iterrows():
                entity_id = f"LOINC:{row['LOINC_NUM']}"  # Add LOINC: prefix
                label = str(row['LONG_COMMON_NAME'])
                
                # Add main label
                rows.append({
                    'DEFAULT_LABEL': label,
                    'SYN': label,
                    'MAPPING_TYPE': 'exact',
                    'ENTITY_CLASS': self.metadata.entity_class,
                    'ONTOLOGY_NAME': self.metadata.name
                })
                
                # Add synonyms from SHORTNAME, DisplayName, and COMPONENT
                for col in ['SHORTNAME', 'DisplayName', 'COMPONENT']:
                    if col in df.columns and pd.notnull(row[col]):
                        syn = str(row[col]).strip()
                        if syn and syn != label:
                            rows.append({
                                'DEFAULT_LABEL': label,
                                'SYN': syn,
                                'MAPPING_TYPE': 'synonym',
                                'ENTITY_CLASS': self.metadata.entity_class,
                                'ONTOLOGY_NAME': self.metadata.name
                            })
        # Handle files already in Kazu format
        elif all(col in df.columns for col in ['IDX', 'DEFAULT_LABEL', 'SYN', 'MAPPING_TYPE']):
            logger.info("Detected Kazu format, adding metadata columns")
            df['ENTITY_CLASS'] = self.metadata.entity_class
            df['ONTOLOGY_NAME'] = self.metadata.name
            df.to_csv(output_path, index=False)
            logger.info(f"Wrote {len(df)} rows to {output_path}")
            return
        else:
            # Handle generic CSV format
            required_cols = ['entity_id', 'label', 'synonyms']
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"Input CSV must contain columns: {required_cols}")
                
            rows = []
            for _, row in df.iterrows():
                entity_id = row['entity_id']
                label = str(row['label'])
                
                # Add main label
                rows.append({
                    'DEFAULT_LABEL': label,
                    'SYN': label,
                    'MAPPING_TYPE': 'exact',
                    'ENTITY_CLASS': self.metadata.entity_class,
                    'ONTOLOGY_NAME': self.metadata.name
                })
                
                # Add synonyms
                if pd.notnull(row['synonyms']) and row['synonyms']:
                    for syn in str(row['synonyms']).split('|'):
                        syn = syn.strip()
                        if syn and syn != label:
                            rows.append({
                                'DEFAULT_LABEL': label,
                                'SYN': syn,
                                'MAPPING_TYPE': 'synonym',
                                'ENTITY_CLASS': self.metadata.entity_class,
                                'ONTOLOGY_NAME': self.metadata.name
                            })
        
        if not rows:
            logger.warning(f"No valid entities found in {csv_path}")
            return
            
        out_df = pd.DataFrame(rows)
        out_df.to_csv(output_path, index=False)
        logger.info(f"Wrote {len(rows)} rows to {output_path}")
    
    def _extract_entity_id(self, subject: rdflib.term.URIRef) -> Optional[str]:
        """Extract entity ID from RDF subject."""
        if isinstance(subject, rdflib.term.URIRef):
            return str(subject)
        return None
    
    def _extract_label(self, graph: rdflib.Graph, subject: rdflib.term.URIRef) -> Optional[str]:
        """Extract label from RDF subject."""
        return next((str(o) for o in graph.objects(subject, rdflib.RDFS.label)), None)
    
    def _extract_synonyms(self, graph: rdflib.Graph, subject: rdflib.term.URIRef) -> List[str]:
        """Extract synonyms from RDF subject."""
        return [str(o) for pred_uri in self.SYNONYM_PREDICATES 
                for o in graph.objects(subject, rdflib.URIRef(pred_uri))]

def process_ontology(args: Tuple[Path, Path, OntologyMetadata]) -> None:
    """Process a single ontology file (for multiprocessing)."""
    input_path, output_path, metadata = args
    converter = KazuOntologyConverter(metadata)
    
    try:
        if input_path.suffix == '.owl':
            converter.convert_owl(input_path, output_path)
        else:
            converter.convert_csv(input_path, output_path)
    except Exception as e:
        logger.error(f"Error processing {input_path}: {str(e)}")

def batch_convert(input_dir: Union[str, Path], output_dir: Union[str, Path], metadata: Optional[OntologyMetadata] = None, 
                 num_processes: Optional[int] = None, metadata_map: Optional[dict] = None) -> None:
    """
    Convert multiple ontology files in parallel.
    Args:
        input_dir: Directory containing input files
        output_dir: Directory for output files
        metadata: Ontology metadata (used if metadata_map is None)
        num_processes: Number of processes to use (default: CPU count)
        metadata_map: Optional dict mapping filename to {'entity_class': ..., 'name': ...}
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_files = []
    for ext in ['.owl', '.csv']:
        input_files.extend(list(input_dir.glob(f'*{ext}')))
    if not input_files:
        logger.warning(f"No input files found in {input_dir}")
        return
    args_list = []
    for input_file in input_files:
        output_file = output_dir / f"{input_file.stem}_kazu.csv"
        if metadata_map:
            meta = metadata_map.get(input_file.name)
            if not meta:
                logger.warning(f"No metadata found for {input_file.name}, skipping.")
                continue
            file_metadata = OntologyMetadata(entity_class=meta['entity_class'], name=meta['name'])
        else:
            file_metadata = metadata
        args_list.append((input_file, output_file, file_metadata))
    if not args_list:
        logger.warning("No files to process after metadata filtering.")
        return
    num_processes = num_processes or min(multiprocessing.cpu_count(), len(args_list))
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(process_ontology, args_list)

def load_metadata_csv(metadata_file: str) -> dict:
    import csv
    metadata = {}
    with open(metadata_file, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            metadata[row['filename']] = {
                'entity_class': row['entity_class'],
                'name': row['name']
            }
    return metadata

def main():
    """Command-line interface for the converter."""
    import argparse
    parser = argparse.ArgumentParser(description='Convert ontologies to Kazu-compatible format')
    parser.add_argument('--input', required=True, help='Input file or directory path')
    parser.add_argument('--output', required=True, help='Output file or directory path')
    parser.add_argument('--entity-class', help='Entity class name')
    parser.add_argument('--name', help='Ontology name')
    parser.add_argument('--data-origin', help='Data origin description')
    parser.add_argument('--format', choices=['owl', 'csv'], help='Input format (required for single file)')
    parser.add_argument('--batch', action='store_true', help='Process all files in input directory')
    parser.add_argument('--processes', type=int, help='Number of processes for batch processing')
    parser.add_argument('--metadata', help='CSV file mapping filename to entity_class and name (for batch mode)')
    args = parser.parse_args()
    if args.batch:
        if not os.path.isdir(args.input):
            raise ValueError("Input must be a directory when using --batch")
        if args.metadata:
            metadata_map = load_metadata_csv(args.metadata)
            batch_convert(args.input, args.output, None, args.processes, metadata_map)
        else:
            if not args.entity_class or not args.name:
                raise ValueError("--entity-class and --name are required if --metadata is not provided in batch mode")
            metadata = OntologyMetadata(
                entity_class=args.entity_class,
                name=args.name,
                data_origin=args.data_origin
            )
            batch_convert(args.input, args.output, metadata, args.processes)
    else:
        if not args.format:
            raise ValueError("--format is required for single file conversion")
        if not args.entity_class or not args.name:
            raise ValueError("--entity-class and --name are required for single file conversion")
        metadata = OntologyMetadata(
            entity_class=args.entity_class,
            name=args.name,
            data_origin=args.data_origin
        )
        converter = KazuOntologyConverter(metadata)
        if args.format == 'owl':
            converter.convert_owl(args.input, args.output)
        else:
            converter.convert_csv(args.input, args.output)

if __name__ == "__main__":
    main() 