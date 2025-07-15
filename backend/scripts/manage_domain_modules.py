#!/usr/bin/env python3

import os
from pathlib import Path
import json
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DomainModuleManager:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.ontology_dir = self.base_dir / "ontologies"
        self.domains = ['diagnosis', 'phenotype', 'pathogenesis', 'population']
        self.module_config = self._load_module_config()

    def _load_module_config(self) -> Dict:
        """Load module configuration from JSON file."""
        config_file = self.base_dir / "config" / "module_config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading module config: {e}")
                return {}
        return {}

    def _save_module_config(self):
        """Save module configuration to JSON file."""
        config_file = self.base_dir / "config" / "module_config.json"
        config_file.parent.mkdir(exist_ok=True)
        try:
            with open(config_file, 'w') as f:
                json.dump(self.module_config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving module config: {e}")

    def get_module_dependencies(self, domain: str) -> List[str]:
        """Get dependencies for a specific domain module."""
        return self.module_config.get(domain, {}).get('dependencies', [])

    def get_module_instructions(self, domain: str) -> Optional[str]:
        """Get instructions for a specific domain module."""
        instructions_file = self.ontology_dir / domain / f"{domain}_instructions.txt"
        if instructions_file.exists():
            try:
                with open(instructions_file, 'r') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading instructions for {domain}: {e}")
        return None

    def update_module_instructions(self, domain: str, instructions: str):
        """Update instructions for a specific domain module."""
        instructions_file = self.ontology_dir / domain / f"{domain}_instructions.txt"
        try:
            instructions_file.parent.mkdir(exist_ok=True)
            with open(instructions_file, 'w') as f:
                f.write(instructions)
            logger.info(f"Updated instructions for {domain}")
        except Exception as e:
            logger.error(f"Error updating instructions for {domain}: {e}")

    def add_module_dependency(self, domain: str, dependency: str):
        """Add a dependency to a domain module."""
        if domain not in self.module_config:
            self.module_config[domain] = {'dependencies': []}
        
        if dependency not in self.module_config[domain]['dependencies']:
            self.module_config[domain]['dependencies'].append(dependency)
            self._save_module_config()
            logger.info(f"Added dependency {dependency} to {domain}")

    def remove_module_dependency(self, domain: str, dependency: str):
        """Remove a dependency from a domain module."""
        if domain in self.module_config and dependency in self.module_config[domain]['dependencies']:
            self.module_config[domain]['dependencies'].remove(dependency)
            self._save_module_config()
            logger.info(f"Removed dependency {dependency} from {domain}")

    def validate_module_structure(self, domain: str) -> bool:
        """Validate the structure of a domain module."""
        domain_dir = self.ontology_dir / domain
        if not domain_dir.exists():
            logger.error(f"Domain directory not found: {domain}")
            return False

        required_files = [
            f"{domain}_core.ttl",
            f"{domain}_instructions.txt"
        ]

        for file in required_files:
            if not (domain_dir / file).exists():
                logger.error(f"Required file not found: {file}")
                return False

        return True

    def get_module_status(self, domain: str) -> Dict:
        """Get the current status of a domain module."""
        status = {
            'exists': self.validate_module_structure(domain),
            'dependencies': self.get_module_dependencies(domain),
            'has_instructions': bool(self.get_module_instructions(domain))
        }
        return status

    def list_all_modules(self) -> Dict[str, Dict]:
        """List all domain modules and their status."""
        return {domain: self.get_module_status(domain) for domain in self.domains}

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Create and run the manager
    manager = DomainModuleManager(str(project_root))
    
    # Example usage
    for domain in manager.domains:
        status = manager.get_module_status(domain)
        logger.info(f"Module {domain}: {status}")

if __name__ == "__main__":
    main() 