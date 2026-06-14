"""Tests for stroke engine."""

import pytest
import numpy as np
import cv2
from art_animator.core.stroke_engine import StrokeEngine, Stroke, StrokeLayer, SmoothNoise


class TestSmoothNoise:
    """Test smooth noise generator."""
    
    def test_initialization(self):
        """Test noise generator initialization."""
        noise = SmoothNoise(seed=42)
        assert noise._base.shape == (4096,)
        assert noise._base.min() >= -1
        assert noise._base.max() <= 1
    
    def test_call(self):
        """Test single noise value generation."""
        noise = SmoothNoise(seed=42)
        val = noise(0.5, freq=1.0)
        assert -1 <= val <= 1
    
    def test_array(self):
        """Test noise array generation."""
        noise = SmoothNoise(seed=42)
        arr = noise.array(100, freq=1.0, scale=2.0)
        assert arr.shape == (100,)
        assert arr.min() >= -2
        assert arr.max() <= 2


class TestStrokeEngine:
    """Test stroke engine."""
    
    @pytest.fixture
    def engine(self):
        """Create stroke engine instance."""
        return StrokeEngine(detail_level=50, human_jitter=True)
    
    @pytest.fixture
    def test_image(self):
        """Create test image."""
        img = np.ones((200, 200, 3), dtype=np.uint8) * 255
        cv2.rectangle(img, (50, 50), (150, 150), (0, 0, 0), 2)
        cv2.circle(img, (100, 100), 30, (0, 0, 0), 2)
        return img
    
    def test_initialization(self, engine):
        """Test engine initialization."""
        assert engine.detail_level == 0.5
        assert engine.human_jitter is True
        assert engine.style == "Pencil Sketch"
    
    def test_extract_stroke_layers(self, engine, test_image):
        """Test stroke layer extraction."""
        layers = engine.extract_stroke_layers(test_image, test_image)
        
        assert len(layers) == 3
        assert layers[0].name == "outline"
        assert layers[1].name == "detail"
        assert layers[2].name == "shading"
        
        # Should have some strokes
        total_strokes = sum(len(layer.strokes) for layer in layers)
        assert total_strokes > 0
    
    def test_smooth_path(self):
        """Test path smoothing."""
        pts = np.array([[0, 0], [10, 10], [20, 5], [30, 15]], dtype=np.float32)
        smoothed = StrokeEngine._smooth_path(pts, n_out=20)
        
        assert smoothed is not None
        assert len(smoothed) >= len(pts)
    
    def test_compute_pressure(self):
        """Test pressure computation."""
        gray = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        pts = np.array([[10, 10], [20, 20], [30, 30]], dtype=np.float32)
        
        thickness = StrokeEngine._compute_pressure(pts, gray, (1.0, 3.0))
        
        assert thickness.shape == (3,)
        assert thickness.min() >= 0
        assert thickness.max() <= 3.0
    
    def test_local_gradient_angle(self):
        """Test gradient angle computation."""
        patch = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
        angle = StrokeEngine._local_gradient_angle(patch)
        
        assert isinstance(angle, float)
        assert -np.pi <= angle <= np.pi


class TestStroke:
    """Test Stroke dataclass."""
    
    def test_creation(self):
        """Test stroke creation."""
        pts = np.array([[0, 0], [10, 10]], dtype=np.float32)
        thickness = np.array([1.0, 2.0], dtype=np.float32)
        
        stroke = Stroke(points=pts, thickness=thickness)
        
        assert stroke.points.shape == (2, 2)
        assert stroke.thickness.shape == (2,)
        assert stroke.darkness == 0.85
        assert stroke.layer == 0
        assert stroke.color == (20, 20, 20)


class TestStrokeLayer:
    """Test StrokeLayer dataclass."""
    
    def test_creation(self):
        """Test layer creation."""
        layer = StrokeLayer(name="test")
        
        assert layer.name == "test"
        assert layer.strokes == []
    
    def test_add_strokes(self):
        """Test adding strokes to layer."""
        layer = StrokeLayer(name="test")
        pts = np.array([[0, 0], [10, 10]], dtype=np.float32)
        thickness = np.array([1.0, 2.0], dtype=np.float32)
        stroke = Stroke(points=pts, thickness=thickness)
        
        layer.strokes.append(stroke)
        
        assert len(layer.strokes) == 1
        assert layer.strokes[0] == stroke
