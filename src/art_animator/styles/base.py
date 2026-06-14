"""Base class for style processors."""

from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
from typing import Optional, Callable


class BaseStyleProcessor(ABC):
    """
    Abstract base class for artistic style processors.
    
    All style implementations should inherit from this class and implement
    the process() method.
    """
    
    def __init__(self, name: str):
        """
        Initialize style processor.
        
        Args:
            name: Human-readable name of the style
        """
        self.name = name
    
    @abstractmethod
    def process(
        self,
        img_bgr: np.ndarray,
        shading_intensity: float = 0.6,
        progress_cb: Optional[Callable[[float, str], None]] = None,
    ) -> np.ndarray:
        """
        Apply artistic style to image.
        
        Args:
            img_bgr: Input image in BGR format
            shading_intensity: Intensity of shading effects (0.0-1.0)
            progress_cb: Optional callback for progress updates
            
        Returns:
            Styled image in BGR format
        """
        pass
    
    def _update_progress(
        self,
        progress_cb: Optional[Callable[[float, str], None]],
        value: float,
        label: str = "",
    ) -> None:
        """Helper to update progress callback."""
        if progress_cb:
            progress_cb(value, label)
