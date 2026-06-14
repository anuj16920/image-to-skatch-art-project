"""Artistic style processors."""

from art_animator.styles.base import BaseStyleProcessor
from art_animator.styles.registry import StyleRegistry, register_style

__all__ = ["BaseStyleProcessor", "StyleRegistry", "register_style"]
