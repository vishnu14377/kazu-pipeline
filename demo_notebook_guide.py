# Jupyter Notebook Demo Guide

This guide provides Python code snippets and explanations to demonstrate the end-to-end process of loading cohort JSONs, extracting concepts, generating RDF triples, visualizing the TTL graph, and deploying to GraphDB within a Jupyter Notebook environment.

---

## 1. Setup and Imports

First, ensure you have the necessary libraries installed. You can install them using pip:
```bash
pip install pandas rdflib pyyaml requests python-dotenv
```

Then, import the required modules:
```python
import os
import json
import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, XSD
import yaml
import re
import logging
import subprocess
from dotenv import load_dotenv

# Configure logging for better output in Jupyter
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables (e.g., BIOPORTAL_API_KEY)
load_dotenv()

# Define project root (adjust if your notebook is not in the project root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.getcwd()))
print(f"Project Root: {PROJECT_ROOT}")

# Add scripts directory to Python path
sys.path.append(os.path.join(PROJECT_ROOT, 'scripts', 'ingest', 'json_parser'))
sys.path.append(os.path.join(PROJECT_ROOT, 'scripts', 'ingest', 'kazu_prep'))
sys.path.append(os.path.join(PROJECT_ROOT, 'scripts', 'ontology_validation'))

# Import functions from your custom scripts
from unified_parser import parse_cohort_json, write_triples_to_file, PREFIXES
from kazu_to_ttl import kazu_to_ttl
from validate_ontology_integrity import validate_ontology_integrity
```

---

## 2. Loading Cohort JSON

Let's load one of the example cohort definition JSON files.

```python
# Path to an example JSON file
json_file_path = os.path.join(PROJECT_ROOT, 'example_input', 'cohortDefinitionOutputs', 'cohort_definition_10616.json')

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        cohort_data = json.load(f)
    print(f"Successfully loaded JSON from: {json_file_path}")
    print(json.dumps(cohort_data, indent=2)[:500] + "...") # Print first 500 characters
except Exception as e:
    logger.error(f"Error loading JSON file: {e}")
    cohort_data = None
```

---

## 3. Extracting Concepts and Generating Triples (TTL)

Now, we'll use the `unified_parser.py` to extract concepts and generate RDF triples in Turtle (TTL) format.

```python
if cohort_data:
    output_ttl_dir = os.path.join(PROJECT_ROOT, 'output', 'ttl', 'demo_output')
    os.makedirs(output_ttl_dir, exist_ok=True)
    
    cohort_id = cohort_data.get('id', 'unknown_cohort')
    output_ttl_file = os.path.join(output_ttl_dir, f"cohort_definition_{cohort_id}.ttl")

    try:
        # The parse_cohort_json function expects a file path, so we'll write the loaded data to a temp file
        # or modify unified_parser to accept dict (for demo purposes, we'll use a temp file)
        temp_json_path = os.path.join(output_ttl_dir, f"temp_cohort_{cohort_id}.json")
        with open(temp_json_path, 'w', encoding='utf-8') as f:
            json.dump(cohort_data, f, indent=2)

        # Parse the temporary JSON file
        triples = parse_cohort_json(temp_json_path)
        
        if triples:
            write_triples_to_file(triples, output_ttl_file)
            print(f"Successfully generated TTL file: {output_ttl_file}")
            
            # Display a portion of the generated TTL
            with open(output_ttl_file, 'r', encoding='utf-8') as f:
                print("\n--- Generated TTL (first 50 lines) ---")
                for i, line in enumerate(f):
                    print(line.strip())
                    if i >= 49: # Print first 50 lines
                        print("...")
                        break
                print("------------------------------------")
        else:
            print("No triples generated for the cohort data.")
            
        # Clean up temp file
        os.remove(temp_json_path)

    except Exception as e:
        logger.error(f"Error generating TTL: {e}")
```

---

## 4. Showing TTL Graph (using rdflib)

We can load the generated TTL file into an `rdflib.Graph` object and inspect its contents. For visualization, you would typically use external tools or libraries like `graphviz` (which requires system-level installation). Here, we'll focus on programmatic inspection.

```python
# Load the generated TTL into an RDF graph
g = Graph()
try:
    g.parse(output_ttl_file, format='turtle')
    print(f"Successfully loaded {len(g)} triples into RDF graph.")
    
    # Example: Print all triples
    print("\n--- All Triples in Graph ---")
    for s, p, o in g:
        print(f"{s} {p} {o}")
    print("----------------------------")

    # Example: Run a simple SPARQL query
    query = """
    SELECT ?cohort ?name ?disease
    WHERE {
        ?cohort a :Cohort ;
                rdfs:label ?name ;
                :hasDisease ?disease .
    }
    """
    print("\n--- SPARQL Query Results ---")
    for row in g.query(query):
        print(f"Cohort: {row.cohort}, Name: {row.name}, Disease: {row.disease}")
    print("----------------------------")

except Exception as e:
    logger.error(f"Error loading or querying TTL graph: {e}")
```

---

## 5. Deploying to GraphDB (Instructions and Example)

Deploying to GraphDB involves running a GraphDB instance and then using its REST API or a client library to upload the TTL file.

**Prerequisites:**
1.  **GraphDB Instance:** Ensure you have a GraphDB instance running (e.g., locally via Docker or a direct installation).
    *   **Docker Example:** `docker run -it -p 7200:7200 --name graphdb-instance ontotext/graphdb:10.3.0`
2.  **Create Repository:** Create a new RDF repository in your GraphDB workbench (e.g., named `my_cohort_repo`).

**Python Code to Upload TTL:**

```python
import requests

# GraphDB connection details
GRAPHDB_URL = "http://localhost:7200" # Adjust if your GraphDB is elsewhere
REPOSITORY_ID = "my_cohort_repo" # The ID of the repository you created

upload_url = f"{GRAPHDB_URL}/repositories/{REPOSITORY_ID}/statements"

headers = {
    "Content-Type": "application/x-turtle"
}

try:
    with open(output_ttl_file, 'rb') as f:
        ttl_data = f.read()

    print(f"Uploading {output_ttl_file} to GraphDB repository: {REPOSITORY_ID}...")
    response = requests.post(upload_url, data=ttl_data, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    print(f"Successfully uploaded data to GraphDB. Status: {response.status_code}")

    # Verify by querying GraphDB (optional, but good for confirmation)
    query_url = f"{GRAPHDB_URL}/repositories/{REPOSITORY_ID}"
    query_headers = {"Accept": "application/sparql-results+json"}
    sparql_query = """
    SELECT (COUNT(?s) as ?count)
    WHERE {
        ?s ?p ?o .
    }
    """
    query_params = {"query": sparql_query}

    query_response = requests.get(query_url, params=query_params, headers=query_headers)
    query_response.raise_for_status()
    
    query_results = query_response.json()
    triple_count = query_results["results"]["bindings"][0]["count"]["value"]
    print(f"Total triples in GraphDB repository '{REPOSITORY_ID}': {triple_count}")

except FileNotFoundError:
    logger.error(f"TTL file not found: {output_ttl_file}. Please ensure it was generated successfully.")
except requests.exceptions.ConnectionError:
    logger.error(f"Could not connect to GraphDB at {GRAPHDB_URL}. Is GraphDB running and accessible?")
except requests.exceptions.RequestException as e:
    logger.error(f"Error during GraphDB upload or query: {e}")
except Exception as e:
    logger.error(f"An unexpected error occurred during GraphDB interaction: {e}")
