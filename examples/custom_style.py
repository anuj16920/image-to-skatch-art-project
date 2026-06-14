"""Example of creating a custom artistic style."""

import cv2
import numpy as np
from art_animator.styles import BaseStyleProcessor, register_style
from typing import Optional, Callable


@register_style("Neon Glow")
class NeonGlowProcessor(BaseStyleProcessor):
    """Custom neon glow effect style."""
    
    def process(
        self,
        img_bgr: np.ndarray,
        shading_intensity: float = 0.6,
        progress_cb: Optional[Callable[[float, str], None]] = None,
    ) -> np.ndarray:
        """Apply neon glow effect."""
        self._update_progress(progress_cb, 0.2, "Detecting edges...")
        
        # Edge detection
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        self._update_progress(progress_cb, 0.5, "Creating glow...")
        
        # Create glow effect
        glow = cv2.GaussianBlur(edges, (15, 15), 0)
        glow = cv2.GaussianBlur(glow, (15, 15), 0)
        
        # Colorize edges
        edges_colored = cv2.applyColorMap(edges, cv2.COLORMAP_HOT)
        glow_colored = cv2.applyColorMap(glow, cv2.COLORMAP_HOT)
        
        self._update_progress(progress_cb, 0.8, "Compositing...")
        
        # Dark background
        result = np.zeros_like(img_bgr)
        
        # Add glow
        result = cv2.addWeighted(result, 1.0, glow_colored, 0.7, 0)
        
        # Add sharp edges
        result = cv2.addWeighted(result, 1.0, edges_colored, shading_intensity, 0)
        
        self._update_progress(progress_cb, 1.0, "Complete")
        
        return result


# Usage example
if __name__ == "__main__":
    from art_animator import ArtProcessor
    from art_animator.utils import Logger
    from art_animator.styles import StyleRegistry
    
    # Register custom style
    # (Already registered via decorator)
    
    # Verify registration
    print("Available styles:", StyleRegistry.list_styles())
    
    # Use custom style
    logger = Logger()
    processor = ArtProcessor(logger)
    
    # Note: You'll need to modify ArtProcessor to use StyleRegistry
    # This is an example of how the plugin system would work
    print("\nCustom style 'Neon Glow' is registered and ready to use!")
