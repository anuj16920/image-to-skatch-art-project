#!/bin/bash
# Development environment setup script

set -e

echo "Setting up AI Art Animator development environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install package in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

echo "✅ Development environment ready!"
echo ""
echo "To activate: source venv/bin/activate"
echo "To run tests: pytest tests/"
echo "To run GUI: art-animator-gui"
