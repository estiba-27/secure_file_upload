package fileupload

default decision = {"allow": false, "reason": "Policy violation"}

decision = result {
    allow
    result := {"allow": true, "reason": ""}
}

allow {
    valid_size
    valid_mime
    valid_hash
    valid_filename
}

valid_size {
    input.size <= input.max_file_size
}

valid_mime {
    input.mime_type == allowed
}

allowed = m {
    m := input.allowed_mime_types[_]
}

valid_hash {
    not input.hash in input.hash_blacklist
}

valid_filename {
    re_match(input.filename_pattern, input.filename)
}

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

