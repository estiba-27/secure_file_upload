from fastapi import APIRouter, UploadFile, File
import os
import shutil
import hashlib
from datetime import datetime
from typing import List
import requests

from app.schemas import FileResponse
from app.services.policy import policy_rules, update_policy
router = APIRouter(prefix="/api")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
ACCEPTED_DIR = os.path.join(STORAGE_DIR, "accepted")
REJECTED_DIR = os.path.join(STORAGE_DIR, "rejected")

os.makedirs(ACCEPTED_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)

OPA_URL = os.getenv(
    "OPA_URL",
    "http://localhost:8181/v1/data/fileupload/decision"
)

uploaded_files: List[dict] = []

def generate_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def evaluate_policy(input_data: dict) -> dict:
    response = requests.post(
        OPA_URL,
        json={"input": input_data},
        timeout=5
    )
    response.raise_for_status()
    return response.json()["result"]

@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...)):
    temp_path = os.path.join(REJECTED_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    size_bytes = os.path.getsize(temp_path)
    file_hash = generate_hash(temp_path)

    opa_input = {
        "size": size_bytes,
        "mime_type": file.content_type,
        "filename": file.filename,
        "hash": file_hash,
        "max_file_size": policy_rules["max_file_size"],
        "allowed_mime_types": policy_rules["allowed_mime_types"],
        "hash_blacklist": policy_rules["hash_blacklist"],
        "filename_pattern": policy_rules["filename_pattern"]
    }

    decision = evaluate_policy(opa_input)

    if decision.get("allow", False):
        final_path = os.path.join(ACCEPTED_DIR, file.filename)
        shutil.move(temp_path, final_path)
        status = "accepted"
        reason = None
    else:
        final_path = temp_path
        status = "rejected"
        reason = decision.get("reason", "Policy violation")

    record = {
        "filename": file.filename,
        "size": size_bytes,
        "hash": file_hash,
        "status": status,
        "reason": reason,
        "uploaded_at": datetime.utcnow().isoformat()
    }

    uploaded_files.append(record)
    return record

@router.get("/files", response_model=List[FileResponse])
def list_files():
    return uploaded_files

@router.get("/policies")
def get_policy():
    return policy_rules

@router.post("/policies")
def set_policy(policy_input: dict):
    update_policy(
        max_file_size=policy_input.get("max_file_size"),
        allowed_mime_types=policy_input.get("allowed_mime_types"),
        hash_blacklist=policy_input.get("hash_blacklist"),
        filename_pattern=policy_input.get("filename_pattern")
    )
    return {"message": "Policy updated successfully", "policy": policy_rules}

