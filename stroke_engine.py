"""
Stroke Engine — The heart of the realistic drawing simulation.

DEPRECATED: This file is kept for backward compatibility.
Please use: from art_animator.core.stroke_engine import StrokeEngine, Stroke, StrokeLayer
"""

import sys
from pathlib import Path

# Add new package to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import from new structure
from art_animator.core.stroke_engine import StrokeEngine, Stroke, StrokeLayer, SmoothNoise

__all__ = ["StrokeEngine", "Stroke", "StrokeLayer", "SmoothNoise"]

# ══════════════════════════════════════════════════════════════════════════
# DEPRECATED CODE BELOW - Kept for reference only
# ══════════════════════════════════════════════════════════════════════════

"""
from __future__ import annotations
import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from scipy.interpolate import CubicSpline


# ─── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class Stroke:
    """A single stroke: a sequence of (x,y) points with per-point attributes."""
    points:    np.ndarray          # shape (N, 2)  float32
    thickness: np.ndarray          # shape (N,)    float32
    darkness:  float = 0.85        # 0=white  1=black
    layer:     int   = 0           # 0=outline 1=detail 2=shading
    color:     Tuple[int,...] = (20, 20, 20)


@dataclass
class StrokeLayer:
    name:    str
    strokes: List[Stroke] = field(default_factory=list)


# ─── Perlin-like Noise ────────────────────────────────────────────────────────

class SmoothNoise:
    """Fast 1-D smooth noise via cosine interpolation of random seeds."""

    def __init__(self, seed: int = 0):
        rng = np.random.default_rng(seed)
        self._base = rng.uniform(-1, 1, 4096)

    def __call__(self, t: float, freq: float = 1.0) -> float:
        idx = (t * freq) % len(self._base)
        i   = int(idx)
        f   = idx - i
        v0  = self._base[i % len(self._base)]
        v1  = self._base[(i + 1) % len(self._base)]
        # Cosine interpolation
        ft  = (1.0 - np.cos(f * np.pi)) * 0.5
        return v0 * (1 - ft) + v1 * ft

    def array(self, n: int, freq: float = 1.0, scale: float = 1.0) -> np.ndarray:
        t = np.linspace(0, n / 20.0, n)
        return np.array([self(ti, freq) for ti in t]) * scale


# ─── Main Engine ──────────────────────────────────────────────────────────────

class StrokeEngine:

    def __init__(
        self,
        detail_level: int = 75,        # 10–100
        human_jitter: bool = True,
        style: str = "Pencil Sketch",
    ):
        self.detail_level  = detail_level / 100.0
        self.human_jitter  = human_jitter
        self.style         = style
        self._noise_x      = SmoothNoise(seed=3)
        self._noise_y      = SmoothNoise(seed=7)
        self._noise_p      = SmoothNoise(seed=11)   # pressure noise

    # ══════════════════════════════════════════════════════════════════════════
    # PUBLIC: analyze image → list of ordered StrokeLayers
    # ══════════════════════════════════════════════════════════════════════════

    def extract_stroke_layers(
        self,
        source_bgr: np.ndarray,
        styled_bgr: np.ndarray,
    ) -> List[StrokeLayer]:
        """
        Returns three layers:
          Layer 0 — Rough outline  (main contours)
          Layer 1 — Mid details    (secondary edges)
          Layer 2 — Fine shading   (tonal hatching)
        """
        gray   = cv2.cvtColor(source_bgr, cv2.COLOR_BGR2GRAY)
        styled_gray = cv2.cvtColor(styled_bgr, cv2.COLOR_BGR2GRAY)
        h, w   = gray.shape

        layers = []

        # ── Layer 0: Main contours ─────────────────────────────────────────
        outline_layer = StrokeLayer("outline")
        edges_coarse  = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 20, 60)
        contours, hierarchy = cv2.findContours(
            edges_coarse, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS
        )
        # Order: larger contours first (outer structures)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        max_contours = max(10, int(len(contours) * 0.3 * self.detail_level))
        for cnt in contours[:max_contours]:
            if cv2.contourArea(cnt) < 30:
                continue
            stroke = self._contour_to_stroke(cnt, gray, layer=0, thickness_range=(1.8, 3.5))
            if stroke:
                outline_layer.strokes.append(stroke)
        layers.append(outline_layer)

        # ── Layer 1: Detail edges ──────────────────────────────────────────
        detail_layer = StrokeLayer("detail")
        edges_fine   = cv2.Canny(gray, 40, 120)
        contours2, _ = cv2.findContours(
            edges_fine, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1
        )
        contours2 = sorted(contours2, key=cv2.contourArea, reverse=True)
        max_detail = max(20, int(len(contours2) * 0.5 * self.detail_level))
        for cnt in contours2[:max_detail]:
            if cv2.contourArea(cnt) < 15:
                continue
            stroke = self._contour_to_stroke(cnt, gray, layer=1, thickness_range=(0.8, 2.0))
            if stroke:
                detail_layer.strokes.append(stroke)
        layers.append(detail_layer)

        # ── Layer 2: Tonal shading ─────────────────────────────────────────
        shade_layer = StrokeLayer("shading")
        shade_strokes = self._generate_shading_strokes(styled_gray, source_bgr)
        shade_layer.strokes = shade_strokes
        layers.append(shade_layer)

        return layers

    # ══════════════════════════════════════════════════════════════════════════
    # CONTOUR → STROKE
    # ══════════════════════════════════════════════════════════════════════════

    def _contour_to_stroke(
        self,
        contour: np.ndarray,
        gray: np.ndarray,
        layer: int,
        thickness_range: Tuple[float, float] = (1.0, 2.5),
    ) -> Optional[Stroke]:
        """Convert an OpenCV contour to a smooth, jittered Stroke."""
        pts = contour.reshape(-1, 2).astype(np.float32)
        if len(pts) < 4:
            return None

        # Subsample dense contours
        if len(pts) > 200:
            idx = np.linspace(0, len(pts) - 1, 200, dtype=int)
            pts = pts[idx]

        # Smooth via Catmull-Rom spline
        pts = self._smooth_path(pts)
        if pts is None or len(pts) < 3:
            return None

        # Pressure from local image gradient (darker areas → thicker)
        thickness = self._compute_pressure(pts, gray, thickness_range)

        # Human jitter
        if self.human_jitter:
            pts = self._apply_jitter(pts, magnitude=1.2)

        # Color from style
        color = self._stroke_color(layer)
        darkness = np.clip(0.6 + layer * 0.1, 0, 1.0)

        return Stroke(points=pts, thickness=thickness, darkness=darkness,
                      layer=layer, color=color)

    # ══════════════════════════════════════════════════════════════════════════
    # SHADING STROKES
    # ══════════════════════════════════════════════════════════════════════════

    def _generate_shading_strokes(
        self,
        gray: np.ndarray,
        source_bgr: np.ndarray,
    ) -> List[Stroke]:
        """
        Generate hatching / cross-hatching strokes in dark areas.
        Stroke density is proportional to local darkness.
        """
        h, w = gray.shape
        strokes: List[Stroke] = []

        # Downsample for speed
        scale  = min(1.0, 600 / max(h, w))
        gh, gw = int(h * scale), int(w * scale)
        small  = cv2.resize(gray, (gw, gh), interpolation=cv2.INTER_AREA)

        # Divide image into a grid; shade each cell proportionally
        cell   = max(12, int(min(gh, gw) / 40))
        rng    = np.random.default_rng(42)

        for gy in range(0, gh - cell, cell):
            for gx in range(0, gw - cell, cell):
                patch    = small[gy:gy + cell, gx:gx + cell]
                lum      = patch.mean() / 255.0   # 0=dark 1=bright
                darkness = 1.0 - lum              # 1=lots of strokes

                if darkness < 0.15:               # skip very bright areas
                    continue

                n_strokes = int(darkness * self.detail_level * 4)
                if n_strokes < 1:
                    continue

                # Hatch direction tied to local gradient orientation
                patch_big = gray[int(gy / scale):int((gy + cell) / scale),
                                  int(gx / scale):int((gx + cell) / scale)]
                angle = self._local_gradient_angle(patch_big)

                for si in range(n_strokes):
                    # Map back to full resolution
                    fx = int(gx / scale) + rng.integers(0, int(cell / scale))
                    fy = int(gy / scale) + rng.integers(0, int(cell / scale))
                    length = rng.integers(8, max(9, int(30 * darkness * self.detail_level)))

                    jitter_angle = angle + rng.uniform(-0.25, 0.25)
                    dx = np.cos(jitter_angle) * length
                    dy = np.sin(jitter_angle) * length

                    n_pts = max(4, length // 4)
                    t     = np.linspace(0, 1, n_pts)
                    x_pts = (fx + dx * t).astype(np.float32)
                    y_pts = (fy + dy * t).astype(np.float32)

                    if self.human_jitter:
                        jx = self._noise_x.array(n_pts, freq=3.0, scale=0.8)
                        jy = self._noise_y.array(n_pts, freq=3.0, scale=0.8)
                        x_pts += jx.astype(np.float32)
                        y_pts += jy.astype(np.float32)

                    pts = np.stack([x_pts, y_pts], axis=1)

                    # Taper thickness
                    base_thick = 0.5 + darkness * 0.8
                    tap = np.sin(np.linspace(0, np.pi, n_pts))
                    thickness = (tap * base_thick).astype(np.float32)
                    thickness = np.clip(thickness, 0.3, 2.0)

                    strokes.append(Stroke(
                        points=pts, thickness=thickness,
                        darkness=darkness * 0.7,
                        layer=2, color=(30, 30, 30)
                    ))

        return strokes

    # ══════════════════════════════════════════════════════════════════════════
    # MATH / GEOMETRY HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    @staticmethod
    def _smooth_path(pts: np.ndarray, n_out: int = 80) -> Optional[np.ndarray]:
        """Smooth a polyline with a cubic spline."""
        if len(pts) < 4:
            return pts
        # Cumulative arc-length parameterization
        diffs = np.diff(pts, axis=0)
        dists = np.sqrt((diffs ** 2).sum(axis=1))
        dists = np.where(dists < 1e-6, 1e-6, dists)
        t     = np.concatenate([[0], np.cumsum(dists)])
        t     = t / t[-1]

        try:
            cs_x  = CubicSpline(t, pts[:, 0])
            cs_y  = CubicSpline(t, pts[:, 1])
            t_new = np.linspace(0, 1, min(n_out, len(pts) * 3))
            return np.stack([cs_x(t_new), cs_y(t_new)], axis=1).astype(np.float32)
        except Exception:
            return pts

    @staticmethod
    def _compute_pressure(
        pts: np.ndarray,
        gray: np.ndarray,
        thickness_range: Tuple[float, float],
    ) -> np.ndarray:
        """Sample image gradient magnitude to drive stroke thickness."""
        h, w = gray.shape
        # Gradient magnitude
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        mag = np.sqrt(gx ** 2 + gy ** 2)
        mag = cv2.normalize(mag, None, 0, 1, cv2.NORM_MINMAX)

        thickness = np.zeros(len(pts), dtype=np.float32)
        for i, (px, py) in enumerate(pts):
            xi, yi = int(np.clip(px, 0, w - 1)), int(np.clip(py, 0, h - 1))
            t = float(mag[yi, xi])
            lo, hi = thickness_range
            thickness[i] = lo + t * (hi - lo)

        # Taper at start and end (simulate pen pickup)
        n    = len(thickness)
        taper_len = max(1, n // 6)
        taper = np.ones(n)
        taper[:taper_len]   = np.linspace(0.1, 1.0, taper_len)
        taper[-taper_len:]  = np.linspace(1.0, 0.1, taper_len)
        return thickness * taper

    def _apply_jitter(self, pts: np.ndarray, magnitude: float = 1.5) -> np.ndarray:
        """Add smooth Perlin-like jitter to simulate hand tremor."""
        n  = len(pts)
        jx = self._noise_x.array(n, freq=2.0, scale=magnitude)
        jy = self._noise_y.array(n, freq=2.0, scale=magnitude)
        return pts + np.stack([jx, jy], axis=1).astype(np.float32)

    @staticmethod
    def _local_gradient_angle(patch: np.ndarray) -> float:
        """Dominant gradient direction in a patch (for shading alignment)."""
        if patch.size < 4:
            return np.pi / 4
        gx  = cv2.Sobel(patch.astype(np.float32), cv2.CV_32F, 1, 0)
        gy  = cv2.Sobel(patch.astype(np.float32), cv2.CV_32F, 0, 1)
        ang = np.arctan2(gy.mean(), gx.mean() + 1e-9)
        return float(ang + np.pi / 2)   # perpendicular to gradient = along edge

    def _stroke_color(self, layer: int) -> Tuple[int, int, int]:
        """Map layer index to stroke color based on style."""
        if self.style == "Charcoal":
            return [(10, 10, 15), (20, 20, 25), (35, 35, 40)][layer]
        if self.style in ("Watercolor", "Oil Painting", "Anime / Manga"):
            return [(15, 15, 15), (25, 25, 25), (40, 40, 40)][layer]
        return [(10, 10, 10), (20, 20, 20), (35, 35, 35)][layer]