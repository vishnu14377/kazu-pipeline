# Kazu Ontology Preparation Pipeline

This directory contains scripts for preparing biomedical ontologies for use with Kazu's NER pipeline. The process converts OWL and CSV ontologies into Kazu-compatible tabular dictionaries, adds metadata, and ensures all outputs are in the correct format (no deprecated IDX column).

## Pipeline Overview (2024 Update)

### 1. **Ontology Extraction**
Convert OWL ontologies to simple CSVs with entity IDs, labels, and synonyms:
```bash
poetry run python scripts/ingest/kazu_prep/owl_to_kazu_csv_batch.py
```
- **Input:** OWL files in `data/ontologies/`
- **Output:** CSVs in `data/dictionaries/` with columns: `entity_id,label,synonyms`
- **Note:** No `IDX` column is present in the output.

### 2. **Tabular Conversion**
Convert the above CSVs into Kazu's tabular format:
```bash
poetry run python scripts/ingest/kazu_prep/convert_to_kazu_tabular.py
```
- **Input:** CSVs from `data/dictionaries/`
- **Output:** Tabular CSVs in `data/tabular_ontologies/` with columns: `DEFAULT_LABEL,SYN,MAPPING_TYPE`
- **Note:** No `IDX` column is present in the output.

### 3. **Add Metadata**
Add Kazu-required metadata columns:
```bash
poetry run python scripts/ingest/kazu_prep/add_kazu_metadata.py
```
- **Input:** Tabular CSVs from `data/tabular_ontologies/`
- **Output:** Final Kazu dictionaries in `data/kazu_formatted_ontologies/` (e.g., `doid_kazu.csv`)
- **Note:** No `IDX` column is present in the output.

### 4. **LOINC Handling**
For LOINC, use the dedicated script:
```bash
poetry run python scripts/ingest/kazu_prep/loinc_csv_to_kazu_dict.py
```
- **Input:** LOINC CSV in `data/dictionaries/loinc.csv` (already in Kazu-compatible format with columns `entity_id,label,synonyms`)
- **Output:** Final LOINC dictionary in `data/kazu_formatted_ontologies/loinc_kazu.csv`
- **Note:** No `IDX` column is present in the output.

---

## Example Output (doid_kazu.csv)
```
DEFAULT_LABEL,SYN,MAPPING_TYPE
angiosarcoma,angiosarcoma,exact
angiosarcoma,hemangiosarcoma,synonym
...
```

## Full Process Summary
1. **owl_to_kazu_csv_batch.py**: Extracts entity_id, label, and synonyms from OWL files. Output: `data/dictionaries/*.csv`
2. **convert_to_kazu_tabular.py**: Converts to Kazu tabular format. Output: `data/tabular_ontologies/*.csv`
3. **add_kazu_metadata.py**: Adds metadata, finalizes for Kazu. Output: `data/kazu_formatted_ontologies/*_kazu.csv`
4. **loinc_csv_to_kazu_dict.py**: Processes LOINC CSV from `data/dictionaries/loinc.csv` into a Kazu-compatible dictionary.

## Notes
- The deprecated `IDX` column is no longer present in any output.
- All scripts should be run from the project root (`dMaster`).
- If you add new ontologies, place them in `data/ontologies/` and rerun the pipeline.
- For troubleshooting, check logs and ensure all input files are present and correctly formatted.

---

## (Legacy/Reference) Previous Steps and Details

# Kazu Setup and Preparation

This directory contains scripts for setting up and preparing Kazu for biomedical NER tasks.

## Initial Setup

### Prerequisites

1. Create a `.env` file in your project root with your BioPortal API key:
```bash
# Get your API key from https://bioportal.bioontology.org/account
BIOPORTAL_API_KEY=your_api_key_here
```

2. Ensure you have the required Python packages:
```bash
poetry add protobuf tiktoken rdflib pandas
```

### Step 1: Download Required Models

The `download_biobert.py` script downloads the necessary ML models for Kazu:
- BioBERT (primary model for biomedical NER)
- BigBird (optional, currently has known tokenizer issues)

Run it from your project root:
```bash
poetry run python scripts/ingest/kazu_prep/download_biobert.py
```

Expected output:
```
Downloading models to: /path/to/your/project/data/huggingface_models
Downloading biobert from dmis-lab/biobert-base-cased-v1.1 ...
Successfully saved biobert to /path/to/your/project/data/huggingface_models/biobert
```

Note: The BigBird model may fail to download due to tokenizer issues. This is not critical for most biomedical NER tasks as BioBERT is the primary model.

### Step 2: Download Required Ontologies

The `download_ontologies.py` script downloads the necessary biomedical ontologies:
- DOID (Disease Ontology)
- HPO (Human Phenotype Ontology)
- SNOMED CT
- And others...

Run it from your project root:
```bash
poetry run python scripts/ingest/kazu_prep/download_ontologies.py
```

Expected output:
```
Downloading https://raw.githubusercontent.com/BioAssayOntology/BAO/master/bao_complete.owl -> /path/to/your/project/data/ontologies/bao.owl
Downloaded /path/to/your/project/data/ontologies/bao.owl
...
```

Note: Some ontologies require special handling:
- LOINC: 
  1. Download the LOINC Table CSV from https://loinc.org/downloads/loinc-table/
     - You need the "LOINC Table" CSV file, not the OWL/FHIR format
     - The file should have columns like LOINC_NUM, LONG_COMMON_NAME, etc.
  2. Place the CSV file in data/ontologies/loinc.csv
  3. Convert to Kazu format using the specialized LOINC converter:
  ```bash
  poetry run python scripts/ingest/kazu_prep/loinc_csv_to_kazu_dict.py \
      --input data/ontologies/loinc.csv \
      --output data/kazu_ontologies/loinc_kazu.csv
  ```
  This script handles LOINC's specific format and adds the required LOINC: prefix to entity IDs.
- SNOMED CT: Requires license and manual download
- Other ontologies may have specific format requirements

### Step 3: Convert Ontologies to Kazu Format

The `kazu_ontology_converter.py` script converts the downloaded OWL files into Kazu-compatible CSV format. The converter:
- Extracts entity IDs, labels, and synonyms from OWL files
- Handles multiple synonym types (exact, related, broad, narrow)
- Creates properly formatted CSV files for Kazu's TabularOntologyParser
- Supports both single file and batch processing

#### Convert a Single Ontology

```bash
poetry run python scripts/ingest/kazu_prep/kazu_ontology_converter.py \
    --input data/ontologies/doid.owl \
    --output data/kazu_ontologies/doid_kazu.csv \
    --format owl \
    --entity-class Disease \
    --name DOID
```

Expected output:
```
Converting OWL file: data/ontologies/doid.owl
Wrote 36702 rows to data/kazu_ontologies/doid_kazu.csv
```

The output CSV will have these columns:
- IDX: Entity identifier (e.g., DOID URI)
- DEFAULT_LABEL: Primary label for the entity
- SYN: Synonym or exact match
- MAPPING_TYPE: Either 'exact' or 'synonym'
- ENTITY_CLASS: The class name you specified (e.g., 'Disease')
- ONTOLOGY_NAME: The ontology name you specified (e.g., 'DOID')

Example output:
```csv
IDX,DEFAULT_LABEL,SYN,MAPPING_TYPE,ENTITY_CLASS,ONTOLOGY_NAME
http://purl.obolibrary.org/obo/DOID_0001816,angiosarcoma,angiosarcoma,exact,Disease,DOID
http://purl.obolibrary.org/obo/DOID_0001816,angiosarcoma,hemangiosarcoma,synonym,Disease,DOID
```

#### Convert All Ontologies in Batch

```bash
poetry run python scripts/ingest/kazu_prep/kazu_ontology_converter.py \
    --input data/ontologies \
    --output data/kazu_ontologies \
    --entity-class Disease \
    --name DOID \
    --batch
```

The batch mode:
- Processes all .owl and .csv files in the input directory
- Uses multiprocessing for faster conversion
- Creates output files with '_kazu.csv' suffix
- Automatically creates the output directory if it doesn't exist

## Directory Structure

After running these scripts, you should have:
```
data/
├── huggingface_models/
│   └── biobert/
│       └── [model files]
├── ontologies/
│   ├── bao.owl
│   ├── cso.owl
│   ├── dct.owl
│   ├── doid.owl
│   ├── efo.owl
│   ├── hp.owl
│   ├── mondo.owl
│   ├── obcs.owl
│   ├── obi.owl
│   ├── provo.owl
│   ├── sepio.owl
│   ├── snomedct.owl
│   ├── snomedct_us.owl
│   └── [other ontology files]
└── kazu_ontologies/
    ├── cso_kazu.csv
    ├── doid_kazu.csv
    ├── hp_kazu.csv
    ├── obcs_kazu.csv
    ├── obi_kazu.csv
    ├── provo_kazu.csv
    ├── sepio_kazu.csv
    └── [other converted files]
```

Note: Some ontologies may not convert successfully due to syntax errors or format issues. The converter will log these errors and continue with the remaining files.

## Troubleshooting

1. **BioPortal API Key Issues**
   - Ensure your `.env` file is in the project root
   - Verify your API key is valid at https://bioportal.bioontology.org/account

2. **Model Download Issues**
   - If BioBERT download fails, check your internet connection
   - If BigBird fails, this is expected and not critical

3. **Ontology Download Issues**
   - Some ontologies may require manual download due to licensing
   - Check the console output for specific error messages

4. **Conversion Issues**
   - If an ontology fails to convert, check the OWL file format
   - Some ontologies may require special handling (see custom_csv_parser.py for examples)
   - Check the logs for specific error messages
   - Common issues:
     - Missing rdfs:label for entities
     - Malformed OWL syntax
     - Large ontologies may take longer to process

## Next Steps

After completing the initial setup, you can proceed to:
1. Setting up Kazu configuration
2. Running NER tasks

See the other scripts in this directory for these next steps. 