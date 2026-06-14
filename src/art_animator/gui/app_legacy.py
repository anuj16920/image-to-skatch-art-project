"""Legacy GUI wrapper for backward compatibility."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from art_animator.gui.main import AIArtAnimatorApp, launch

__all__ = ["AIArtAnimatorApp", "launch"]
