import os
import pytest
import json
from unified_parser import parse_cohort_json, write_triples_to_file

# Define paths relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
INPUT_DIR = os.path.join(PROJECT_ROOT, 'example_input', 'cohortDefinitionOutputs')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output', 'ttl', 'test_output')

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_output_dir():
    """Create and clean up the output directory for tests."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    yield
    # Clean up generated TTL files after tests
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".ttl") or f.endswith(".json"):
            os.remove(os.path.join(OUTPUT_DIR, f))
    os.rmdir(OUTPUT_DIR)

def test_parse_single_cohort_json():
    """Test parsing a single cohort JSON file and generating TTL."""
    json_file = os.path.join(INPUT_DIR, 'cohort_definition_10616.json')
    output_ttl_file = os.path.join(OUTPUT_DIR, 'cohort_definition_10616.ttl')

    # Ensure the input JSON file exists
    assert os.path.exists(json_file)

    # Parse the JSON and generate triples
    triples = parse_cohort_json(json_file)
    assert triples is not None and len(triples) > 0, "Should generate some triples"

    # Write the triples to a TTL file
    write_triples_to_file(triples, output_ttl_file)
    assert os.path.exists(output_ttl_file), "TTL file should be created"

    # Basic check of TTL content (e.g., check for prefixes and some expected triples)
    with open(output_ttl_file, 'r') as f:
        content = f.read()
        assert "@prefix" in content
        assert ":Cohort10616" in content
        assert ":hasDisease" in content


def test_parse_invalid_json():
    """Test parsing an invalid JSON file."""
    invalid_json_content = "{\"id\": 123, \"name\": \"Test Cohort\", \"clinical_description\": \"\"}" # Missing required fields
    invalid_json_file = os.path.join(OUTPUT_DIR, 'invalid_cohort.json')
    with open(invalid_json_file, 'w') as f:
        f.write(invalid_json_content)

    triples = parse_cohort_json(invalid_json_file)
    assert triples is None or len(triples) == 0, "Should not generate triples for invalid JSON"

