#!/usr/bin/env python3

import os
import sys
import pytest
from pathlib import Path
import sys
import os
from pathlib import Path

# Add the scripts directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from validate_ontology import OntologyValidator, ValidationResult

@pytest.fixture
def validator():
    """Create a validator instance for testing"""
    ontology_dir = Path(__file__).parent.parent / "ontologies"
    return OntologyValidator(str(ontology_dir))

def test_load_ontology(validator):
    """Test that the ontology loads correctly"""
    assert validator.load_ontology() is True

def test_check_consistency(validator):
    """Test consistency checking"""
    result = validator.check_consistency()
    assert isinstance(result, ValidationResult)
    # The ontology should be consistent
    assert result.is_valid is True
    assert len(result.errors) == 0

def test_check_duplicate_classes(validator):
    """Test duplicate class detection"""
    result = validator.check_duplicate_classes()
    assert isinstance(result, ValidationResult)
    # If duplicates are found, they should be reported
    if not result.is_valid:
        assert len(result.errors) > 0
        assert len(result.suggestions) > 0

def test_check_property_domains(validator):
    """Test property domain checking"""
    result = validator.check_property_domains()
    assert isinstance(result, ValidationResult)
    # Multiple domains should be reported as warnings
    if result.warnings:
        assert len(result.suggestions) > 0

def test_check_imports(validator):
    """Test import checking"""
    result = validator.check_imports()
    assert isinstance(result, ValidationResult)
    # All imports should be valid
    assert result.is_valid is True
    assert len(result.errors) == 0

def test_run_all_checks(validator):
    """Test running all checks together"""
    result = validator.run_all_checks()
    assert isinstance(result, ValidationResult)
    # The combined result should reflect all checks
    if not result.is_valid:
        assert len(result.errors) > 0 or len(result.warnings) > 0 