import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BIOPORTAL_API_KEY = os.getenv("BIOPORTAL_API_KEY")

# Get the absolute path to the project root (2 levels up from this script)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
ONTOLOGY_DIR = PROJECT_ROOT / 'data' / 'ontologies'
ONTOLOGY_DIR.mkdir(parents=True, exist_ok=True)

ONTOLOGIES = [
    ("bao.owl", "https://raw.githubusercontent.com/BioAssayOntology/BAO/master/bao_complete.owl"),
    ("cso.owl", f"https://data.bioontology.org/ontologies/CSO/submissions/1/download?apikey={BIOPORTAL_API_KEY}" if BIOPORTAL_API_KEY else None),
    ("dct.owl", "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dcterms.rdf"),
    ("dc.owl", "https://www.dublincore.org/specifications/dublin-core/dces/2008-01-14/dc.rdf"),
    ("efo.owl", "https://www.ebi.ac.uk/efo/efo.owl"),
    ("doid.owl", "http://purl.obolibrary.org/obo/doid.owl"),
    ("hp.owl", "http://purl.obolibrary.org/obo/hp.owl"),
    # LOINC: No public OWL, must download manually from https://loinc.org/downloads/loinc-table/
    ("mondo.owl", "http://purl.obolibrary.org/obo/mondo.owl"),
    ("obi.owl", "http://purl.obolibrary.org/obo/obi.owl"),
    ("obcs.owl", "http://purl.obolibrary.org/obo/obcs.owl"),
    ("time.owl", "http://www.w3.org/2006/time#"),
    ("provo.owl", "http://www.w3.org/ns/prov-o.owl"),
    ("snomedct_us.owl", "https://download.nlm.nih.gov/umls/kss/2023AB/SNOMEDCT_US/SnomedCT_InternationalEdition.owl"),
    ("rxnorm.owl", "https://download.nlm.nih.gov/umls/kss/2023AB/RXNORM/RxNorm_full.owl"),
    ("sepio.owl", "http://purl.obolibrary.org/obo/sepio.owl"),
    ("snomedct.owl", "https://download.nlm.nih.gov/umls/kss/2023AB/SNOMEDCT/SnomedCT_InternationalEdition.owl"),
    ("rdfs.owl", "http://www.w3.org/2000/01/rdf-schema#"),
]

def download(url, dest):
    print(f"Downloading {url} -> {dest}")
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        print(f"Downloaded {dest}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

for fname, url in ONTOLOGIES:
    if url is None:
        print(f"Skipping {fname}: No URL or missing API key.")
        continue
    if "loinc" in fname:
        print(f"Skipping {fname}: LOINC OWL not publicly available. Download manually from https://loinc.org/downloads/loinc-table/")
        continue
    dest = ONTOLOGY_DIR / fname
    if dest.exists():
        print(f"{dest} already exists, skipping.")
        continue
    download(url, dest) 