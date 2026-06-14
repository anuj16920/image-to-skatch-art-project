"""
Stroke Engine — The heart of the realistic drawing simulation.

Algorithm:
  1. Multi-scale Canny edge detection → contour map
  2. Contour extraction + hierarchical ordering (outer → inner)
  3. Stroke path simulation with:
       • Catmull-Rom spline smoothing
       • Variable pressure (thickness) via intensity map
       • Human-like jitter (Perlin-style noise)
       • Layer system: rough outline → mid details → fine shading
  4. Shading pass using adaptive stroke density from grayscale luminance
"""

from __future__ import annotations
import cv2
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from scipy.interpolate import CubicSpline


@dataclass
class Stroke:
    """
    A single stroke: a sequence of (x,y) points with per-point attributes.
    
    Attributes:
        points: Array of (x, y) coordinates, shape (N, 2), dtype float32
        thickness: Per-point thickness values, shape (N,), dtype float32
        darkness: Opacity/intensity (0=white, 1=black)
        layer: Drawing layer (0=outline, 1=detail, 2=shading)
        color: RGB color tuple
    """
    points: np.ndarray
    thickness: np.ndarray
    darkness: float = 0.85
    layer: int = 0
    color: Tuple[int, int, int] = (20, 20, 20)


@dataclass
class StrokeLayer:
    """
    Collection of strokes belonging to the same drawing phase.
    
    Attributes:
        name: Layer name (e.g., "outline", "detail", "shading")
        strokes: List of Stroke objects
    """
    name: str
    strokes: List[Stroke] = field(default_factory=list)


class SmoothNoise:
    """
    Fast 1-D smooth noise generator via cosine interpolation.
    
    Used to simulate natural hand tremor in stroke paths.
    """

    def __init__(self, seed: int = 0):
        """
        Initialize noise generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        rng = np.random.default_rng(seed)
        self._base = rng.uniform(-1, 1, 4096)

    def __call__(self, t: float, freq: float = 1.0) -> float:
        """
        Sample noise at time t.
        
        Args:
            t: Time parameter
            freq: Frequency multiplier
            
        Returns:
            Noise value in range [-1, 1]
        """
        idx = (t * freq) % len(self._base)
        i = int(idx)
        f = idx - i
        v0 = self._base[i % len(self._base)]
        v1 = self._base[(i + 1) % len(self._base)]
        ft = (1.0 - np.cos(f * np.pi)) * 0.5
        return v0 * (1 - ft) + v1 * ft

    def array(self, n: int, freq: float = 1.0, scale: float = 1.0) -> np.ndarray:
        """
        Generate array of noise values.
        
        Args:
            n: Number of samples
            freq: Frequency multiplier
            scale: Amplitude multiplier
            
        Returns:
            Array of noise values
        """
        t = np.linspace(0, n / 20.0, n)
        return np.array([self(ti, freq) for ti in t]) * scale


class StrokeEngine:
    """
    Core engine for extracting realistic drawing strokes from images.
    
    Converts raster images into ordered sequences of vector strokes that
    simulate how an artist would draw the image by hand.
    """

    def __init__(
        self,
        detail_level: int = 75,
        human_jitter: bool = True,
        style: str = "Pencil Sketch",
    ):
        """
        Initialize stroke engine.
        
        Args:
            detail_level: Stroke density (10-100, higher = more strokes)
            human_jitter: Enable natural hand tremor simulation
            style: Art style name (affects stroke colors)
        """
        self.detail_level = detail_level / 100.0
        self.human_jitter = human_jitter
        self.style = style
        self._noise_x = SmoothNoise(seed=3)
        self._noise_y = SmoothNoise(seed=7)
        self._noise_p = SmoothNoise(seed=11)

    def extract_stroke_layers(
        self,
        source_bgr: np.ndarray,
        styled_bgr: np.ndarray,
    ) -> List[StrokeLayer]:
        """
        Extract ordered stroke layers from images.
        
        Args:
            source_bgr: Original image in BGR format
            styled_bgr: Styled image in BGR format
            
        Returns:
            List of three StrokeLayer objects:
                - Layer 0: Rough outline (main contours)
                - Layer 1: Mid details (secondary edges)
                - Layer 2: Fine shading (tonal hatching)
        """
        gray = cv2.cvtColor(source_bgr, cv2.COLOR_BGR2GRAY)
        styled_gray = cv2.cvtColor(styled_bgr, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        layers = []

        # Layer 0: Main contours
        outline_layer = StrokeLayer("outline")
        edges_coarse = cv2.Canny(cv2.GaussianBlur(gray, (5, 5), 0), 20, 60)
        contours, hierarchy = cv2.findContours(
            edges_coarse, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS
        )
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        max_contours = max(10, int(len(contours) * 0.3 * self.detail_level))
        
        for cnt in contours[:max_contours]:
            if cv2.contourArea(cnt) < 30:
                continue
            stroke = self._contour_to_stroke(cnt, gray, layer=0, thickness_range=(1.8, 3.5))
            if stroke:
                outline_layer.strokes.append(stroke)
        layers.append(outline_layer)

        # Layer 1: Detail edges
        detail_layer = StrokeLayer("detail")
        edges_fine = cv2.Canny(gray, 40, 120)
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

        # Layer 2: Tonal shading
        shade_layer = StrokeLayer("shading")
        shade_strokes = self._generate_shading_strokes(styled_gray, source_bgr)
        shade_layer.strokes = shade_strokes
        layers.append(shade_layer)

        return layers

    def _contour_to_stroke(
        self,
        contour: np.ndarray,
        gray: np.ndarray,
        layer: int,
        thickness_range: Tuple[float, float] = (1.0, 2.5),
    ) -> Optional[Stroke]:
        """
        Convert OpenCV contour to smooth, jittered Stroke.
        
        Args:
            contour: OpenCV contour array
            gray: Grayscale image for pressure computation
            layer: Layer index (0, 1, or 2)
            thickness_range: Min and max thickness values
            
        Returns:
            Stroke object or None if contour is too small
        """
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

        # Pressure from local image gradient
        thickness = self._compute_pressure(pts, gray, thickness_range)

        # Human jitter
        if self.human_jitter:
            pts = self._apply_jitter(pts, magnitude=1.2)

        color = self._stroke_color(layer)
        darkness = np.clip(0.6 + layer * 0.1, 0, 1.0)

        return Stroke(
            points=pts,
            thickness=thickness,
            darkness=darkness,
            layer=layer,
            color=color
        )

    def _generate_shading_strokes(
        self,
        gray: np.ndarray,
        source_bgr: np.ndarray,
    ) -> List[Stroke]:
        """
        Generate hatching/cross-hatching strokes in dark areas.
        
        Stroke density is proportional to local darkness.
        
        Args:
            gray: Grayscale image
            source_bgr: Original BGR image
            
        Returns:
            List of shading strokes
        """
        h, w = gray.shape
        strokes: List[Stroke] = []

        # Downsample for speed
        scale = min(1.0, 600 / max(h, w))
        gh, gw = int(h * scale), int(w * scale)
        small = cv2.resize(gray, (gw, gh), interpolation=cv2.INTER_AREA)

        # Grid-based shading
        cell = max(12, int(min(gh, gw) / 40))
        rng = np.random.default_rng(42)

        for gy in range(0, gh - cell, cell):
            for gx in range(0, gw - cell, cell):
                patch = small[gy:gy + cell, gx:gx + cell]
                lum = patch.mean() / 255.0
                darkness = 1.0 - lum

                if darkness < 0.15:
                    continue

                n_strokes = int(darkness * self.detail_level * 4)
                if n_strokes < 1:
                    continue

                # Hatch direction from gradient
                patch_big = gray[
                    int(gy / scale):int((gy + cell) / scale),
                    int(gx / scale):int((gx + cell) / scale)
                ]
                angle = self._local_gradient_angle(patch_big)

                for si in range(n_strokes):
                    fx = int(gx / scale) + rng.integers(0, int(cell / scale))
                    fy = int(gy / scale) + rng.integers(0, int(cell / scale))
                    length = rng.integers(8, max(9, int(30 * darkness * self.detail_level)))

                    jitter_angle = angle + rng.uniform(-0.25, 0.25)
                    dx = np.cos(jitter_angle) * length
                    dy = np.sin(jitter_angle) * length

                    n_pts = max(4, length // 4)
                    t = np.linspace(0, 1, n_pts)
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
                        points=pts,
                        thickness=thickness,
                        darkness=darkness * 0.7,
                        layer=2,
                        color=(30, 30, 30)
                    ))

        return strokes

    @staticmethod
    def _smooth_path(pts: np.ndarray, n_out: int = 80) -> Optional[np.ndarray]:
        """
        Smooth polyline with cubic spline.
        
        Args:
            pts: Input points, shape (N, 2)
            n_out: Number of output points
            
        Returns:
            Smoothed points or None if smoothing fails
        """
        if len(pts) < 4:
            return pts
        
        # Arc-length parameterization
        diffs = np.diff(pts, axis=0)
        dists = np.sqrt((diffs ** 2).sum(axis=1))
        dists = np.where(dists < 1e-6, 1e-6, dists)
        t = np.concatenate([[0], np.cumsum(dists)])
        t = t / t[-1]

        try:
            cs_x = CubicSpline(t, pts[:, 0])
            cs_y = CubicSpline(t, pts[:, 1])
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
        """
        Compute stroke thickness from image gradient magnitude.
        
        Args:
            pts: Stroke points
            gray: Grayscale image
            thickness_range: (min_thickness, max_thickness)
            
        Returns:
            Per-point thickness array
        """
        h, w = gray.shape
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

        # Taper at start/end (pen pickup simulation)
        n = len(thickness)
        taper_len = max(1, n // 6)
        taper = np.ones(n)
        taper[:taper_len] = np.linspace(0.1, 1.0, taper_len)
        taper[-taper_len:] = np.linspace(1.0, 0.1, taper_len)
        return thickness * taper

    def _apply_jitter(self, pts: np.ndarray, magnitude: float = 1.5) -> np.ndarray:
        """
        Add smooth Perlin-like jitter to simulate hand tremor.
        
        Args:
            pts: Input points
            magnitude: Jitter amplitude in pixels
            
        Returns:
            Jittered points
        """
        n = len(pts)
        jx = self._noise_x.array(n, freq=2.0, scale=magnitude)
        jy = self._noise_y.array(n, freq=2.0, scale=magnitude)
        return pts + np.stack([jx, jy], axis=1).astype(np.float32)

    @staticmethod
    def _local_gradient_angle(patch: np.ndarray) -> float:
        """
        Compute dominant gradient direction in image patch.
        
        Used for aligning shading strokes with image structure.
        
        Args:
            patch: Grayscale image patch
            
        Returns:
            Angle in radians
        """
        if patch.size < 4:
            return np.pi / 4
        gx = cv2.Sobel(patch.astype(np.float32), cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(patch.astype(np.float32), cv2.CV_32F, 0, 1)
        ang = np.arctan2(gy.mean(), gx.mean() + 1e-9)
        return float(ang + np.pi / 2)

    def _stroke_color(self, layer: int) -> Tuple[int, int, int]:
        """
        Map layer index to stroke color based on style.
        
        Args:
            layer: Layer index (0, 1, or 2)
            
        Returns:
            RGB color tuple
        """
        if self.style == "Charcoal":
            return [(10, 10, 15), (20, 20, 25), (35, 35, 40)][layer]
        if self.style in ("Watercolor", "Oil Painting", "Anime / Manga"):
            return [(15, 15, 15), (25, 25, 25), (40, 40, 40)][layer]
        return [(10, 10, 10), (20, 20, 20), (35, 35, 35)][layer]
