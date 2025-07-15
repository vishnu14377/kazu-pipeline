# dMaster

This repository contains a sample Turtle (`.ttl`) file and a pytest-based
unit test that validates the file's syntax using `rdflib`.

## Setup (Recommended: Poetry)

1. Install [Poetry](https://python-poetry.org/docs/#installation) if you haven't already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies (from the project root):

```bash
cd dMaster
poetry install
```

3. Activate the Poetry shell (optional, for interactive work):

```bash
poetry shell
```

## Running the tests

You can run the test suite using Poetry:

```bash
poetry run pytest
```

Or, if you prefer pip:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the tests with `pytest`:

```bash
pytest
```

## What the tests do

- **tests/test_ontology.py**: Checks that the main ontology and all core ontologies can be parsed, that essential classes and properties are present, that the ontology is consistent (using OWLReady2), and that SHACL validation passes.
- **tests/test_ttl_syntax.py**: Checks that all `.ttl` files in the ontologies directory are syntactically valid, not empty, and have required structure (prefixes, class definitions, etc.).

## Project structure

- `ontologies/` — Contains the main ontology and core ontology files.
- `tests/` — Contains all test scripts.
- `pyproject.toml` — Poetry configuration and dependencies.

## How to Run Ontology Tests

### 1. Install Dependencies
Make sure you have all required Python packages installed:

```bash
pip install -r requirements.txt
```

### 2. Run All Ontology Tests
From the `dMaster` directory, run:

```bash
pytest tests/test_ttl_syntax.py -v
```
This will:
- Check the syntax of all `.ttl` files in the `ontologies/` directory and its subdirectories
- Validate the main ontology file
- Check for basic structure in each core ontology

### 3. Test an Individual Ontology File
To test a specific ontology file (for example, only the phenotype ontology):

```bash
pytest tests/test_ttl_syntax.py -v -k phenotype
```
This will only run tests that include `phenotype` in their test ID or file path.

Alternatively, you can directly test a single file using rdflib in Python:

```python
from rdflib import Graph

g = Graph()
g.parse('ontologies/phenotype/phenotype_core.ttl', format='turtle')
print(f"Triples: {len(g)}")
```

## Troubleshooting
- Make sure you are using Python 3.12 (or as specified in `pyproject.toml`).
- If a test fails, check the error message for the file and line number.
- Common issues are missing semicolons, periods, or malformed triples in Turtle files.
- After fixing, re-run the tests to confirm the issue is resolved.
- If you add new `.ttl` files or change ontology structure, re-run the tests to ensure validity.

---

For more advanced validation (e.g., SHACL, logical consistency), see the `tests/` directory or ask for additional test scripts.

For more help, open an issue or contact the maintainer.
