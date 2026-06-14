"""Tests for image utilities."""

import pytest
import numpy as np
from PIL import Image
import cv2
from art_animator.utils.image_utils import (
    pil_to_cv2,
    cv2_to_pil,
    resize_for_processing,
)


class TestImageConversion:
    """Test image format conversion."""
    
    def test_pil_to_cv2(self):
        """Test PIL to OpenCV conversion."""
        pil_img = Image.new('RGB', (100, 100), color=(255, 0, 0))
        cv2_img = pil_to_cv2(pil_img)
        
        assert cv2_img.shape == (100, 100, 3)
        assert cv2_img.dtype == np.uint8
        # Red in RGB becomes Blue in BGR
        assert cv2_img[0, 0, 2] == 255
    
    def test_cv2_to_pil(self):
        """Test OpenCV to PIL conversion."""
        cv2_img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2_img[:, :, 0] = 255  # Blue channel
        
        pil_img = cv2_to_pil(cv2_img)
        
        assert pil_img.size == (100, 100)
        # Blue in BGR becomes Red in RGB
        assert pil_img.getpixel((0, 0))[2] == 255


class TestResize:
    """Test image resizing."""
    
    def test_resize_large_image(self):
        """Test resizing image larger than max_dim."""
        img = np.zeros((2000, 1500, 3), dtype=np.uint8)
        resized, scale = resize_for_processing(img, max_dim=1000)
        
        assert max(resized.shape[:2]) <= 1000
        assert scale < 1.0
    
    def test_resize_small_image(self):
        """Test that small images are not upscaled."""
        img = np.zeros((500, 400, 3), dtype=np.uint8)
        resized, scale = resize_for_processing(img, max_dim=1000)
        
        assert resized.shape == img.shape
        assert scale == 1.0
