package fileupload

# Default: reject
default decision = {"allow": false, "reason": "Policy violation"}

# Accept only if all checks pass
decision = {"allow": true, "reason": ""} {
    valid_size
    valid_mime
    valid_hash
    valid_filename
}

# File size check
valid_size {
    input.size <= input.max_file_size
}

# MIME type check
valid_mime {
    some i
    input.mime_type == input.allowed_mime_types[i]
}

# Hash blacklist check
valid_hash {
    not input.hash in input.hash_blacklist
}

# Filename pattern check
valid_filename {
    re_match(input.filename_pattern, input.filename)
}

# Detailed failure reasons
decision = {"allow": false, "reason": reason} {
    not valid_size
    reason := sprintf("File too large. Max allowed: %d bytes", [input.max_file_size])
}

decision = {"allow": false, "reason": reason} {
    not valid_mime
    reason := sprintf("Invalid MIME type. Allowed: %v", [input.allowed_mime_types])
}

decision = {"allow": false, "reason": reason} {
    not valid_hash
    reason := "File hash is blacklisted"
}

decision = {"allow": false, "reason": reason} {
    not valid_filename
    reason := sprintf("Filename does not match pattern: %s", [input.filename_pattern])
}
