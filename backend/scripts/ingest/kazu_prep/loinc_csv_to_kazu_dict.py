import pandas as pd
import argparse
import logging
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_loinc_to_kazu_dict(loinc_csv_path, output_path):
    """
    Convert LOINC CSV to Kazu-compatible dictionary format.
    
    Args:
        loinc_csv_path: Path to input LOINC CSV file
        output_path: Path to output Kazu-compatible CSV file
    """
    try:
        # Read LOINC CSV
        logger.info(f"Reading LOINC CSV from: {loinc_csv_path}")
        loinc_df = pd.read_csv(loinc_csv_path, low_memory=False)
        
        # Verify required columns
        required_cols = ['entity_id', 'label', 'synonyms']
        missing_cols = [col for col in required_cols if col not in loinc_df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Finalize DataFrame
        kazu_df_final = loinc_df[['entity_id', 'label', 'synonyms']]
        
        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Drop 'IDX' column if it exists
        if 'IDX' in kazu_df_final.columns:
            kazu_df_final = kazu_df_final.drop(columns=['IDX'])
        
        # Save to CSV
        kazu_df_final.to_csv(output_path, index=False)
        logger.info(f"Successfully wrote {len(kazu_df_final)} rows to: {output_path}")
        
    except Exception as e:
        logger.error(f"Error converting LOINC CSV: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert LOINC CSV to Kazu dictionary.')
    parser.add_argument('--input', default="data/dictionaries/loinc.csv", help='Path to input LOINC CSV file.')
    parser.add_argument('--output', default="data/kazu_formatted_ontologies/loinc_kazu.csv", help='Path to output Kazu-compatible dictionary CSV file.')
    
    args = parser.parse_args()
    
    convert_loinc_to_kazu_dict(args.input, args.output) 