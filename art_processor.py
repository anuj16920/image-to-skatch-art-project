"""
Art Style Processor — converts source images into artistic renditions.

DEPRECATED: This file is kept for backward compatibility.
Please use: from art_animator.core.art_processor import ArtProcessor
"""

import sys
from pathlib import Path

# Add new package to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import from new structure
from art_animator.core.art_processor import ArtProcessor

__all__ = ["ArtProcessor"]

# ══════════════════════════════════════════════════════════════════════════
# DEPRECATED CODE BELOW - Kept for reference only
# ══════════════════════════════════════════════════════════════════════════

"""
from __future__ import annotations
import cv2
import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter
from skimage import exposure, color as skcolor
from utils import Logger, pil_to_cv2, cv2_to_pil, resize_for_processing
from typing import Callable, Optional


class ArtProcessor:

    def __init__(self, logger: Logger):
        self.logger = logger

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC API
    # ══════════════════════════════════════════════════════════════════════════

    def apply_style(
        self,
        image_path: str,
        style: str,
        shading_intensity: float = 0.6,
        progress_cb: Optional[Callable] = None,
    ) -> Image.Image:
        """Apply the chosen artistic style and return a PIL image."""
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            raise ValueError(f"Cannot read image: {image_path}")
        img_bgr, _ = resize_for_processing(img_bgr, max_dim=1400)

        def prog(v, label=""):
            if progress_cb:
                progress_cb(v, label)

        prog(0.15, "Loading image...")
        style_map = {
            "Pencil Sketch":    self._pencil_sketch,
            "Advanced Sketch":  self._advanced_sketch,
            "Watercolor":       self._watercolor,
            "Oil Painting":     self._oil_painting,
            "Charcoal":         self._charcoal,
            "Anime / Manga":    self._anime,
        }
        fn = style_map.get(style, self._pencil_sketch)
        prog(0.3, f"Applying {style}...")
        result_bgr = fn(img_bgr, shading_intensity)
        prog(0.9, "Finalizing...")
        return cv2_to_pil(result_bgr)

    # ══════════════════════════════════════════════════════════════════════════
    # STYLE IMPLEMENTATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def _pencil_sketch(self, img: np.ndarray, intensity: float) -> np.ndarray:
        """Classic dodge-blend pencil sketch."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        inv = cv2.bitwise_not(gray)
        blur_k = max(21, int(intensity * 80) | 1)
        blurred = cv2.GaussianBlur(inv, (blur_k, blur_k), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256.0)
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)
        # Add fine grain
        noise = np.random.normal(0, 3 * intensity, sketch.shape).astype(np.int16)
        sketch = np.clip(sketch.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

    def _advanced_sketch(self, img: np.ndarray, intensity: float) -> np.ndarray:
        """Edge-aware sketch with multi-scale details."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Normalize
        gray = exposure.equalize_adapthist(gray, clip_limit=0.025)
        gray = (gray * 255).astype(np.uint8)

        # Multi-scale Canny edges
        edges_fine  = cv2.Canny(gray, 30,  90)
        edges_mid   = cv2.Canny(gray, 15,  50)
        edges_coarse= cv2.Canny(cv2.GaussianBlur(gray, (5,5), 0), 10, 40)
        edges = np.maximum(np.maximum(edges_fine, edges_mid), edges_coarse)

        # Base sketch via dodge
        inv    = cv2.bitwise_not(gray)
        blur_k = max(15, int(intensity * 60) | 1)
        blurred = cv2.GaussianBlur(inv, (blur_k, blur_k), 0)
        base   = cv2.divide(gray, 255 - blurred, scale=256.0)

        # Merge edges into base
        edge_f = (255 - edges).astype(np.float32) / 255.0
        result = (base.astype(np.float32) * edge_f * 0.85 +
                  base.astype(np.float32) * 0.15)
        result = np.clip(result, 0, 255).astype(np.uint8)
        # Directional texture
        result = self._add_pencil_texture(result, intensity)
        return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    def _watercolor(self, img: np.ndarray, intensity: float) -> np.ndarray:
        """Watercolor using bilateral filtering + edge preservation + color quantization."""
        # Bilateral smoothing passes
        smooth = img.copy()
        passes = max(2, int(intensity * 6))
        for _ in range(passes):
            smooth = cv2.bilateralFilter(smooth, 9, 75, 75)

        # Color quantization (K-means)
        data = smooth.reshape((-1, 3)).astype(np.float32)
        k = max(8, int(12 * intensity))
        _, labels, centers = cv2.kmeans(
            data, k, None,
            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0),
            4, cv2.KMEANS_RANDOM_CENTERS
        )
        quantized = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)

        # Edge detection for brush strokes
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(
            cv2.medianBlur(gray, 7), 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
        )
        edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Blend quantized color with edges
        result = cv2.bitwise_and(quantized, edges_bgr)

        # Slight diffusion halo
        halo = cv2.GaussianBlur(result, (5, 5), 0)
        result = cv2.addWeighted(result, 0.85, halo, 0.15, 0)

        # Boost saturation
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (1.0 + 0.4 * intensity), 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    def _oil_painting(self, img: np.ndarray, intensity: float) -> np.ndarray:
        """Oil painting via xPhoto oilPainting + texture."""
        try:
            result = cv2.xphoto.oilPainting(img, 7, 1)
        except AttributeError:
            # Fallback: aggressive bilateral + emboss
            result = img.copy()
            for _ in range(3):
                result = cv2.bilateralFilter(result, 15, 80, 80)
            kernel_sharpener = np.array([[-1,-1,-1],
                                          [-1, 9,-1],
                                          [-1,-1,-1]])
            result = cv2.filter2D(result, -1, kernel_sharpener)

        # Add brushstroke texture
        h, w = result.shape[:2]
        brush_noise = np.random.normal(0, 8 * intensity, (h, w, 3)).astype(np.int16)
        # Smooth the noise to simulate brush direction
        brush_noise[:, :, 0] = uniform_filter(brush_noise[:, :, 0], size=15)
        brush_noise[:, :, 1] = uniform_filter(brush_noise[:, :, 1], size=15)
        brush_noise[:, :, 2] = uniform_filter(brush_noise[:, :, 2], size=15)
        result = np.clip(result.astype(np.int16) + brush_noise * 0.4, 0, 255).astype(np.uint8)

        # Enhance contrast
        lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB).astype(np.float32)
        lab[:, :, 0] = np.clip(lab[:, :, 0] * 1.1, 0, 255)
        return cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)

    def _charcoal(self, img: np.ndarray, intensity: float) -> np.ndarray:
        """Charcoal drawing — dark, smudgy, dramatic."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Invert
        inv = cv2.bitwise_not(gray)
        # Heavy blur for smudge
        smudge_k = max(25, int(intensity * 100) | 1)
        smudge = cv2.GaussianBlur(inv, (smudge_k, smudge_k), 0)
        charcoal = cv2.divide(gray, 255 - smudge, scale=256.0)

        # Darken significantly
        charcoal = np.clip(charcoal.astype(np.float32) * (1.0 - intensity * 0.3), 0, 255).astype(np.uint8)

        # Add grain / smudge texture
        noise = np.random.normal(0, 12 * intensity, gray.shape).astype(np.int16)
        noise = cv2.GaussianBlur(noise.astype(np.float32), (3, 3), 0).astype(np.int16)
        charcoal = np.clip(charcoal.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        # High-contrast edges
        edges = cv2.Canny(gray, 20, 60)
        edges_dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8))
        charcoal[edges_dilated > 0] = np.clip(
            charcoal[edges_dilated > 0].astype(int) - 40, 0, 255
        ).astype(np.uint8)

        return cv2.cvtColor(charcoal, cv2.COLOR_GRAY2BGR)

    def _anime(self, img: np.ndarray, intensity: float) -> np.ndarray:
        """Anime / Manga cel-shaded style."""
        # Flatten colors
        smooth = cv2.bilateralFilter(img, 15, 80, 80)
        smooth = cv2.bilateralFilter(smooth, 9, 60, 60)

        # Color quantization
        data  = smooth.reshape((-1, 3)).astype(np.float32)
        k     = 6
        _, labels, centers = cv2.kmeans(
            data, k, None,
            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0),
            4, cv2.KMEANS_RANDOM_CENTERS
        )
        flat = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)

        # Bold outlines
        gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 200)
        k_size = max(1, int(intensity * 3))
        edges  = cv2.dilate(edges, np.ones((k_size, k_size), np.uint8))
        outline= cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Burn outlines onto flat colors
        result = flat.copy()
        mask   = edges > 0
        result[mask] = np.clip(
            result[mask].astype(int) - 120, 0, 255
        ).astype(np.uint8)

        # Boost saturation
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.6, 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.05, 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def _add_pencil_texture(gray: np.ndarray, intensity: float) -> np.ndarray:
        """Overlay directional pencil hatching texture."""
        h, w = gray.shape
        texture = np.zeros_like(gray, dtype=np.float32)

        rng = np.random.default_rng(7)
        n_lines = int(h * intensity * 2)
        for _ in range(n_lines):
            x0 = rng.integers(0, w)
            y0 = rng.integers(0, h)
            angle = rng.uniform(0, np.pi)
            length = rng.integers(10, 40)
            dx = int(np.cos(angle) * length)
            dy = int(np.sin(angle) * length)
            alpha = rng.uniform(0.02, 0.08)
            cv2.line(texture, (x0, y0), (x0 + dx, y0 + dy), alpha, 1, cv2.LINE_AA)

        texture_smooth = cv2.GaussianBlur(texture, (3, 3), 0)
        result = np.clip(gray.astype(np.float32) - texture_smooth * 60 * intensity, 0, 255)
        return result.astype(np.uint8)