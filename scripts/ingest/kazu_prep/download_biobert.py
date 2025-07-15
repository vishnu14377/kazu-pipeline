import os
from pathlib import Path
from transformers import AutoModel, AutoTokenizer

# Get the absolute path to the project root (2 levels up from this script)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data' / 'huggingface_models'

MODELS = {
    'biobert': 'dmis-lab/biobert-base-cased-v1.1',
    'bigbird': 'google/bigbird-roberta-base'
}

def download_model(model_name, model_id):
    print(f"Downloading {model_name} from {model_id} ...")
    model_dir = DATA_DIR / model_name
    model_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        AutoTokenizer.from_pretrained(model_id, cache_dir=str(model_dir))
        AutoModel.from_pretrained(model_id, cache_dir=str(model_dir))
        print(f"Successfully saved {model_name} to {model_dir}")
    except Exception as e:
        print(f"Error downloading {model_name}: {str(e)}")
        raise

if __name__ == "__main__":
    print(f"Downloading models to: {DATA_DIR}")
    for name, hf_id in MODELS.items():
        download_model(name, hf_id) 