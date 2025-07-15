# Ontology Validation Workflow

This directory contains tools for validating and debugging the modular ontology system. The main script `validate_ontology.py` implements an automated validation pipeline that checks for common issues in modular ontologies.

## Features

The validation workflow includes the following checks:

1. **Consistency Check**
   - Uses HermiT reasoner to verify logical consistency
   - Identifies unsatisfiable classes
   - Reports any contradictions in the ontology

2. **Duplicate Class Detection**
   - Finds classes with identical labels across modules
   - Suggests owl:equivalentClass axioms to unify duplicates
   - Helps maintain a single source of truth for concepts

3. **Property Domain Validation**
   - Checks for properties with multiple domains
   - Identifies potential domain conflicts
   - Suggests domain consolidation strategies

4. **Import Chain Verification**
   - Validates all owl:imports statements
   - Ensures imported ontologies are accessible
   - Maintains proper module dependencies

## Usage

Run the validation script from the command line:

```bash
python validate_ontology.py <ontology_directory>
```

Example:
```bash
python validate_ontology.py ../ontologies
```

The script will output:
- ✅ Success messages for passed checks
- ❌ Error messages for failed checks
- ⚠️ Warnings for potential issues
- 💡 Suggestions for fixing identified problems

## Test Suite

The validation workflow includes a comprehensive test suite in `tests/test_ontology_validation.py`. Run the tests with:

```bash
pytest tests/test_ontology_validation.py -v
```

## Integration with CI/CD

The validation script can be integrated into your CI/CD pipeline to ensure ontology quality. Example GitHub Actions workflow:

```yaml
name: Ontology Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install owlready2 rdflib pytest
      - name: Run validation
        run: python scripts/validate_ontology.py ontologies/
```

## Best Practices

1. **Run Validation Early**
   - Validate changes before committing
   - Catch issues before they propagate
   - Maintain ontology quality

2. **Address Warnings**
   - Review all warnings carefully
   - Fix potential issues proactively
   - Document intentional exceptions

3. **Follow Suggestions**
   - Consider automated fix suggestions
   - Apply fixes in appropriate modules
   - Maintain modular structure

4. **Regular Testing**
   - Run validation in CI/CD
   - Test after major changes
   - Keep test suite updated

## Troubleshooting

Common issues and solutions:

1. **Import Errors**
   - Check file paths in owl:imports
   - Verify ontology URIs
   - Ensure all dependencies are accessible

2. **Consistency Errors**
   - Review class hierarchies
   - Check disjointness axioms
   - Verify property domains/ranges

3. **Duplicate Classes**
   - Use owl:equivalentClass
   - Consolidate definitions
   - Update references

4. **Property Conflicts**
   - Review domain/range definitions
   - Consider property specialization
   - Document usage patterns

## Contributing

To add new validation checks:

1. Add a new method to `OntologyValidator`
2. Implement the check logic
3. Add corresponding test cases
4. Update documentation

## Dependencies

- Python 3.9+
- owlready2
- rdflib
- pytest (for testing)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 