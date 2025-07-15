import pandas as pd
import rdflib
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import csv
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='phenotype_ingestion.log'
)
logger = logging.getLogger(__name__)

# Define namespaces
DM = Namespace("http://purl.org/dMaster/")
PROV = Namespace("http://www.w3.org/ns/prov#")
SNOMED = Namespace("http://snomed.info/id/")

class PhenotypeIngestionPipeline:
    def __init__(self):
        self.g = Graph()
        self.g.bind("dm", DM)
        self.g.bind("prov", PROV)
        self.g.bind("snomed", SNOMED)
        
    def load_cohort_identification(self, csv_file):
        """Load cohort identification data from CSV."""
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                cohort_uri = DM[f"cohort/{row['cohort_id']}"]
                self.g.add((cohort_uri, RDF.type, DM.Cohort))
                self.g.add((cohort_uri, RDFS.label, Literal(row['cohort_name'])))
                self.g.add((cohort_uri, DM.hasSourceId, Literal(row['source_id'])))
                self.g.add((cohort_uri, DM.hasAtlasLink, Literal(row['atlas_link'])))
                
                # Add provenance
                for s, p, o in self.g.triples((cohort_uri, None, None)):
                    triple = (s, p, o)
                    self.g.add((triple, PROV.wasAttributedTo, DM[row['provenance_agent']]))
                    self.g.add((triple, PROV.wasDerivedFrom, DM[row['provenance_source']]))
                    self.g.add((triple, PROV.generatedAtTime, Literal(row['provenance_timestamp'], datatype=XSD.dateTime)))
            
            logger.info(f"Successfully loaded cohort identification from {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading cohort identification: {str(e)}")
            return False

    def load_clinical_description(self, csv_file):
        """Load clinical description data from CSV."""
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                cohort_uri = DM[f"cohort/{row['cohort_id']}"]
                section_uri = DM[f"clinical_section/{row['cohort_id']}/{row['section']}"]
                
                self.g.add((cohort_uri, DM.hasClinicalSection, section_uri))
                self.g.add((section_uri, RDF.type, DM.ClinicalSection))
                self.g.add((section_uri, RDFS.label, Literal(row['section'])))
                self.g.add((section_uri, DM.hasContent, Literal(row['content'])))
                
                # Add provenance
                for s, p, o in self.g.triples((section_uri, None, None)):
                    triple = (s, p, o)
                    self.g.add((triple, PROV.wasAttributedTo, DM[row['provenance_agent']]))
                    self.g.add((triple, PROV.wasDerivedFrom, DM[row['provenance_source']]))
                    self.g.add((triple, PROV.generatedAtTime, Literal(row['provenance_timestamp'], datatype=XSD.dateTime)))
            
            logger.info(f"Successfully loaded clinical description from {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading clinical description: {str(e)}")
            return False

    def load_evaluation_summary(self, csv_file):
        """Load evaluation summary data from CSV."""
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                cohort_uri = DM[f"cohort/{row['cohort_id']}"]
                section_uri = DM[f"evaluation_section/{row['cohort_id']}/{row['section']}"]
                
                self.g.add((cohort_uri, DM.hasEvaluationSection, section_uri))
                self.g.add((section_uri, RDF.type, DM.EvaluationSection))
                self.g.add((section_uri, RDFS.label, Literal(row['section'])))
                self.g.add((section_uri, DM.hasContent, Literal(row['content'])))
                
                # Add provenance
                for s, p, o in self.g.triples((section_uri, None, None)):
                    triple = (s, p, o)
                    self.g.add((triple, PROV.wasAttributedTo, DM[row['provenance_agent']]))
                    self.g.add((triple, PROV.wasDerivedFrom, DM[row['provenance_source']]))
                    self.g.add((triple, PROV.generatedAtTime, Literal(row['provenance_timestamp'], datatype=XSD.dateTime)))
            
            logger.info(f"Successfully loaded evaluation summary from {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading evaluation summary: {str(e)}")
            return False

    def load_human_readable_algorithm(self, csv_file):
        """Load human readable algorithm data from CSV."""
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                cohort_uri = DM[f"cohort/{row['cohort_id']}"]
                section_uri = DM[f"algorithm_section/{row['cohort_id']}/{row['section']}"]
                
                self.g.add((cohort_uri, DM.hasAlgorithmSection, section_uri))
                self.g.add((section_uri, RDF.type, DM.AlgorithmSection))
                self.g.add((section_uri, RDFS.label, Literal(row['section'])))
                self.g.add((section_uri, DM.hasContent, Literal(row['content'])))
                
                # Add provenance
                for s, p, o in self.g.triples((section_uri, None, None)):
                    triple = (s, p, o)
                    self.g.add((triple, PROV.wasAttributedTo, DM[row['provenance_agent']]))
                    self.g.add((triple, PROV.wasDerivedFrom, DM[row['provenance_source']]))
                    self.g.add((triple, PROV.generatedAtTime, Literal(row['provenance_timestamp'], datatype=XSD.dateTime)))
            
            logger.info(f"Successfully loaded human readable algorithm from {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading human readable algorithm: {str(e)}")
            return False

    def load_concept_sets(self, csv_file):
        """Load concept sets data from CSV."""
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                cohort_uri = DM[f"cohort/{row['cohort_id']}"]
                concept_uri = SNOMED[row['concept_id']]
                
                # Add concept to graph
                self.g.add((concept_uri, RDF.type, DM.Concept))
                self.g.add((concept_uri, RDFS.label, Literal(row['concept_name'])))
                self.g.add((concept_uri, DM.hasVocabulary, Literal(row['vocabulary_id'])))
                
                # Link to cohort
                if row['is_main_concept']:
                    self.g.add((cohort_uri, DM.hasMainConcept, concept_uri))
                else:
                    self.g.add((cohort_uri, DM.hasIncludedConcept, concept_uri))
                
                # Add concept properties
                self.g.add((concept_uri, DM.includeDescendants, Literal(row['include_descendants'], datatype=XSD.boolean)))
                self.g.add((concept_uri, DM.isExcluded, Literal(row['is_excluded'], datatype=XSD.boolean)))
                self.g.add((concept_uri, DM.includeMapped, Literal(row['include_mapped'], datatype=XSD.boolean)))
                
                # Add provenance
                for s, p, o in self.g.triples((concept_uri, None, None)):
                    triple = (s, p, o)
                    self.g.add((triple, PROV.wasAttributedTo, DM[row['provenance_agent']]))
                    self.g.add((triple, PROV.wasDerivedFrom, DM[row['provenance_source']]))
                    self.g.add((triple, PROV.generatedAtTime, Literal(row['provenance_timestamp'], datatype=XSD.dateTime)))
            
            logger.info(f"Successfully loaded concept sets from {csv_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading concept sets: {str(e)}")
            return False
            
    def validate_triples(self):
        """Validate the generated triples against SHACL shapes."""
        # TODO: Implement SHACL validation
        pass
        
    def save_to_ttl(self, output_file):
        """Save the graph to a Turtle file."""
        try:
            self.g.serialize(destination=output_file, format="turtle")
            logger.info(f"Successfully saved triples to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving triples: {str(e)}")
            return False

def main():
    pipeline = PhenotypeIngestionPipeline()
    
    # Load all data
    if (pipeline.load_cohort_identification("cohort_identification.csv") and
        pipeline.load_clinical_description("clinical_description.csv") and
        pipeline.load_evaluation_summary("evaluation_summary.csv") and
        pipeline.load_human_readable_algorithm("human_readable_algorithm.csv") and
        pipeline.load_concept_sets("concept_sets.csv")):
        
        # Validate triples
        pipeline.validate_triples()
        
        # Save to TTL
        pipeline.save_to_ttl("phenotype_cohorts.ttl")
    else:
        logger.error("Failed to process one or more data files")

if __name__ == "__main__":
    main() 