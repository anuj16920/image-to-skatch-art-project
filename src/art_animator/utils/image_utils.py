"""Image processing utilities."""

from __future__ import annotations
import os
import cv2
import numpy as np
from PIL import Image
from typing import Tuple


def validate_image_path(path: str) -> Tuple[bool, str]:
    """
    Validate that a path points to a readable image file.
    
    Args:
        path: Path to image file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.isfile(path):
        return False, "File not found."
    
    ext = os.path.splitext(path)[1].lower()
    if ext not in {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}:
        return False, f"Unsupported format: {ext}"
    
    try:
        img = Image.open(path)
        img.verify()
    except Exception as e:
        return False, f"Cannot read image: {e}"
    
    return True, ""


def pil_to_cv2(pil_img: Image.Image) -> np.ndarray:
    """
    Convert PIL RGB image to OpenCV BGR format.
    
    Args:
        pil_img: PIL Image in RGB format
        
    Returns:
        NumPy array in BGR format
    """
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_img: np.ndarray) -> Image.Image:
    """
    Convert OpenCV BGR image to PIL RGB format.
    
    Args:
        cv2_img: NumPy array in BGR format
        
    Returns:
        PIL Image in RGB format
    """
    return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))


def resize_for_processing(
    img: np.ndarray,
    max_dim: int = 1400,
) -> Tuple[np.ndarray, float]:
    """
    Resize image for processing while maintaining aspect ratio.
    
    Args:
        img: Input image (BGR)
        max_dim: Maximum dimension (width or height)
        
    Returns:
        Tuple of (resized_image, scale_factor)
    """
    h, w = img.shape[:2]
    scale = min(1.0, max_dim / max(h, w))
    
    if scale < 1.0:
        new_w = int(w * scale)
        new_h = int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return img, scale
