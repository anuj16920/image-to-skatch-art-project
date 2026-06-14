"""Convenience script to run GUI from project root."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from art_animator.gui.main import launch

if __name__ == "__main__":
    launch()
