#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the root directory of your dMaster project
DMaster_DIR="/Users/nicholasbaro/Python/dMaster"

# Navigate to the dMaster directory
echo "Navigating to ${DMaster_DIR}"
cd "${DMaster_DIR}"

# Define file paths
COMBINED_ONTOLOGY="ontologies/combined_ontology.ttl"
BACKUP_DIR="ontologies/backups"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Timestamp for backup file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/combined_ontology_${TIMESTAMP}.ttl"

# Backup existing combined ontology if it exists
if [ -f "${COMBINED_ONTOLOGY}" ]; then
    echo "Backing up existing ${COMBINED_ONTOLOGY} to ${BACKUP_FILE}"
    mv "${COMBINED_ONTOLOGY}" "${BACKUP_FILE}"
else
    echo "No existing ${COMBINED_ONTOLOGY} found, skipping backup."
fi

# Run the combine_ontologies.py script
echo "Running combine_ontologies.py..."
python3 scripts/combine_ontologies.py
echo "Ontologies combined successfully."

# GraphDB repository URL
GRAPHDB_REPO_URL="http://localhost:7200/repositories/local-test"

# Clear existing data in GraphDB
echo "Clearing GraphDB repository: ${GRAPHDB_REPO_URL}"
curl -X DELETE "${GRAPHDB_REPO_URL}/statements"
echo "GraphDB repository cleared."

# Load the new combined ontology into GraphDB
echo "Loading new combined ontology into GraphDB..."
curl -X POST -H "Content-Type: text/turtle" -T "${COMBINED_ONTOLOGY}" "${GRAPHDB_REPO_URL}/statements"
echo "New combined ontology loaded into GraphDB."

echo "Update process completed." 