from typing import List, Optional

policy_rules = {
    "max_file_size": 5 * 1024 * 1024,  # 5 MB
    "allowed_mime_types": ["application/pdf", "image/png", "image/jpeg"],
    "hash_blacklist": [],
    # Allow letters, digits, underscores, dashes, spaces, parentheses, dots
    "filename_pattern": r"^[\w\s\-\(\)]+(\.[a-zA-Z0-9]+)+$"
}

def update_policy(
    max_file_size: Optional[int] = None,
    allowed_mime_types: Optional[List[str]] = None,
    hash_blacklist: Optional[List[str]] = None,
    filename_pattern: Optional[str] = None
):
    if max_file_size is not None:
        policy_rules["max_file_size"] = max_file_size
    if allowed_mime_types is not None:
        policy_rules["allowed_mime_types"] = allowed_mime_types
    if hash_blacklist is not None:
        policy_rules["hash_blacklist"] = hash_blacklist
    if filename_pattern is not None:
        policy_rules["filename_pattern"] = filename_pattern
