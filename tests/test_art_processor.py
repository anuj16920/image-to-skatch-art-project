"""Tests for art processor."""

import pytest
import numpy as np
from art_animator.core.art_processor import ArtProcessor


class TestArtProcessor:
    """Test art processor."""
    
    @pytest.fixture
    def processor(self, logger):
        """Create processor instance."""
        return ArtProcessor(logger)
    
    def test_initialization(self, processor):
        """Test processor initialization."""
        assert processor.logger is not None
    
    def test_apply_style_invalid_path(self, processor):
        """Test with invalid image path."""
        with pytest.raises(ValueError):
            processor.apply_style("nonexistent.jpg", "Pencil Sketch")
    
    def test_apply_style_invalid_style(self, processor, temp_image_path):
        """Test with invalid style name."""
        with pytest.raises(KeyError):
            processor.apply_style(temp_image_path, "Invalid Style")
    
    def test_pencil_sketch(self, processor, test_image_bgr):
        """Test pencil sketch style."""
        result = processor._pencil_sketch(test_image_bgr, 0.6)
        assert result.shape == test_image_bgr.shape
        assert result.dtype == np.uint8
    
    def test_watercolor(self, processor, test_image_bgr):
        """Test watercolor style."""
        result = processor._watercolor(test_image_bgr, 0.6)
        assert result.shape == test_image_bgr.shape
        assert result.dtype == np.uint8
    
    def test_charcoal(self, processor, test_image_bgr):
        """Test charcoal style."""
        result = processor._charcoal(test_image_bgr, 0.6)
        assert result.shape == test_image_bgr.shape
        assert result.dtype == np.uint8
