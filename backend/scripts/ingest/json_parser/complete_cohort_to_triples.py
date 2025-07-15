import os
import json
import re
from kazu.pipeline import Pipeline
from pathlib import Path
from typing import List
import hydra
from hydra.utils import instantiate
from kazu.utils.constants import HYDRA_VERSION_BASE
from omegaconf import OmegaConf

# === Config ===
COHORT_DIR = Path("./example_input/cohortDefinitionOutputs")
OUTPUT_DIR = Path("./output_triples")
OUTPUT_DIR.mkdir(exist_ok=True)

# === Helper Functions ===
def clean_text(text: str) -> str:
    text = re.sub(r"\[.*?\]", "", text)  # Remove citations like [1-3]
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_disease_subject(name: str) -> str:
    disease_label = name.replace(" ", "").replace("'", "")
    return f":{disease_label}"

def extract_concepts(subject: str, text: str, kazu_pipeline) -> List[str]:
    doc = kazu_pipeline.process_text(text)
    triples = []
    seen = set()
    for ent in doc.entities:
        if ent.label_ and ent.norm:
            pred = f"disease:{ent.label_.replace(' ', '')}"
            obj = f"disease:{ent.norm.replace(' ', '')}"
            triple = f"{subject} {pred} {obj} ."
            if triple not in seen:
                triples.append(triple)
                seen.add(triple)
    return triples

def extract_metadata_triples(subject: str, cohort_id, name, description) -> List[str]:
    triples = [
        f"{subject} rdf:type :Disease .",
        f"{subject} rdfs:label \"{name}\" .",
        f"{subject} :hasClinicalDescription \"{description}\" ."
    ]
    cohort_uri = f":Cohort{cohort_id}"
    triples.append(f"{cohort_uri} rdf:type :Cohort .")
    triples.append(f"{cohort_uri} rdfs:label \"{name}\" .")
    triples.append(f"{cohort_uri} :describesDisease {subject} .")
    return triples

def save_triples(filename: str, triples: List[str]):
    with open(OUTPUT_DIR / filename, "w", encoding="utf-8") as f:
        f.write("# Disease Definition and Characteristics\n")
        for triple in triples:
            f.write(triple + "\n")

def process_cohort_file(filepath: Path, kazu_pipeline):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    cohort_id = data.get("id", "Unknown")
    name = data.get("name", "")
    clinical_desc = clean_text(data.get("clinical_description", ""))

    subject_uri = extract_disease_subject(name)

    triples = []
    triples.extend(extract_metadata_triples(subject_uri, cohort_id, name, clinical_desc))
    triples.extend(extract_concepts(subject_uri, clinical_desc, kazu_pipeline))

    filename = f"cohort_{cohort_id}.ttl"
    save_triples(filename, triples)

# === Main Execution ===
config_path = Path(__file__).parent / "conf"
config_name = "config"

@hydra.main(version_base=HYDRA_VERSION_BASE, config_path=str(config_path), config_name=config_name)
def main(cfg):
    kazu_pipeline = instantiate(cfg.Pipeline)
    files = [f for f in COHORT_DIR.glob("*.json")]
    for file in files:
        print(f"Processing {file.name}")
        process_cohort_file(file, kazu_pipeline)

if __name__ == "__main__":
    main()
