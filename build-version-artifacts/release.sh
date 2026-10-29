#!/bin/bash

release() {
    local release_type=$1
    local release_notes=$2
    
    if [ -z "$release_type" ]; then
        echo "Usage: $0 {major|minor|patch} 'release notes'"
        exit 1
    fi
    
    if ! git diff-index --quiet HEAD --; then
        echo "Error: Working directory has uncommitted changes"
        exit 1
    fi
    
    ./version-manager.sh bump "$release_type"
    new_version=$(./version-manager.sh get)
    
    if [ -n "$release_notes" ]; then
        ./version-manager.sh changelog "$release_notes"
    fi
    
    git add VERSION CHANGELOG.md
    git commit -m "Bump version to $new_version"
    
    ./build.sh
    
    git add builds/ metadata/
    git commit -m "Add build artifacts for version $new_version"
    
    echo "=== Release Complete for Version $new_version ==="
}

release "$@"
