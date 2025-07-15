import os
import sys
import logging
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple
import glob
import concurrent.futures

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

class ParserRunner:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(self.script_dir)))
        
        self.unified_parser_script = os.path.join(self.script_dir, 'unified_parser.py')
        self.input_dir = os.path.join(self.project_root, 'example_input/cohortDefinitionOutputs')
        self.output_dir = os.path.join(self.script_dir, 'output/ttl/unified')
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.stats = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'validation_errors': 0
        }

    def validate_ttl_file(self, ttl_file: str) -> int:
        """Validate a TTL file using rapper and return error count."""
        try:
            result = subprocess.run(
                ['rapper', '-i', 'turtle', ttl_file, '-c'],
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                logger.info(f"Rapper validation output for {ttl_file}:\n{result.stdout}")
            if result.stderr:
                logger.error(f"Rapper validation errors for {ttl_file}:\n{result.stderr}")
            
            if result.returncode == 0:
                logger.info(f"TTL file {ttl_file} validated successfully")
                return 0
            else:
                logger.error(f"TTL file {ttl_file} failed validation")
                # A simple way to count errors: count lines in stderr
                return len(result.stderr.splitlines())
                
        except Exception as e:
            logger.error(f"Error running rapper validation on {ttl_file}: {str(e)}")
            return 1 # Count as one error for the file

    def run_parser_for_file(self, json_file_path: str) -> Tuple[bool, int]:
        """Run the unified parser for a single JSON file and validate its output."""
        file_name = os.path.basename(json_file_path)
        output_ttl_file = os.path.join(self.output_dir, os.path.splitext(file_name)[0] + ".ttl")
        validation_errors = 0

        try:
            logger.info(f"Processing {json_file_path}...")
            result = subprocess.run(
                ['python3', self.unified_parser_script, json_file_path, self.output_dir],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.stdout:
                logger.info(f"Parser output for {file_name}:\n{result.stdout}")
            if result.stderr:
                logger.error(f"Parser errors for {file_name}:\n{result.stderr}")
            
            if result.returncode == 0:
                logger.info(f"Successfully parsed {file_name}")
                # Validate the generated TTL file
                validation_errors = self.validate_ttl_file(output_ttl_file)
                return True, validation_errors
            else:
                logger.error(f"Parsing {file_name} failed with return code {result.returncode}")
                return False, 1 # Count as one parsing error
                
        except Exception as e:
            logger.error(f"Error processing {json_file_path}: {str(e)}")
            return False, 1

    def run_all_parsers(self) -> None:
        """Run all parsers in parallel and report performance."""
        logger.info("Starting parser execution sequence...")

        json_files = glob.glob(os.path.join(self.input_dir, '*.json'))
        self.stats['total_files'] = len(json_files)

        if not json_files:
            logger.warning("No JSON files found to process.")
            return

        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_to_file = {executor.submit(self.run_parser_for_file, file_path): file_path for file_path in json_files}
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    success, validation_errors = future.result()
                    if success:
                        self.stats['successful'] += 1
                    else:
                        self.stats['failed'] += 1
                    self.stats['validation_errors'] += validation_errors
                except Exception as exc:
                    logger.error(f'{file_path} generated an exception: {exc}')
                    self.stats['failed'] += 1

        logger.info("\nCombining all generated TTL files...")
        combined_ttl_path = os.path.join(self.project_root, 'output/combined_cohorts.ttl')
        combine_script_path = os.path.join(self.script_dir, 'combine_ttl_files.py')
        
        # Ensure the output directory for combined TTL exists
        os.makedirs(os.path.dirname(combined_ttl_path), exist_ok=True)

        result = subprocess.run(
            ['python3', combine_script_path, self.output_dir, combined_ttl_path],
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        if result.returncode == 0:
            logger.info("All TTL files combined successfully.")
            # Validate the combined ontology
            logger.info("\nValidating combined ontology integrity...")
            validation_script_path = os.path.join(self.project_root, 'scripts/ontology_validation/validate_ontology_integrity.py')
            validation_result = subprocess.run(
                ['python3', validation_script_path, combined_ttl_path],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if validation_result.returncode == 0:
                logger.info("Combined ontology validated successfully.")
            else:
                logger.error(f"Combined ontology integrity validation failed:\n{validation_result.stderr}")
                self.stats['validation_errors'] += len(validation_result.stderr.splitlines())
        else:
            logger.error(f"Failed to combine TTL files:\n{result.stderr}")
            self.stats['failed'] += self.stats['total_files'] # If combining fails, all files effectively failed

        logger.info("\n--- Performance Report ---")
        success_rate = (self.stats['successful'] / self.stats['total_files']) * 100 if self.stats['total_files'] > 0 else 0
        logger.info(f"Overall Success Rate: {success_rate:.2f}%")
        logger.info(f"Total Files Processed: {self.stats['total_files']}")
        logger.info(f"Successfully Parsed: {self.stats['successful']}")
        logger.info(f"Failed to Parse: {self.stats['failed']}")
        logger.info(f"Total Validation Errors: {self.stats['validation_errors']}")

def main():
    runner = ParserRunner()
    runner.run_all_parsers()

if __name__ == "__main__":
    main() 