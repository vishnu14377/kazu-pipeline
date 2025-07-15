import json
import os
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import unicodedata
import re

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cohort_parser_unified.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationContext:
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
    ID = "id"
    NAME = "name"
    CLINICAL_DESCRIPTION = "clinical_description"
    EVALUATION_SUMMARY = "evaluation_summary"
    HUMAN_READABLE_ALGORITHM = "human_readable_algorithm"
    CONCEPT_SETS = "concept_sets"

class OutputMode(Enum):
    RAW = "raw"
    STRUCTURED = "structured"
    TTL = "ttl"

class UnifiedCohortParser:
    def __init__(self, output_dir: str = "output/ttl", mode: OutputMode = OutputMode.TTL):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.mode = mode

        self.prefixes = {
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'owl': 'http://www.w3.org/2002/07/owl#',
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'dct': 'http://purl.org/dc/terms/',
            'prov': 'http://www.w3.org/ns/prov#',
            'time': 'http://www.w3.org/2006/time#',
            'disease': 'http://example.org/ontology/disease#',
            'snomed': 'http://purl.bioontology.org/ontology/SNOMEDCT/',
            'json': 'http://example.org/json/'
        }

        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'warnings': 0
        }

    def validate_cohort_data(self, data: Dict[str, Any], cohort_id: str) -> List[ValidationContext]:
        validation_results = []
        for field in RequiredField:
            context = ValidationContext(
                cohort_id=cohort_id,
                field_name=field.value,
                raw_value=data.get(field.value)
            )
            if field.value not in data:
                context.validation_errors.append(f"Required field '{field.value}' is missing")
                validation_results.append(context)
                continue
            value = data[field.value]
            if value is None or (isinstance(value, str) and not value.strip()):
                context.validation_errors.append(f"Field '{field.value}' is empty")
                validation_results.append(context)
                continue
            validation_results.append(context)
        return validation_results

    def log_validation_results(self, validation_contexts: List[ValidationContext]):
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

    def generate_raw_output(self, data: Dict[str, Any], cohort_id: str) -> str:
        return json.dumps(data, indent=2)

    def generate_structured_output(self, data: Dict[str, Any], cohort_id: str) -> str:
        ttl_lines = []
        for prefix, uri in self.prefixes.items():
            ttl_lines.append(f"@prefix {prefix}: <{uri}> .")
        ttl_lines.append("")
        ttl_lines.extend([
            f":Cohort{cohort_id} rdf:type :Cohort .",
        ])
        for key, value in data.items():
            field_uri = f":Field_{cohort_id}_{key}"
            ttl_lines.extend([
                f":Cohort{cohort_id} json:hasField {field_uri} .",
                f"{field_uri} rdf:type json:Field .",
                f"{field_uri} json:fieldName \"{key}\" .",
                f"{field_uri} json:fieldValue \"{str(value).replace('\"', '\\\"')}\" .",
                f"{field_uri} json:sourceDocument \"{data.get('edit_url', '')}\" .",
                ""
            ])
        return "\n".join(ttl_lines)

    def generate_ttl_output(self, data: Dict[str, Any], cohort_id: str) -> str:
        # For brevity, reuse parse_cohort_json_to_triples.py logic or simplified version here
        # This example will just call generate_structured_output for demonstration
        return self.generate_structured_output(data, cohort_id)

    def parse_json_file(self, file_path: str) -> bool:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            cohort_id = str(data.get('id', 'Unknown'))
            validation_results = self.validate_cohort_data(data, cohort_id)
            self.log_validation_results(validation_results)
            if any(context.validation_errors for context in validation_results):
                self.stats['failed'] += 1
                return False
            if self.mode == OutputMode.RAW:
                output_content = self.generate_raw_output(data, cohort_id)
                ext = "json"
            elif self.mode == OutputMode.STRUCTURED:
                output_content = self.generate_structured_output(data, cohort_id)
                ext = "ttl"
            else:
                output_content = self.generate_ttl_output(data, cohort_id)
                ext = "ttl"
            output_file = os.path.join(self.output_dir, f"cohort_definition_{cohort_id}.{ext}")
            with open(output_file, 'w') as f:
                f.write(output_content)
            logger.info(f"Successfully processed {file_path} -> {output_file}")
            self.stats['successful'] += 1
            return True
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            self.stats['failed'] += 1
            return False

    def parse_json_files(self, file_paths: List[str]) -> None:
        self.stats['total_files'] = len(file_paths)
        for file_path in file_paths:
            logger.info(f"\nProcessing {file_path}...")
            self.parse_json_file(file_path)
        logger.info("\nProcessing Summary:")
        logger.info(f"Total files processed: {self.stats['total_files']}")
        logger.info(f"Successfully processed: {self.stats['successful']}")
        logger.info(f"Failed to process: {self.stats['failed']}")
        logger.info(f"Validation warnings: {self.stats['warnings']}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Unified Cohort JSON Parser")
    parser.add_argument("--mode", choices=["raw", "structured", "ttl"], default="ttl", help="Output mode")
    args = parser.parse_args()
    mode = OutputMode(args.mode)
    parser = UnifiedCohortParser(mode=mode)
    input_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 
                             'example_input/cohortDefinitionOutputs')
    json_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.json')]
    parser.parse_json_files(json_files)

if __name__ == "__main__":
    main()
