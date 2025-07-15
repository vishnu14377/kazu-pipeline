# Ingest Scripts for dMaster

This directory contains scripts for extracting and processing cohort definition data for ontology modeling in the dMaster project.

## Kazu Ontology Converter

The `kazu_ontology_converter.py` script provides a unified interface for converting ontologies (both OWL and CSV formats) to Kazu-compatible tabular format. It supports:
- OWL to Kazu CSV conversion
- CSV to Kazu CSV conversion
- Proper metadata handling for Kazu's TabularOntologyParser
- Multiprocessing for batch processing

### Usage

#### Single File Conversion
```bash
python kazu_ontology_converter.py \
    --input <input_file> \
    --output <output_file> \
    --format <owl|csv> \
    --entity-class <class_name> \
    --name <ontology_name> \
    [--data-origin <origin>]
```

#### Batch Processing
```bash
python kazu_ontology_converter.py \
    --input <input_directory> \
    --output <output_directory> \
    --entity-class <class_name> \
    --name <ontology_name> \
    --batch \
    [--data-origin <origin>] \
    [--processes <num_processes>]
```

### Output Format

The converter generates CSV files with the following columns:
- `IDX`: Entity identifier
- `DEFAULT_LABEL`: Main label
- `SYN`: Synonym
- `MAPPING_TYPE`: Type of mapping ('exact' or 'synonym')
- `ENTITY_CLASS`: Entity class name
- `ONTOLOGY_NAME`: Ontology name

### Examples

1. Convert a single OWL file:
```bash
python kazu_ontology_converter.py \
    --input data/ontologies/doid.owl \
    --output data/dictionaries/doid_kazu.csv \
    --format owl \
    --entity-class Disease \
    --name DOID \
    --data-origin "Disease Ontology v2023-01-01"
```

2. Convert a single CSV file:
```bash
python kazu_ontology_converter.py \
    --input data/dictionaries/loinc.csv \
    --output data/dictionaries/loinc_kazu.csv \
    --format csv \
    --entity-class LaboratoryTest \
    --name LOINC
```

3. Process all files in a directory:
```bash
python kazu_ontology_converter.py \
    --input data/ontologies \
    --output data/dictionaries \
    --entity-class Concept \
    --name MIXED \
    --batch \
    --processes 4
```

## Other Scripts

### extract_title_explicit_triples.py
- **Purpose:** Extracts explicit RDF/OWL triples from a cohort definition JSON file, focusing on disease and temporal concepts in the cohort title.
- **Temporal Modeling:** Temporal constraints (e.g., 'Earliest event', 'First occurrence') are modeled as `time:TemporalEntity` and linked to the cohort with the `:hasTemporalConstraint` property.
- **Cohort ID Modeling:** The cohort ID is emitted as a data property triple (`dct:identifier`) with integer type (e.g., `:Cohort10616 dct:identifier "10616"^^xsd:integer .`).
- **Edit URL Modeling:** The `edit_url` field is emitted as both an `rdfs:seeAlso` and `foaf:page` triple, linking the cohort to the URL as both a data property and annotation (e.g., `:Cohort10616 rdfs:seeAlso <https://...> .` and `:Cohort10616 foaf:page <https://...> .`).
- **Usage:**
  ```bash
  python extract_title_explicit_triples.py <cohort_json_file>
  ```
  - `<cohort_json_file>` can be just the filename (searched in the default cohort directory) or an absolute path.
- **Output:** Prints Turtle-style triples to stdout.

### bioportal_annotator_example.py
- **Purpose:** Demonstrates how to call the BioPortal Annotator API and extract ontology IDs from text or JSON input.
- **Usage:**
  ```bash
  python bioportal_annotator_example.py <input_file>
  ```

### extract_cohort_json_chunks.py
- **Purpose:** Extracts and prints key fields or chunks from cohort definition JSON files for inspection or further processing.
- **Usage:**
  ```bash
  python extract_cohort_json_chunks.py <cohort_json_file>
  ```

### list_cohort_json_files.py
- **Purpose:** Lists all available cohort definition JSON files in the example input directory.
- **Usage:**
  ```bash
  python list_cohort_json_files.py
  ```

## Notes
- All scripts are intended to be run from the `dMaster` project root unless otherwise specified.
- For ontology modeling, always check and align with canonical URIs and modular ontology best practices.

## Troubleshooting

### Error: `hydra.errors.InstantiationException: Error locating target 'kazu.steps.parsers.custom_csv_parser.CustomCSVParser'`

This error indicates that Hydra (a configuration and instantiation library) can't find the specified Python class `CustomCSVParser` in the module path provided (`kazu.steps.parsers.custom_csv_parser`).

#### Step-by-step solution:

1. **Verify the Module Structure**
   Ensure that your file structure looks exactly like this:
   ```
   kazu/
   └── steps/
       └── parsers/
           └── custom_csv_parser.py
   ```

2. **Check Class Name**
   Within `custom_csv_parser.py`, make sure you have exactly this class:
   ```python
   class CustomCSVParser:
       def __init__(self, some_params=None):
           # your initialization code
           pass

       def parse(self, filepath):
           # parsing logic
           pass
   ```

3. **Check Imports and PYTHONPATH**
   Verify that your Python environment can find the module:
   ```bash
   export PYTHONPATH=/path/to/your/project:$PYTHONPATH
   ```
   Replace `/path/to/your/project` with the absolute path to the parent directory containing `kazu`.

4. **Verify Hydra Configuration**
   Your Hydra configuration (YAML) should precisely match the Python class path:
   ```yaml
   Pipeline:
     steps:
       - parsers0:
           _target_: kazu.steps.parsers.custom_csv_parser.CustomCSVParser
           some_params: value
   ```
   Ensure no typos or mismatches.

5. **Debugging Hydra**
   To get the full traceback, run the command with:
   ```bash
   HYDRA_FULL_ERROR=1 python your_script.py
   ```
   This will display the chained exceptions clearly.

#### Recommended Next Action:
First, ensure the module path and class names exactly match your directory and file contents. Then re-run the Hydra command with the full error option to pinpoint precisely why the import fails. 