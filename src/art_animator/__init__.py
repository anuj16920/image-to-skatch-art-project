"""
AI Art Animator - Professional stroke-level drawing animation system.

This package provides tools for converting static images into realistic
"artist drawing" videos with multiple artistic styles and extensive
customization options.
"""

__version__ = "1.0.0"
__author__ = "AI Art Animator Team"

from art_animator.core.animator import ArtAnimator
from art_animator.core.stroke_engine import StrokeEngine, Stroke, StrokeLayer
from art_animator.core.art_processor import ArtProcessor
from art_animator.config.settings import Config

__all__ = [
    "ArtAnimator",
    "StrokeEngine",
    "Stroke",
    "StrokeLayer",
    "ArtProcessor",
    "Config",
]
