from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import subprocess
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
import tempfile
from rdflib import Graph
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="dMaster Ontology System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base paths
BASE_DIR = Path(__file__).parent
ONTOLOGIES_DIR = BASE_DIR / "ontologies"
OUTPUT_DIR = BASE_DIR / "output"
TESTS_DIR = BASE_DIR / "tests"
SCRIPTS_DIR = BASE_DIR / "scripts"

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "dMaster Ontology System"}

@app.get("/api/ontologies")
async def get_ontologies():
    """Get list of all ontology files and their status."""
    try:
        ontologies = []
        for root, dirs, files in os.walk(ONTOLOGIES_DIR):
            for file in files:
                if file.endswith('.ttl'):
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(ONTOLOGIES_DIR)
                    
                    # Check if file is valid
                    is_valid = False
                    error_msg = None
                    triple_count = 0
                    
                    try:
                        g = Graph()
                        g.parse(file_path, format="turtle")
                        is_valid = True
                        triple_count = len(g)
                    except Exception as e:
                        error_msg = str(e)
                    
                    ontologies.append({
                        "name": file,
                        "path": str(relative_path),
                        "full_path": str(file_path),
                        "is_valid": is_valid,
                        "error": error_msg,
                        "triple_count": triple_count,
                        "size": file_path.stat().st_size
                    })
        
        return {"ontologies": ontologies}
    except Exception as e:
        logger.error(f"Error getting ontologies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ontology/{ontology_name}")
async def get_ontology_content(ontology_name: str):
    """Get content of a specific ontology file."""
    try:
        file_path = None
        for root, dirs, files in os.walk(ONTOLOGIES_DIR):
            if ontology_name in files:
                file_path = Path(root) / ontology_name
                break
        
        if not file_path or not file_path.exists():
            raise HTTPException(status_code=404, detail="Ontology file not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {"name": ontology_name, "content": content}
    except Exception as e:
        logger.error(f"Error getting ontology content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate")
async def validate_ontologies():
    """Run ontology validation tests."""
    try:
        # Run pytest on TTL syntax tests
        result = subprocess.run(
            ["python", "-m", "pytest", str(TESTS_DIR / "test_ttl_syntax.py"), "-v", "--tb=short"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    except Exception as e:
        logger.error(f"Error running validation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/combine")
async def combine_ontologies():
    """Combine all ontologies into a single file."""
    try:
        result = subprocess.run(
            ["python", str(SCRIPTS_DIR / "combine_ontologies.py")],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        
        combined_file = ONTOLOGIES_DIR / "combined_ontology.ttl"
        file_exists = combined_file.exists()
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "file_created": file_exists,
            "file_path": str(combined_file) if file_exists else None
        }
    except Exception as e:
        logger.error(f"Error combining ontologies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{file_type}")
async def download_file(file_type: str):
    """Download generated files."""
    try:
        if file_type == "combined":
            file_path = ONTOLOGIES_DIR / "combined_ontology.ttl"
        else:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type="text/turtle"
        )
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_ontology(file: UploadFile = File(...)):
    """Upload a new ontology file."""
    try:
        if not file.filename.endswith('.ttl'):
            raise HTTPException(status_code=400, detail="Only .ttl files are allowed")
        
        # Create uploads directory if it doesn't exist
        uploads_dir = ONTOLOGIES_DIR / "uploads"
        uploads_dir.mkdir(exist_ok=True)
        
        file_path = uploads_dir / file.filename
        
        # Save the file
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        # Validate the uploaded file
        is_valid = False
        error_msg = None
        try:
            g = Graph()
            g.parse(file_path, format="turtle")
            is_valid = True
        except Exception as e:
            error_msg = str(e)
        
        return {
            "success": True,
            "filename": file.filename,
            "path": str(file_path),
            "is_valid": is_valid,
            "error": error_msg
        }
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics."""
    try:
        stats = {
            "total_ontologies": 0,
            "valid_ontologies": 0,
            "invalid_ontologies": 0,
            "total_triples": 0,
            "ontology_domains": []
        }
        
        domain_stats = {}
        
        for root, dirs, files in os.walk(ONTOLOGIES_DIR):
            for file in files:
                if file.endswith('.ttl'):
                    stats["total_ontologies"] += 1
                    file_path = Path(root) / file
                    
                    # Get domain from directory name
                    domain = Path(root).name
                    if domain not in domain_stats:
                        domain_stats[domain] = {"count": 0, "valid": 0, "triples": 0}
                    
                    domain_stats[domain]["count"] += 1
                    
                    try:
                        g = Graph()
                        g.parse(file_path, format="turtle")
                        stats["valid_ontologies"] += 1
                        stats["total_triples"] += len(g)
                        domain_stats[domain]["valid"] += 1
                        domain_stats[domain]["triples"] += len(g)
                    except Exception:
                        stats["invalid_ontologies"] += 1
        
        stats["ontology_domains"] = [
            {"name": domain, **data} for domain, data in domain_stats.items()
        ]
        
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)