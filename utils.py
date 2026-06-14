"""
Shared utilities — logging, image I/O, texture generation.

DEPRECATED: This file is kept for backward compatibility.
Please use: from art_animator.utils import Logger, pil_to_cv2, etc.
"""

import sys
from pathlib import Path

# Add new package to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import from new structure
from art_animator.utils.logger import Logger
from art_animator.utils.image_utils import (
    pil_to_cv2,
    cv2_to_pil,
    validate_image_path,
    resize_for_processing,
)
from art_animator.utils.texture_generator import get_paper_texture

__all__ = [
    "Logger",
    "pil_to_cv2",
    "cv2_to_pil",
    "validate_image_path",
    "resize_for_processing",
    "get_paper_texture",
]

# ══════════════════════════════════════════════════════════════════════════
# DEPRECATED CODE BELOW - Kept for reference only
# ══════════════════════════════════════════════════════════════════════════

"""
import os
import time
import numpy as np
from PIL import Image
import cv2


class Logger:
    """Thread-safe in-memory logger with optional callback."""

    def __init__(self, max_lines: int = 500):
        self.lines: list[str] = []
        self.max_lines = max_lines
        self.callback = None  # set by GUI

    def log(self, msg: str):
        ts = time.strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}"
        self.lines.append(entry)
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)
        if self.callback:
            self.callback(entry)
        print(entry)


def validate_image_path(path: str) -> tuple[bool, str]:
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
    """Convert PIL RGB → OpenCV BGR."""
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)


def cv2_to_pil(cv2_img: np.ndarray) -> Image.Image:
    """Convert OpenCV BGR → PIL RGB."""
    return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))


def resize_for_processing(img: np.ndarray, max_dim: int = 1200) -> tuple[np.ndarray, float]:
    """Resize image so the largest dimension ≤ max_dim. Returns (resized, scale)."""
    h, w = img.shape[:2]
    scale = min(max_dim / max(h, w), 1.0)
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img, scale


def get_paper_texture(width: int, height: int, bg_type: str = "White Paper") -> np.ndarray:
    """Generate a realistic paper/canvas texture background (BGR)."""
    if bg_type == "Pure White":
        return np.ones((height, width, 3), dtype=np.uint8) * 255

    if bg_type == "Pure Black":
        return np.zeros((height, width, 3), dtype=np.uint8)

    if bg_type == "Dark Canvas":
        base = np.random.randint(28, 45, (height, width, 3), dtype=np.uint8)
        noise = np.random.normal(0, 4, (height, width, 3)).astype(np.int16)
        canvas = np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return canvas

    # White Paper (default) and Aged Paper
    base_color = (245, 240, 235) if bg_type == "White Paper" else (210, 195, 160)

    # Generate layered noise for paper texture
    rng = np.random.default_rng(42)
    texture = np.full((height, width, 3), base_color, dtype=np.float32)

    # Coarse grain
    coarse = rng.normal(0, 6, (height // 4, width // 4, 3))
    coarse = cv2.resize(coarse.astype(np.float32), (width, height))
    texture += coarse

    # Fine grain
    fine = rng.normal(0, 3, (height, width, 3))
    texture += fine

    # Fiber lines (horizontal)
    for _ in range(height // 8):
        y = rng.integers(0, height)
        alpha = rng.uniform(0.3, 0.7)
        length = rng.integers(width // 4, width)
        x0 = rng.integers(0, width - length)
        thickness_variation = rng.normal(0, 1, length)
        texture[y, x0:x0 + length, :] -= alpha * 8 + thickness_variation[:, np.newaxis]

    if bg_type == "Aged Paper":
        # Add slight yellowing vignette
        cx, cy = width / 2, height / 2
        Y, X = np.ogrid[:height, :width]
        dist = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
        vignette = (dist / dist.max() * 20).astype(np.float32)
        texture[:, :, 2] -= vignette  # reduce blue → more yellow

    return np.clip(texture, 0, 255).astype(np.uint8)


def blend_stroke_on_background(
    background: np.ndarray,
    stroke_layer: np.ndarray,
    alpha: float = 1.0,
) -> np.ndarray:
    """Alpha-blend a stroke layer onto background."""
    bg = background.astype(np.float32)
    sl = stroke_layer.astype(np.float32)
    blended = bg + (sl - bg) * alpha
    return np.clip(blended, 0, 255).astype(np.uint8)