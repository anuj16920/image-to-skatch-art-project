#!/bin/bash
# Build release package

set -e

echo "Building AI Art Animator release..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Run tests
echo "Running tests..."
pytest tests/ -v

# Run linters
echo "Running linters..."
flake8 src/art_animator tests
black --check src/art_animator tests
isort --check src/art_animator tests

# Build package
echo "Building package..."
python -m build

echo "✅ Build complete!"
echo "Packages in dist/:"
ls -lh dist/
