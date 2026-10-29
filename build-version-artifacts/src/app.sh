#!/bin/bash
# Simple calculator application
VERSION="0.0.0"

calculate() {
    echo "Calculator v${VERSION}"
    echo "Result: $(($1 + $2))"
}

calculate "$@"
