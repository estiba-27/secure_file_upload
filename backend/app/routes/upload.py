from fastapi import APIRouter, UploadFile, File
import os
import shutil
import hashlib
from datetime import datetime
from typing import List
import re

from app.schemas import FileResponse
from app.services.policy import policy_rules  # statically read policy

router = APIRouter(prefix="/api")

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
ACCEPTED_DIR = os.path.join(STORAGE_DIR, "accepted")
REJECTED_DIR = os.path.join(STORAGE_DIR, "rejected")

os.makedirs(ACCEPTED_DIR, exist_ok=True)
os.makedirs(REJECTED_DIR, exist_ok=True)

# Uploaded files list
uploaded_files: List[dict] = []


def generate_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def evaluate_policy(input_data: dict) -> dict:
    """
    Evaluate policy locally based on policy_rules (static Python check)
    instead of calling OPA server.
    """
    # Size check
    if input_data["size"] > input_data["max_file_size"]:
        return {"allow": False, "reason": f"File too large. Max: {input_data['max_file_size']} bytes"}

    # MIME type check
    if input_data["mime_type"] not in input_data["allowed_mime_types"]:
        return {"allow": False, "reason": f"Invalid MIME type. Allowed: {input_data['allowed_mime_types']}"}

    # Hash blacklist check
    if input_data["hash"] in input_data["hash_blacklist"]:
        return {"allow": False, "reason": "File hash is blacklisted"}

    # Filename pattern check
    if not re.match(input_data["filename_pattern"], input_data["filename"]):
        return {"allow": False, "reason": f"Filename does not match pattern: {input_data['filename_pattern']}"}

    # If all checks pass
    return {"allow": True, "reason": None}


@router.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...)):
    temp_path = os.path.join(REJECTED_DIR, file.filename)

    # Save file to temporary path
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        buffer.flush()
        os.fsync(buffer.fileno())

    # Get real size and hash
    size_bytes = os.path.getsize(temp_path)
    file_hash = generate_hash(temp_path)

    # Prepare input for policy evaluation
    policy_input = {
        "size": size_bytes,
        "mime_type": file.content_type,
        "filename": file.filename,
        "hash": file_hash,
        "max_file_size": policy_rules["max_file_size"],
        "allowed_mime_types": policy_rules["allowed_mime_types"],
        "hash_blacklist": policy_rules["hash_blacklist"],
        "filename_pattern": policy_rules["filename_pattern"]
    }

    decision = evaluate_policy(policy_input)

    if decision["allow"]:
        final_path = os.path.join(ACCEPTED_DIR, file.filename)
        shutil.move(temp_path, final_path)
        status = "accepted"
        reason = None
    else:
        final_path = temp_path
        status = "rejected"
        reason = decision["reason"]


    record = {
        "filename": file.filename,
        "size": size_bytes,                     
        "size_mb": round(size_bytes / (1024 * 1024), 4),  
        "hash": file_hash,
        "status": status,
        "reason": reason,
        "uploaded_at": datetime.utcnow().isoformat(),
    }

    uploaded_files.append(record)
    return record


@router.get("/files", response_model=List[FileResponse])
def list_files():
    return uploaded_files


@router.get("/policies")
def get_policy():
    return policy_rules
