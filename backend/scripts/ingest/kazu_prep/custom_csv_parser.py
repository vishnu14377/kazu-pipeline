import csv
from typing import List, Dict, Optional

class CustomSynonym:
    def __init__(self, text, mention_confidence=1.0, case_sensitive=False):
        self.text = text
        self.mention_confidence = mention_confidence
        self.case_sensitive = case_sensitive

class CustomDictionaryResource:
    def __init__(self, entity_id, label, synonyms, metadata=None):
        self.entity_id = entity_id
        self.label = label
        self.synonyms = synonyms
        self.metadata = metadata or {}

    def syn_norm_for_linking(self, entity_class=None):
        # Return the normalized label as a string (not a list)
        return self.label.lower()

    def active_ner_synonyms(self):
        """
        Returns all synonyms and the label, lowercased, as CustomSynonym objects for NER string matching.
        """
        return [CustomSynonym(self.label.lower())] + [CustomSynonym(s.lower()) for s in self.synonyms if s]

class CustomCSVParser:
    """
    Custom parser for Kazu that reads dictionary CSV files and yields entity records.
    Each CSV should have columns: entity_id, label, synonyms (pipe-separated).
    Implements the populate_databases method required by Kazu's parser interface.
    """

    def __init__(self, csv_paths: Optional[List[str]] = None, entity_class: str = "Entity", name: str = "CustomCSVParser"):
        """
        :param csv_paths: List of CSV file paths to parse.
        :param entity_class: The type of entity being parsed (e.g., 'Disease', 'Phenotype').
        """
        self.csv_paths = csv_paths or []
        self.entities = []
        self.entity_class = entity_class
        self.name = name

    def parse(self) -> List[CustomDictionaryResource]:
        """
        Parses all CSV files and returns a list of CustomDictionaryResource objects.
        """
        entities = []
        for path in self.csv_paths:
            try:
                with open(path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        entity = CustomDictionaryResource(
                            row.get("entity_id", ""),
                            row.get("label", ""),
                            row.get("synonyms", "").split("|") if row.get("synonyms") else [],
                            metadata={k: v for k, v in row.items() if k not in ["entity_id", "label", "synonyms"]}
                        )
                        entities.append(entity)
            except Exception as e:
                print(f"Error reading {path}: {e}")
        return entities

    def populate_databases(self, force=False, return_resources=False):
        """
        Loads the CSVs and prepares the entities list for Kazu string matching.
        This method is required by the Kazu parser interface.
        If return_resources is True, returns the loaded entities.
        """
        self.entities = self.parse()
        if return_resources:
            return self.entities 