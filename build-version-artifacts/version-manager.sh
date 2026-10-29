#!/bin/bash

VERSION_FILE="VERSION"
CHANGELOG_FILE="CHANGELOG.md"

init_version() {
    if [ ! -f "$VERSION_FILE" ]; then
        echo "0.1.0" > "$VERSION_FILE"
        echo "Version initialized to 0.1.0"
    fi
}

get_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "0.0.0"
    fi
}

bump_version() {
    local bump_type=$1
    local current_version=$(get_version)
    
    IFS='.' read -r major minor patch <<< "$current_version"
    
    case $bump_type in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
        *)
            echo "Invalid bump type. Use: major, minor, or patch"
            exit 1
            ;;
    esac
    
    new_version="${major}.${minor}.${patch}"
    echo "$new_version" > "$VERSION_FILE"
    echo "Version bumped to $new_version"
}

update_changelog() {
    local version=$1
    local message=$2
    local date=$(date +%Y-%m-%d)
    
    echo "## [${version}] - ${date}" >> "$CHANGELOG_FILE"
    echo "- ${message}" >> "$CHANGELOG_FILE"
    echo "" >> "$CHANGELOG_FILE"
    echo "Changelog updated for version $version"
}

case $1 in
    init)
        init_version
        ;;
    get)
        get_version
        ;;
    bump)
        bump_version "$2"
        ;;
    changelog)
        update_changelog "$(get_version)" "$2"
        ;;
    *)
        echo "Usage: $0 {init|get|bump major|minor|patch|changelog 'message'}"
        exit 1
        ;;
esac
