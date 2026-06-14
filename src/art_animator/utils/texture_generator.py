"""Paper texture generation utilities."""

from __future__ import annotations
import cv2
import numpy as np
from typing import Tuple


def get_paper_texture(
    width: int,
    height: int,
    bg_type: str = "White Paper",
) -> np.ndarray:
    """
    Generate procedural paper/canvas texture.
    
    Args:
        width: Texture width in pixels
        height: Texture height in pixels
        bg_type: Background type (White Paper, Aged Paper, Dark Canvas, etc.)
        
    Returns:
        BGR image with paper texture
    """
    if bg_type == "Pure White":
        return np.full((height, width, 3), 255, dtype=np.uint8)
    
    if bg_type == "Pure Black":
        return np.zeros((height, width, 3), dtype=np.uint8)
    
    # Base color
    if bg_type == "Aged Paper":
        base = np.full((height, width, 3), [220, 235, 245], dtype=np.uint8)
    elif bg_type == "Dark Canvas":
        base = np.full((height, width, 3), [35, 35, 40], dtype=np.uint8)
    else:  # White Paper
        base = np.full((height, width, 3), [245, 248, 250], dtype=np.uint8)
    
    # Coarse grain
    rng = np.random.default_rng(42)
    coarse = rng.integers(-8, 9, (height, width), dtype=np.int16)
    coarse = cv2.GaussianBlur(coarse.astype(np.float32), (5, 5), 0)
    
    # Fine grain
    fine = rng.integers(-3, 4, (height, width), dtype=np.int16)
    
    # Fiber lines
    for _ in range(int(height * 0.02)):
        y = rng.integers(0, height)
        x_start = rng.integers(0, width // 2)
        x_end = rng.integers(width // 2, width)
        cv2.line(
            fine,
            (x_start, y),
            (x_end, y),
            int(rng.integers(-2, 3)),
            1,
        )
    
    # Combine
    combined = base.astype(np.int16) + coarse[..., None] + fine[..., None]
    combined = np.clip(combined, 0, 255).astype(np.uint8)
    
    # Vignette for aged paper
    if bg_type == "Aged Paper":
        cy, cx = height // 2, width // 2
        Y, X = np.ogrid[:height, :width]
        dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
        max_dist = np.sqrt(cx ** 2 + cy ** 2)
        vignette = 1.0 - (dist / max_dist) * 0.15
        combined = (combined * vignette[..., None]).astype(np.uint8)
    
    return combined
