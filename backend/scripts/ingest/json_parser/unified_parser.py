import json
import os
import sys
import re
import logging
import argparse
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import unicodedata
import yaml

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cohort_parser.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CohortParserError(Exception):
    """Base exception for cohort parser errors."""
    pass

class FieldValidationError(CohortParserError):
    """Raised when a required field is missing or invalid."""
    pass

class ConceptSetError(CohortParserError):
    """Raised when there are issues with concept sets."""
    pass

class VocabularyError(CohortParserError):
    """Raised when there are issues with vocabulary mappings."""
    pass

class DateFormatError(CohortParserError):
    """Raised when there are issues with date formats."""
    pass

class TextProcessingError(CohortParserError):
    """Raised when there are issues processing text fields."""
    pass

@dataclass
class ValidationContext:
    """Stores validation context for error reporting."""
    cohort_id: str
    field_name: str
    raw_value: Any
    validation_errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []
        if self.warnings is None:
            self.warnings = []

class RequiredField(Enum):
    """Enum for required fields in cohort definitions."""
    ID = "id"
    NAME = "name"
    CLINICAL_DESCRIPTION = "clinical_description"
    EVALUATION_SUMMARY = "evaluation_summary"
    HUMAN_READABLE_ALGORITHM = "human_readable_algorithm"
    CONCEPT_SETS = "concept_sets"

def validate_required_fields(data: Dict[str, Any], cohort_id: str) -> List[ValidationContext]:
    """
    Validates that all required fields are present and non-empty.
    Returns a list of validation contexts with any errors or warnings.
    """
    validation_results = []
    
    for field in RequiredField:
        context = ValidationContext(
            cohort_id=cohort_id,
            field_name=field.value,
            raw_value=data.get(field.value)
        )
        
        # Check if field exists
        if field.value not in data:
            context.validation_errors.append(f"Required field '{field.value}' is missing")
            validation_results.append(context)
            continue
        
        value = data[field.value]
        
        # Check if field is empty
        if value is None or (isinstance(value, str) and not value.strip()):
            context.validation_errors.append(f"Field '{field.value}' is empty")
            validation_results.append(context)
            continue
        
        # Field-specific validations
        if field == RequiredField.ID:
            if not isinstance(value, (int, str)):
                context.validation_errors.append("ID must be an integer or string")
            elif isinstance(value, str) and not value.isdigit():
                context.validation_errors.append("ID must be numeric")
        
        elif field == RequiredField.NAME:
            if not isinstance(value, str):
                context.validation_errors.append("Name must be a string")
            elif len(value) < 3:
                context.warnings.append("Name is very short")
        
        elif field == RequiredField.CONCEPT_SETS:
            if not isinstance(value, list):
                context.validation_errors.append("Concept sets must be a list")
            elif not value:
                context.warnings.append("Concept sets list is empty")
            else:
                # Validate each concept set
                for i, concept_set in enumerate(value):
                    if not isinstance(concept_set, dict):
                        context.validation_errors.append(f"Concept set {i} is not a dictionary")
                        continue
                    
                    if 'id' not in concept_set:
                        context.validation_errors.append(f"Concept set {i} missing 'id'")
                    if 'name' not in concept_set:
                        context.validation_errors.append(f"Concept set {i} missing 'name'")
                    if 'expression' not in concept_set:
                        context.validation_errors.append(f"Concept set {i} missing 'expression'")
        
        validation_results.append(context)
    
    return validation_results

def validate_concept_set(concept_set: Dict[str, Any], set_index: int) -> List[str]:
    """
    Validates a single concept set structure.
    Returns a list of validation errors.
    """
    errors = []
    
    # Check required fields
    if 'id' not in concept_set:
        errors.append(f"Concept set {set_index} missing 'id'")
    if 'name' not in concept_set:
        errors.append(f"Concept set {set_index} missing 'name'")
    if 'expression' not in concept_set:
        errors.append(f"Concept set {set_index} missing 'expression'")
    
    # Validate expression structure
    if 'expression' in concept_set:
        expression = concept_set['expression']
        if not isinstance(expression, dict):
            errors.append(f"Concept set {set_index} expression is not a dictionary")
        elif 'items' not in expression:
            errors.append(f"Concept set {set_index} expression missing 'items'")
        elif not isinstance(expression['items'], list):
            errors.append(f"Concept set {set_index} expression items is not a list")
    
    # Validate resolved concepts if present
    if 'resolvedConcepts' in concept_set:
        if not isinstance(concept_set['resolvedConcepts'], list):
            errors.append(f"Concept set {set_index} resolvedConcepts is not a list")
    
    return errors

def validate_vocabulary_mapping(vocabulary_id: str) -> Tuple[bool, str]:
    """
    Validates a vocabulary ID and returns (is_valid, prefix).
    """
    vocab_map = {
        'SNOMED': 'snomed:',
        'LOINC': 'loinc:',
        'RxNorm': 'rxnorm:',
        'ICD10': 'icd10:',
        'ICD9CM': 'icd9:',
        'UMLS': 'umls:',
        'MeSH': 'mesh:',
        'DOID': 'doid:',
        'HPO': 'hp:',
        'MONDO': 'mondo:'
    }
    
    if vocabulary_id not in vocab_map:
        return False, f"Unknown vocabulary ID: {vocabulary_id}"
    
    return True, vocab_map[vocabulary_id]

def validate_date_format(date_str: str) -> Tuple[bool, str]:
    """
    Validates a date string format.
    Returns (is_valid, error_message).
    """
    try:
        # Try parsing as ISO format
        datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True, ""
    except ValueError:
        try:
            # Try parsing as Unix timestamp (milliseconds)
            datetime.fromtimestamp(int(date_str) / 1000)
            return True, ""
        except (ValueError, TypeError):
            return False, f"Invalid date format: {date_str}"

def sanitize_text(text: str) -> str:
    """
    Sanitizes text for TTL output.
    Handles special characters, newlines, and Unicode.
    """
    if not isinstance(text, str):
        return str(text)
    
    # Normalize Unicode
    text = unicodedata.normalize('NFKC', text)
    
    # Replace special characters
    text = text.replace('"', '\"')
    text = text.replace('\n', '\n')
    text = text.replace('\r', '\r')
    text = text.replace('\t', '\t')
    
    # Remove control characters
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
    
    return text

def log_validation_results(validation_contexts: List[ValidationContext]):
    """
    Logs validation results with appropriate severity levels.
    """
    for context in validation_contexts:
        if context.validation_errors:
            logger.error(f"Cohort {context.cohort_id} - {context.field_name} validation errors:")
            for error in context.validation_errors:
                logger.error(f"  - {error}")
        
        if context.warnings:
            logger.warning(f"Cohort {context.cohort_id} - {context.field_name} warnings:")
            for warning in context.warnings:
                logger.warning(f"  - {warning}")
        
        if not context.validation_errors and not context.warnings:
            logger.info(f"Cohort {context.cohort_id} - {context.field_name} validation passed")

class PerspectiveError(Exception):
    """Base exception for perspective-related errors."""
    pass

class PerspectiveValidationError(PerspectiveError):
    """Raised when perspective validation fails."""
    pass

class PerspectiveParsingError(PerspectiveError):
    """Raised when perspective parsing fails."""
    pass

@dataclass
class PerspectiveContext:
    """Stores context about the perspective being processed."""
    cohort_id: str
    field_name: str
    raw_value: Any
    parsed_value: Optional[Any] = None
    validation_errors: List[str] = None

    def __post_init__(self):
        if self.validation_errors is None:
            self.validation_errors = []

class PerspectiveField(Enum):
    """Enum for perspective-related fields."""
    CLINICAL_DESCRIPTION = "clinical_description"
    EVALUATION_SUMMARY = "evaluation_summary"
    HUMAN_READABLE_ALGORITHM = "human_readable_algorithm"
    TITLE = "title"

def validate_perspective_field(field: PerspectiveField, value: Any) -> List[str]:
    """
    Validates a perspective field value.
    Returns a list of validation errors, empty if valid.
    """
    errors = []
    
    if not isinstance(value, str):
        errors.append(f"{field.value} must be a string")
        return errors
    
    if not value.strip():
        errors.append(f"{field.value} cannot be empty")
        return errors
    
    # Field-specific validations
    if field == PerspectiveField.CLINICAL_DESCRIPTION:
        if len(value) < 50:
            errors.append("Clinical description should be at least 50 characters")
        if not any(keyword in value.lower() for keyword in ["characterized", "located", "age", "incidence", "prevalence"]):
            errors.append("Clinical description should include key medical characteristics")
    
    elif field == PerspectiveField.EVALUATION_SUMMARY:
        if not any(keyword in value.lower() for keyword in ["developed", "validated", "tested"]):
            errors.append("Evaluation summary should include development and validation details")
    
    elif field == PerspectiveField.HUMAN_READABLE_ALGORITHM:
        if not value.startswith("###"):
            errors.append("Algorithm should start with section headers")
        if not all(section in value for section in ["Cohort Entry", "Cohort Exit", "Cohort Eras"]):
            errors.append("Algorithm should include all required sections")
    
    elif field == PerspectiveField.TITLE:
        if not re.search(r'of\\s+\\w+', value):
            errors.append("Title should include 'of' followed by a condition")
    
    return errors

def get_perspective_context(cohort_id: str, field: PerspectiveField, value: Any) -> PerspectiveContext:
    """
    Creates a perspective context object for a field.
    """
    return PerspectiveContext(
        cohort_id=cohort_id,
        field_name=field.value,
        raw_value=value
    )

def log_perspective_issues(context: PerspectiveContext):
    """
    Logs perspective-related issues.
    """
    if context.validation_errors:
        logger.warning(f"Perspective validation issues in cohort {context.cohort_id}:")
        for error in context.validation_errors:
            logger.warning(f"  - {context.field_name}: {error}")
    else:
        logger.info(f"Perspective validation passed for {context.field_name} in cohort {context.cohort_id}")

# Load core_base.json for ontology-aware validation
try:
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'ontologies/metadata/core_base.json'), 'r') as f:
        CORE_ONTOLOGY = json.load(f)
except FileNotFoundError:
    logger.error("core_base.json not found. Ontology-aware validation will be skipped.")
    CORE_ONTOLOGY = {"classes": [], "semantic_domains": []}
except json.JSONDecodeError:
    logger.error("Error decoding core_base.json. Ontology-aware validation will be skipped.")
    CORE_ONTOLOGY = {"classes": [], "semantic_domains": []}

def _get_class_info(class_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves class information from the loaded ontology."""
    for cls in CORE_ONTOLOGY.get("classes", []):
        if cls["id"] == class_id:
            return cls
    return None

def _is_valid_class(class_id: str) -> bool:
    """Checks if a given class_id exists in the ontology."""
    return _get_class_info(class_id) is not None

def _is_subclass_of(sub_class_id: str, super_class_id: str) -> bool:
    """Checks if sub_class_id is a subclass of super_class_id."""
    if sub_class_id == super_class_id:
        return True
    
    current_class = _get_class_info(sub_class_id)
    if not current_class:
        return False
    
    for parent_id in current_class.get("subClassOf", []):
        if parent_id == super_class_id:
            return True
        # Recursively check superclasses
        if _is_subclass_of(parent_id, super_class_id):
            return True
    return False

# Namespace prefixes
PREFIXES = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix prov: <http://example.org/prov-ontology#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix disease: <http://example.org/ontology/disease#> .

# Biomedical Ontologies
@prefix doid: <http://purl.obolibrary.org/obo/DOID_> .
@prefix hp: <http://purl.obolibrary.org/obo/HP_> .
@prefix mondo: <http://purl.obolibrary.org/obo/MONDO_> .
@prefix snomed: <http://purl.bioontology.org/ontology/SNOMEDCT/> .
@prefix loinc: <http://purl.bioontology.org/ontology/LNC/> .
@prefix rxnorm: <http://purl.bioontology.org/ontology/RXNORM/> .
@prefix icd10: <http://purl.bioontology.org/ontology/ICD10/> .
@prefix icd9: <http://purl.bioontology.org/ontology/ICD9CM/> .
@prefix umls: <http://purl.bioontology.org/ontology/UMLS/> .
@prefix mesh: <http://purl.bioontology.org/ontology/MESH/> .
@prefix chebi: <http://purl.obolibrary.org/obo/CHEBI_> .
@prefix go: <http://purl.obolibrary.org/obo/GO_> .
@prefix obo: <http://purl.obolibrary.org/obo/> .
@prefix oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> .

# OMOP/OHDSI
@prefix omop: <http://purl.org/ohdsi/omop/> .
@prefix ohdsi: <http://purl.org/ohdsi/> .

# Default namespace for our cohort model
@prefix : <http://example.org/cohort/> .

"""

def is_nonempty_literal(val):
    return val is not None and str(val).strip() != ''

def sanitize_local_name(name):
    """Replace illegal Turtle local name characters with underscores."""
    if not isinstance(name, str):
        return name
    # Replace /, \, space, :, and other non-alphanum (except - and _) with _
    return re.sub(r'[^A-Za-z0-9_\-]', '_', name)


# Load extraction rules
with open(os.path.join(os.path.dirname(__file__), 'extraction_rules.yaml'), 'r') as f:
    EXTRACTION_RULES = yaml.safe_load(f)

def get_vocabulary_prefix(vocabulary_id):
    return EXTRACTION_RULES['vocabularies'].get(vocabulary_id, ':')

def parse_clinical_description(description, disease_uri):
    triples = []
    for rule in EXTRACTION_RULES['extraction_patterns']:
        for pattern in rule['patterns']:
            for match in re.finditer(pattern, description, re.IGNORECASE):
                if 'value' in match.groupdict():
                    value = match.group('value').strip()
                    # Ontology-aware validation for extracted values
                    if rule['predicate'] == "disease:hasInflammationCharacteristic" and not _is_valid_class(f"disease:{value.replace(' ', '')}"):
                        logger.warning(f"Invalid class for inflammation characteristic: disease:{value.replace(' ', '')}")
                        continue
                    if rule['predicate'] == "disease:affectsAnatomicalSite" and not _is_valid_class(f"disease:{value.replace(' ', '')}"):
                        logger.warning(f"Invalid class for anatomical site: disease:{value.replace(' ', '')}")
                        continue
                    if rule['predicate'] == "disease:hasPhenotype" and not _is_valid_class(f"disease:{value.replace(' ', '')}"):
                        logger.warning(f"Invalid class for phenotype: disease:{value.replace(' ', '')}")
                        continue
                    if rule['predicate'] == "disease:hasRiskFactor" and not _is_valid_class(f"disease:{value.replace(' ', '')}"):
                        logger.warning(f"Invalid class for risk factor: disease:{value.replace(' ', '')}")
                        continue

                    triples.append(f"{disease_uri} {rule['predicate']} disease:{sanitize_local_name(value)} .")
                else:
                    # Handle patterns that don't have a named group
                    value = match.group(1).strip()
                    triples.append(f"{disease_uri} {rule['predicate']} \"{sanitize_local_name(value)}\"^^xsd:string .")
    return triples


def parse_title(title):
    """
    Extracts disease and temporal constraint from the cohort title.
    Returns (disease, temporal) tuple.
    """
    disease = None
    temporal = None
    
    # Extract disease (after 'of')
    m = re.search(r'of (.+)', title, re.IGNORECASE)
    if m:
        disease = m.group(1).strip()
    
    # Extract temporal (before 'of')
    m2 = re.search(r'(Earliest event|First occurrence|Latest event|Initial diagnosis)', title, re.IGNORECASE)
    if m2:
        temporal = m2.group(1).strip()
    
    return disease, temporal



def parse_evaluation_summary(summary, cohort_uri):
    """
    Parse evaluation summary into RDF triples capturing cohort development and validation details.
    """
    triples = []
    
    # Add the full summary as a property
    triples.append(f"{cohort_uri} :hasEvaluationSummary \"{summary}\" .")
    
    # Create a validation activity
    validation_activity = f":ValidationActivity_{cohort_uri.split(':')[1]}"
    triples.append(f"{validation_activity} rdf:type prov:Activity .")
    triples.append(f"{validation_activity} rdfs:label \"Cohort Validation Activity\" .")
    triples.append(f"{cohort_uri} prov:wasGeneratedBy {validation_activity} .")
    
    # Extract development details
    if "developed" in summary:
        # Extract the type of cohort (prevalent/incident)
        cohort_type_match = re.search(r'(\w+) cohort', summary)
        if cohort_type_match:
            cohort_type = cohort_type_match.group(1)
            triples.append(f"{cohort_uri} :hasCohortType \"{cohort_type}\" .")
            
            # Create development activity
            dev_activity = f":DevelopmentActivity_{cohort_uri.split(':')[1]}"
            triples.append(f"{dev_activity} rdf:type prov:Activity .")
            triples.append(f"{dev_activity} rdfs:label \"Cohort Development Activity\" .")
            triples.append(f"{cohort_uri} prov:wasGeneratedBy {dev_activity} .")
    
    # Extract concept set details
    concept_set_match = re.search(r'concept set of (\d+) concepts', summary)
    if concept_set_match:
        num_concepts = concept_set_match.group(1)
        triples.append(f"{cohort_uri} :hasConceptSetSize \"{num_concepts}\"^^xsd:integer .")
    
    # Extract database coverage
    db_match = re.search(r'from all (\d+) databases', summary)
    if db_match:
        num_dbs = db_match.group(1)
        triples.append(f"{cohort_uri} :hasDatabaseCoverage \"{num_dbs}\"^^xsd:integer .")
        
        # Create database activity
        db_activity = f":DatabaseActivity_{cohort_uri.split(':')[1]}"
        triples.append(f"{db_activity} rdf:type prov:Activity .")
        triples.append(f"{db_activity} rdfs:label \"Database Coverage Activity\" .")
        triples.append(f"{cohort_uri} prov:wasGeneratedBy {db_activity} .")
    
    # Extract time period for validation
    time_period_match = re.search(r'(\d+)-(\d+) day', summary)
    if time_period_match:
        start_days = time_period_match.group(1)
        end_days = time_period_match.group(2)
        triples.append(f"{cohort_uri} :hasValidationTimePeriodStart \"{start_days}\"^^xsd:integer .")
        triples.append(f"{cohort_uri} :hasValidationTimePeriodEnd \"{end_days}\"^^xsd:integer .")
    
    # Extract performance metrics
    if "specificity" in summary.lower() and "sensitivity" in summary.lower():
        triples.append(f"{cohort_uri} :hasPerformanceMetrics :SpecificityAndSensitivity .")
        
        # Create performance evaluation activity
        perf_activity = f":PerformanceActivity_{cohort_uri.split(':')[1]}"
        triples.append(f"{perf_activity} rdf:type prov:Activity .")
        triples.append(f"{perf_activity} rdfs:label \"Performance Evaluation Activity\" .")
        triples.append(f"{cohort_uri} prov:wasGeneratedBy {perf_activity} .")
    
    # Extract validation tool
    if "PheValuator" in summary:
        triples.append(f"{cohort_uri} :validatedBy :PheValuator .")
        
        # Create PheValuator agent
        phevaluator_agent = ":PheValuatorAgent"
        triples.append(f"{phevaluator_agent} rdf:type prov:Agent .")
        triples.append(f"{phevaluator_agent} rdfs:label \"PheValuator Validation Tool\" .")
        triples.append(f"{validation_activity} prov:wasAssociatedWith {phevaluator_agent} .")
    
    return triples

def parse_human_readable_algorithm(algorithm, cohort_uri):
    """
    Parse human readable algorithm into PROV-O activities and relationships.
    """
    triples = []
    
    # Create algorithm development activity
    algo_activity = f":AlgorithmActivity_{cohort_uri.split(':')[1]}"
    triples.append(f"{algo_activity} rdf:type prov:Activity .")
    triples.append(f"{algo_activity} rdfs:label \"Cohort Algorithm Development\" .")
    triples.append(f"{cohort_uri} prov:wasGeneratedBy {algo_activity} .")
    
    # Add the full algorithm text
    triples.append(f"{cohort_uri} :hasAlgorithm \"{algorithm}\" .")
    
    # Parse entry events section
    if "Cohort Entry Events" in algorithm:
        entry_activity = f":EntryEventActivity_{cohort_uri.split(':')[1]}"
        triples.append(f"{entry_activity} rdf:type prov:Activity .")
        triples.append(f"{entry_activity} rdfs:label \"Entry Event Definition\" .")
        triples.append(f"{algo_activity} prov:wasDerivedFrom {entry_activity} .")
        
        # Extract entry conditions
        entry_section = algorithm.split("Cohort Entry Events")[1].split("###")[0]
        conditions = re.findall(r"condition occurrence of '([^']+)'", entry_section)
        for i, condition in enumerate(conditions, 1):
            condition_uri = f":EntryCondition_{cohort_uri.split(':')[1]}_{i}"
            triples.append(f"{condition_uri} rdf:type :EntryCondition .")
            triples.append(f"{condition_uri} rdfs:label \"{condition}\" .")
            triples.append(f"{entry_activity} :definesCondition {condition_uri} .")
        
        # Extract time constraints
        if "first time in the person's history" in entry_section:
            triples.append(f"{entry_activity} :hasTimeConstraint :FirstOccurrence .")
            triples.append(f":FirstOccurrence rdf:type :TimeConstraint .")
            triples.append(f":FirstOccurrence rdfs:label \"First occurrence in history\" .")
        
        # Extract event limiting
        if "earliest event per person" in entry_section:
            triples.append(f"{entry_activity} :hasEventLimit :EarliestEvent .")
            triples.append(f":EarliestEvent rdf:type :EventLimit .")
            triples.append(f":EarliestEvent rdfs:label \"Earliest event per person\" .")
    
    # Parse exit criteria section
    if "Cohort Exit" in algorithm:
        exit_activity = f":ExitCriteriaActivity_{cohort_uri.split(':')[1]}"
        triples.append(f"{exit_activity} rdf:type prov:Activity .")
        triples.append(f"{exit_activity} rdfs:label \"Exit Criteria Definition\" .")
        triples.append(f"{algo_activity} prov:wasDerivedFrom {exit_activity} .")
        
        exit_section = algorithm.split("Cohort Exit")[1].split("###")[0]
        if "end of continuous observation" in exit_section:
            triples.append(f"{exit_activity} :hasExitCriteria :EndOfObservation .")
            triples.append(f":EndOfObservation rdf:type :ExitCriteria .")
            triples.append(f":EndOfObservation rdfs:label \"End of continuous observation\" .")
    
    # Parse cohort eras section
    if "Cohort Eras" in algorithm:
        era_activity = f":EraDefinitionActivity_{cohort_uri.split(':')[1]}"
        triples.append(f"{era_activity} rdf:type prov:Activity .")
        triples.append(f"{era_activity} rdfs:label \"Cohort Era Definition\" .")
        triples.append(f"{algo_activity} prov:wasDerivedFrom {era_activity} .")
        
        era_section = algorithm.split("Cohort Eras")[1]
        if "within" in era_section and "days of each other" in era_section:
            days_match = re.search(r"within (\d+) days", era_section)
            if days_match:
                days = days_match.group(1)
                triples.append(f"{era_activity} :hasEraWindow \"{days}\"^^xsd:integer .")
                triples.append(f"{era_activity} :hasEraWindowUnit \"days\" .")
    
    return triples

def parse_concept_sets(concept_sets, cohort_uri):
    """
    Parse concept sets into PROV-O activities and relationships.
    """
    triples = []
    
    # Create concept set development activity
    concept_activity = f":ConceptSetActivity_{cohort_uri.split(':')[1]}"
    triples.append(f"{concept_activity} rdf:type prov:Activity .")
    triples.append(f"{concept_activity} rdfs:label \"Concept Set Development\" .")
    triples.append(f"{cohort_uri} prov:wasGeneratedBy {concept_activity} .")
    
    # Create literature review activity
    lit_activity = f":LiteratureReviewActivity_{cohort_uri.split(':')[1]}"
    triples.append(f"{lit_activity} rdf:type prov:Activity .")
    triples.append(f"{lit_activity} rdfs:label \"Literature Review\" .")
    triples.append(f"{concept_activity} prov:wasDerivedFrom {lit_activity} .")
    
    # Create PHOEBE analysis activity
    phoebe_activity = f":PHOEBEAnalysisActivity_{cohort_uri.split(':')[1]}"
    triples.append(f"{phoebe_activity} rdf:type prov:Activity .")
    triples.append(f"{phoebe_activity} rdfs:label \"PHOEBE Analysis\" .")
    triples.append(f"{concept_activity} prov:wasDerivedFrom {phoebe_activity} .")
    
    # Create orphan concept analysis activity
    orphan_activity = f":OrphanConceptActivity_{cohort_uri.split(':')[1]}"
    triples.append(f"{orphan_activity} rdf:type prov:Activity .")
    triples.append(f"{orphan_activity} rdfs:label \"Orphan Concept Analysis\" .")
    triples.append(f"{concept_activity} prov:wasDerivedFrom {orphan_activity} .")
    
    # Process each concept set
    for concept_set in concept_sets:
        set_id = concept_set.get('id', '')
        set_name = concept_set.get('name', '')
        
        # Create concept set entity
        set_uri = f":ConceptSet_{sanitize_local_name(set_id)}"
        triples.append(f"{set_uri} rdf:type :ConceptSet .")
        if is_nonempty_literal(set_name):
            triples.append(f"{set_uri} rdfs:label \"{sanitize_local_name(set_name)}\" .")
        triples.append(f"{cohort_uri} :hasConceptSet {set_uri} .")
        
        # Link concept set to its development activity
        set_dev_activity = f":ConceptSetDevActivity_{sanitize_local_name(set_id)}"
        triples.append(f"{set_dev_activity} rdf:type prov:Activity .")
        triples.append(f"{set_dev_activity} rdfs:label \"Concept Set {sanitize_local_name(set_id)} Development\" .")
        triples.append(f"{set_uri} prov:wasGeneratedBy {set_dev_activity} .")
        triples.append(f"{concept_activity} prov:wasDerivedFrom {set_dev_activity} .")
        
        # Process concepts in the set
        for item in concept_set.get('expression', {}).get('items', []):
            concept = item.get('concept', {})
            concept_id = concept.get('CONCEPT_ID', '')
            concept_name = concept.get('CONCEPT_NAME', '')
            concept_code = concept.get('CONCEPT_CODE', '')
            domain_id = concept.get('DOMAIN_ID', '')
            vocabulary_id = concept.get('VOCABULARY_ID', '')
            concept_class = concept.get('CONCEPT_CLASS_ID', '')
            is_excluded = item.get('isExcluded', False)
            include_descendants = item.get('includeDescendants', False)
            include_mapped = item.get('includeMapped', False)
            
            # Get the appropriate vocabulary prefix
            vocab_prefix = get_vocabulary_prefix(vocabulary_id)
            
            # Create concept URI
            concept_uri = f"{vocab_prefix}{sanitize_local_name(concept_code)}"
            
            # Add concept triples
            triples.append(f"{concept_uri} rdf:type :Concept .")
            if is_nonempty_literal(concept_name):
                triples.append(f"{concept_uri} rdfs:label \"{sanitize_local_name(concept_name)}\" .")
            triples.append(f"{concept_uri} :hasConceptCode \"{sanitize_local_name(concept_code)}\" .")
            triples.append(f"{concept_uri} :hasDomain \"{sanitize_local_name(domain_id)}\" .")
            triples.append(f"{concept_uri} :hasVocabulary \"{sanitize_local_name(vocabulary_id)}\" .")
            triples.append(f"{concept_uri} :hasConceptClass \"{sanitize_local_name(concept_class)}\" .")
            
            # Create concept inclusion rule
            rule_uri = f":ConceptRule_{sanitize_local_name(set_id)}_{sanitize_local_name(concept_id)}"
            triples.append(f"{rule_uri} rdf:type :ConceptInclusionRule .")
            triples.append(f"{set_uri} :hasInclusionRule {rule_uri} .")
            triples.append(f"{rule_uri} :appliesToConcept {concept_uri} .")
            
            # Add rule properties
            triples.append(f"{rule_uri} :isExcluded \"{str(is_excluded).lower()}\"^^xsd:boolean .")
            triples.append(f"{rule_uri} :includeDescendants \"{str(include_descendants).lower()}\"^^xsd:boolean .")
            triples.append(f"{rule_uri} :includeMapped \"{str(include_mapped).lower()}\"^^xsd:boolean .")
            
            # Add rule descriptions
            if is_excluded:
                triples.append(f"{rule_uri} rdfs:comment \"Excludes concept and its descendants from the cohort\" .")
            else:
                triples.append(f"{rule_uri} rdfs:comment \"Includes concept in the cohort\" .")
            
            if include_descendants:
                triples.append(f"{rule_uri} rdfs:comment \"Includes all descendant concepts in the hierarchy\" .")
            
            if include_mapped:
                triples.append(f"{rule_uri} rdfs:comment \"Includes mapped concepts from other vocabularies\" .")
            
            # Add skos:exactMatch to the concept in its native vocabulary
            if vocab_prefix != ':':
                triples.append(f"{concept_uri} skos:exactMatch {vocab_prefix}{sanitize_local_name(concept_code)} .")
        
        # Process resolved concepts (descendants)
        for resolved in concept_set.get('resolvedConcepts', []):
            concept_id = resolved.get('conceptId', '')
            concept_name = resolved.get('conceptName', '')
            concept_code = resolved.get('conceptCode', '')
            domain_id = resolved.get('domainId', '')
            vocabulary_id = resolved.get('vocabularyId', '')
            concept_class = resolved.get('conceptClassId', '')
            valid_start = resolved.get('validStartDate', '')
            valid_end = resolved.get('validEndDate', '')
            
            # Get the appropriate vocabulary prefix
            vocab_prefix = get_vocabulary_prefix(vocabulary_id)
            
            # Create concept URI
            concept_uri = f"{vocab_prefix}{sanitize_local_name(concept_code)}"
            
            # Add concept triples
            triples.append(f"{concept_uri} rdf:type :Concept .")
            if is_nonempty_literal(concept_name):
                triples.append(f"{concept_uri} rdfs:label \"{sanitize_local_name(concept_name)}\" .")
            triples.append(f"{concept_uri} :hasConceptCode \"{sanitize_local_name(concept_code)}\" .")
            triples.append(f"{concept_uri} :hasDomain \"{sanitize_local_name(domain_id)}\" .")
            triples.append(f"{concept_uri} :hasVocabulary \"{sanitize_local_name(vocabulary_id)}\" .")
            triples.append(f"{concept_uri} :hasConceptClass \"{sanitize_local_name(concept_class)}\" .")
            
            # Add validity period
            if valid_start:
                triples.append(f"{concept_uri} :validFrom \"{valid_start}\"^^xsd:dateTime .")
            if valid_end:
                triples.append(f"{concept_uri} :validTo \"{valid_end}\"^^xsd:dateTime .")
            
            # Link to concept set as resolved concept
            triples.append(f"{set_uri} :hasResolvedConcept {concept_uri} .")
            
            # Add skos:exactMatch to the concept in its native vocabulary
            if vocab_prefix != ':':
                triples.append(f"{concept_uri} skos:exactMatch {vocab_prefix}{sanitize_local_name(concept_code)} .")
    
    return triples

def escape_literal(s):
    """Escape newlines and carriage returns in a string literal for TTL output."""
    if not isinstance(s, str):
        return s
    return s.replace('"', '\"').replace('\n', '\n').replace('\r', '\r')

def write_triples_to_file(triples, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(PREFIXES)
        for triple in triples:
            # Escape all literals in the triple
            # If the triple contains a quoted string, escape it
            if '"' in triple:
                parts = triple.split('"')
                for i in range(1, len(parts), 2):
                    parts[i] = escape_literal(parts[i])
                triple = '"'.join(parts)
            f.write(triple + '\n')

def parse_cohort_json(file_path):
    """Parse a cohort definition JSON file and extract triples."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON file {file_path}: {str(e)}")
        raise CohortParserError(f"Invalid JSON format in {file_path}") from e
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {str(e)}")
        raise CohortParserError(f"File encoding error in {file_path}") from e
    except Exception as e:
        logger.error(f"Unexpected error reading file {file_path}: {str(e)}")
        raise CohortParserError(f"Error reading file {file_path}") from e
    
    # Get cohort ID for validation context
    cohort_id = str(data.get('id', 'Unknown'))
    
    # Validate required fields
    validation_results = validate_required_fields(data, cohort_id)
    log_validation_results(validation_results)
    
    # Check for critical validation errors
    has_critical_errors = any(
        context.validation_errors 
        for context in validation_results 
        if context.field_name in [RequiredField.ID.value, RequiredField.NAME.value]
    )
    if has_critical_errors:
        raise FieldValidationError(f"Critical validation errors in cohort {cohort_id}")
    
    # Extract fields with validation
    cohort_name = data.get('name', '')
    clinical_desc = data.get('clinical_description', '')
    edit_url = data.get('edit_url', '')
    evaluation_summary = data.get('evaluation_summary', '')
    human_readable_algorithm = data.get('human_readable_algorithm', '')
    concept_sets = data.get('concept_sets', [])
    
    # Define the cohort URI
    cohort_uri = f":Cohort{cohort_id}"
    
    # Output triples
    triples = []
    
    try:
        # Basic cohort information
        triples.append(f"{cohort_uri} rdf:type :Cohort .")
        if is_nonempty_literal(cohort_name):
            triples.append(f"{cohort_uri} rdfs:label \"{sanitize_text(cohort_name)}\" .")
        
        # Add ID as a data property
        if cohort_id != 'Unknown':
            triples.append(f"{cohort_uri} dct:identifier \"{cohort_id}\"^^xsd:integer .")
        
        # Add edit URL as source
        if edit_url:
            triples.append(f"{cohort_uri} dct:source <{edit_url}> .")
            
            # Create Atlas agent
            atlas_agent = ":AtlasAgent"
            triples.append(f"{atlas_agent} rdf:type prov:Agent .")
            triples.append(f"{atlas_agent} rdfs:label \"OHDSI Atlas\" .")
            
            # Create Atlas activity
            atlas_activity = f":AtlasActivity_{cohort_id}"
            triples.append(f"{atlas_activity} rdf:type prov:Activity .")
            triples.append(f"{atlas_activity} rdfs:label \"Atlas Cohort Definition Activity\" .")
            triples.append(f"{cohort_uri} prov:wasGeneratedBy {atlas_activity} .")
            triples.append(f"{atlas_activity} prov:wasAssociatedWith {atlas_agent} .")
        
        # Parse evaluation summary
        if evaluation_summary:
            try:
                eval_triples = parse_evaluation_summary(evaluation_summary, cohort_uri)
                triples.extend(eval_triples)
            except Exception as e:
                logger.error(f"Error parsing evaluation summary for cohort {cohort_id}: {str(e)}")
                raise TextProcessingError(f"Failed to parse evaluation summary in cohort {cohort_id}") from e
        
        # Parse human readable algorithm
        if human_readable_algorithm:
            try:
                algo_triples = parse_human_readable_algorithm(human_readable_algorithm, cohort_uri)
                triples.extend(algo_triples)
            except Exception as e:
                logger.error(f"Error parsing human readable algorithm for cohort {cohort_id}: {str(e)}")
                raise TextProcessingError(f"Failed to parse human readable algorithm in cohort {cohort_id}") from e
        
        # Parse concept sets
        if concept_sets:
            try:
                concept_triples = parse_concept_sets(concept_sets, cohort_uri)
                triples.extend(concept_triples)
            except Exception as e:
                logger.error(f"Error parsing concept sets for cohort {cohort_id}: {str(e)}")
                raise ConceptSetError(f"Failed to parse concept sets in cohort {cohort_id}") from e
        
        # Parse title into components
        try:
            disease, temporal = parse_title(cohort_name)
            
            # Add disease entity if found
            if disease:
                disease_uri = f":Disease_{sanitize_local_name(disease.replace(' ', '_'))}"
                triples.append(f"{disease_uri} rdf:type :Disease .")
                if is_nonempty_literal(disease):
                    triples.append(f"{disease_uri} rdfs:label \"{sanitize_text(disease)}\" .")
                triples.append(f"{cohort_uri} :hasDisease {disease_uri} .")
                
                # Parse clinical description into detailed triples
                if clinical_desc:
                    try:
                        clinical_triples = parse_clinical_description(clinical_desc, disease_uri)
                        triples.extend(clinical_triples)
                    except Exception as e:
                        logger.error(f"Error parsing clinical description for cohort {cohort_id}: {str(e)}")
                        raise TextProcessingError(f"Failed to parse clinical description in cohort {cohort_id}") from e
            
            # Add temporal constraint if found
            if temporal:
                temporal_uri = f":Temporal_{sanitize_local_name(temporal.replace(' ', '_'))}"
                triples.append(f"{temporal_uri} rdf:type time:TemporalEntity .")
                if is_nonempty_literal(temporal):
                    triples.append(f"{temporal_uri} rdfs:label \"{sanitize_text(temporal)}\" .")
                triples.append(f"{cohort_uri} :hasTemporalConstraint {temporal_uri} .")
        except Exception as e:
            logger.error(f"Error parsing title components for cohort {cohort_id}: {str(e)}")
            raise TextProcessingError(f"Failed to parse title components in cohort {cohort_id}") from e
        
        return triples
        
    except Exception as e:
        logger.error(f"Error processing cohort {cohort_id}: {str(e)}")
        raise CohortParserError(f"Failed to process cohort {cohort_id}") from e


def main():
    """Main function to parse a single cohort JSON file to TTL."""
    parser = argparse.ArgumentParser(description="Parse a single cohort definition JSON file to TTL.")
    parser.add_argument("input_file", help="Path to the input cohort definition JSON file.")
    parser.add_argument("output_dir", help="Directory to write the TTL file to.")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)

    if not os.path.isdir(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    logger.info(f"Parsing {args.input_file}...")
    try:
        triples = parse_cohort_json(args.input_file)
        if triples:
            output_filename = os.path.splitext(os.path.basename(args.input_file))[0] + ".ttl"
            output_file_path = os.path.join(args.output_dir, output_filename)
            write_triples_to_file(triples, output_file_path)
            logger.info(f"Successfully wrote triples to {output_file_path}")
        else:
            logger.warning(f"No triples generated for {args.input_file}.")
    except CohortParserError as e:
        logger.error(f"Could not parse {args.input_file}: {e}")


if __name__ == "__main__":
    main()