
import os
import pandas as pd
import glob
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def convert_to_kazu_tabular(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    required_columns = ['entity_id', 'label', 'synonyms']

    for csv_path in glob.glob(os.path.join(input_dir, '*.csv')):
        logger.info(f"Processing {csv_path}...")
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            logger.error(f"Failed to read {csv_path}: {e}")
            continue

        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"Skipping {csv_path}: missing required columns {missing_cols}.")
            continue

        rows = []
        for i, row in df.iterrows():
            entity_id = row['entity_id']
            label = row.get('label')
            synonyms = row.get('synonyms')

            if pd.isna(entity_id):
                logger.warning(f"Row {i+2} in {csv_path} is missing an entity_id. Skipping.")
                continue

            if pd.isna(label) or not str(label).strip():
                logger.warning(f"Row with entity_id {entity_id} in {csv_path} is missing a preferred label. Skipping.")
                continue
            label = str(label).strip()

            # Add preferred label as a synonym with mapping type 'exact'
            rows.append({'DEFAULT_LABEL': label, 'SYN': label, 'MAPPING_TYPE': 'exact'})

            # Add synonyms
            if pd.notna(synonyms) and str(synonyms).strip():
                # Check for common separators and split
                if '|' in str(synonyms):
                    syn_list = str(synonyms).split('|')
                elif ',' in str(synonyms):
                    syn_list = str(synonyms).split(',')
                    if len(syn_list) < 2:
                        logger.warning(f"Synonyms for {entity_id} in {csv_path} are comma-separated, but only one synonym was found. This may be an error.")
                else:
                    syn_list = [str(synonyms)]
                    logger.warning(f"Synonyms for {entity_id} in {csv_path} do not use a recognized separator (|,). Treating the entire string as a single synonym.")

                for syn in syn_list:
                    syn = syn.strip()
                    if syn and syn.lower() != label.lower():
                        rows.append({'DEFAULT_LABEL': label, 'SYN': syn, 'MAPPING_TYPE': 'synonym'})

        if not rows:
            logger.warning(f"No valid rows to write for {csv_path}. Skipping output.")
            continue

        out_df = pd.DataFrame(rows)
        out_path = os.path.join(output_dir, os.path.basename(csv_path))
        try:
            out_df.to_csv(out_path, index=False)
            logger.info(f"Successfully converted {csv_path} to {out_path}")
        except Exception as e:
            logger.error(f"Failed to write output file {out_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert ontology CSVs to Kazu tabular format.")
    parser.add_argument("input_dir", help="Directory containing the input CSV files.")
    parser.add_argument("output_dir", help="Directory to write the output Kazu tabular files.")
    args = parser.parse_args()

    convert_to_kazu_tabular(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()

