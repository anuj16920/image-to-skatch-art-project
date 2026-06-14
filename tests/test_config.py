"""Tests for configuration management."""

import pytest
from pathlib import Path
from art_animator.config.settings import Config, StyleConfig, AnimationConfig


class TestStyleConfig:
    """Test style configuration."""
    
    def test_defaults(self):
        """Test default values."""
        config = StyleConfig()
        assert config.name == "Pencil Sketch"
        assert config.shading_intensity == 0.6
    
    def test_validation_valid(self):
        """Test validation with valid values."""
        config = StyleConfig(shading_intensity=0.5)
        config.validate()  # Should not raise
    
    def test_validation_invalid(self):
        """Test validation with invalid values."""
        config = StyleConfig(shading_intensity=1.5)
        with pytest.raises(ValueError):
            config.validate()


class TestAnimationConfig:
    """Test animation configuration."""
    
    def test_defaults(self):
        """Test default values."""
        config = AnimationConfig()
        assert config.speed == 50
        assert config.detail_level == 75
        assert config.fps == 30
    
    def test_validation_valid(self):
        """Test validation with valid values."""
        config = AnimationConfig(speed=50, detail_level=75, fps=30)
        config.validate()
    
    def test_validation_invalid_speed(self):
        """Test validation with invalid speed."""
        config = AnimationConfig(speed=150)
        with pytest.raises(ValueError):
            config.validate()
