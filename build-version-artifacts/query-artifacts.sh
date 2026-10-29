#!/bin/bash

METADATA_DIR="metadata"

list_artifacts() {
    echo "=== Available Artifacts ==="
    for metadata in "$METADATA_DIR"/*.json; do
        if [ -f "$metadata" ]; then
            version=$(jq -r '.artifact.version' "$metadata")
            name=$(jq -r '.artifact.name' "$metadata")
            date=$(jq -r '.build.date' "$metadata")
            echo "Version: $version | Artifact: $name | Built: $date"
        fi
    done
}

get_artifact_info() {
    local version=$1
    for metadata in "$METADATA_DIR"/*.json; do
        if [ -f "$metadata" ]; then
            artifact_version=$(jq -r '.artifact.version' "$metadata")
            if [ "$artifact_version" = "$version" ]; then
                cat "$metadata" | jq '.'
                return 0
            fi
        fi
    done
    echo "No artifact found for version: $version"
    return 1
}

verify_artifact() {
    local artifact_path=$1
    local metadata_file="${METADATA_DIR}/$(basename "$artifact_path").json"
    
    if [ ! -f "$metadata_file" ]; then
        echo "Metadata file not found: $metadata_file"
        return 1
    fi
    
    expected_checksum=$(jq -r '.artifact.checksum.value' "$metadata_file")
    actual_checksum=$(sha256sum "$artifact_path" | awk '{print $1}')
    
    if [ "$expected_checksum" = "$actual_checksum" ]; then
        echo "Verification PASSED: Checksums match"
        return 0
    else
        echo "Verification FAILED: Checksums do not match"
        return 1
    fi
}

case $1 in
    list) list_artifacts ;;
    info) get_artifact_info "$2" ;;
    verify) verify_artifact "$2" ;;
    *) echo "Usage: $0 {list|info VERSION|verify ARTIFACT_PATH}"; exit 1 ;;
esac
