"""Pytest configuration and fixtures."""

import pytest
import numpy as np
import cv2
from pathlib import Path
from PIL import Image

from art_animator.utils.logger import Logger


@pytest.fixture
def logger():
    """Create logger instance for tests."""
    return Logger(name="TestLogger", level="DEBUG")


@pytest.fixture
def test_image_bgr():
    """Create test BGR image with simple shapes."""
    img = np.ones((200, 200, 3), dtype=np.uint8) * 255
    cv2.rectangle(img, (50, 50), (150, 150), (0, 0, 0), 2)
    cv2.circle(img, (100, 100), 30, (0, 0, 0), 2)
    return img


@pytest.fixture
def test_image_pil():
    """Create test PIL image."""
    return Image.new('RGB', (200, 200), color=(255, 255, 255))


@pytest.fixture
def temp_image_path(tmp_path, test_image_pil):
    """Create temporary image file."""
    path = tmp_path / "test_image.jpg"
    test_image_pil.save(path)
    return str(path)
