"""Convenience script to run CLI from project root."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from art_animator.cli import main

if __name__ == "__main__":
    main()
