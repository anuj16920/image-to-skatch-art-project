"""Tests for animator."""

import pytest
import numpy as np
from PIL import Image
from pathlib import Path

from art_animator.core.animator import ArtAnimator
from art_animator.core.stroke_engine import Stroke, StrokeLayer


class TestArtAnimator:
    """Test art animator."""
    
    @pytest.fixture
    def animator(self, logger, tmp_path):
        """Create animator instance."""
        return ArtAnimator(logger, output_dir=tmp_path)
    
    def test_initialization(self, animator, tmp_path):
        """Test animator initialization."""
        assert animator.OUTPUT_DIR == tmp_path
        assert animator.OUTPUT_DIR.exists()
    
    def test_compose_frame(self, animator):
        """Test frame composition."""
        canvas = np.ones((100, 100, 3), dtype=np.float32) * 200
        bg_texture = np.ones((100, 100, 3), dtype=np.uint8) * 255
        styled = np.ones((100, 100, 3), dtype=np.uint8) * 128
        
        frame = animator._compose_frame(
            canvas, bg_texture, True, styled, 0, 3, 0.5
        )
        
        assert frame.shape == (100, 100, 3)
        assert frame.dtype == np.uint8
    
    def test_render_stroke(self, animator):
        """Test stroke rendering."""
        canvas = np.ones((100, 100, 3), dtype=np.float32) * 255
        
        pts = np.array([[10, 10], [50, 50], [90, 90]], dtype=np.float32)
        thickness = np.array([2.0, 2.0, 2.0], dtype=np.float32)
        stroke = Stroke(points=pts, thickness=thickness)
        
        animator._render_stroke(canvas, stroke, 100, 100, 100, 100)
        
        # Canvas should be modified
        assert not np.all(canvas == 255)
