import os
import json

COHORT_DIR = os.path.join(os.path.dirname(__file__), '../../example_input/cohortDefinitionOutputs')
COHORT_DIR = os.path.abspath(COHORT_DIR)

json_files = [f for f in os.listdir(COHORT_DIR) if f.endswith('.json')]

if not json_files:
    print("No JSON files found.")
    exit(1)

for fname in sorted(json_files):
    print(f"\n{'='*60}\nFile: {fname}\n{'='*60}")
    with open(os.path.join(COHORT_DIR, fname), encoding='utf-8') as f:
        data = json.load(f)
        # Print key fields if present
        for key in ["name", "id", "clinical_description", "evaluation_summary", "human_readable_algorithm"]:
            if key in data:
                print(f"\n{key.replace('_', ' ').title()}:")
                print(data[key]) 