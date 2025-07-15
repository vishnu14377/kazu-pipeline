import os

# Directory containing the cohort definition outputs
COHORT_DIR = os.path.join(os.path.dirname(__file__), '../../example_input/cohortDefinitionOutputs')
COHORT_DIR = os.path.abspath(COHORT_DIR)

print(f"Looking for JSON files in: {COHORT_DIR}")

# List all JSON files in the directory
json_files = [f for f in os.listdir(COHORT_DIR) if f.endswith('.json')]

if not json_files:
    print("No JSON files found.")
else:
    print("Found JSON files:")
    for fname in json_files:
        print(f" - {fname}") 