"""Tests for logger."""

import pytest
from pathlib import Path
from art_animator.utils.logger import Logger


class TestLogger:
    """Test logger functionality."""
    
    def test_initialization(self):
        """Test logger initialization."""
        logger = Logger(name="TestLogger", level="INFO")
        assert logger.name == "TestLogger"
    
    def test_log_levels(self):
        """Test different log levels."""
        logger = Logger(level="DEBUG")
        
        # Should not raise
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_callback(self):
        """Test callback functionality."""
        messages = []
        
        def callback(msg):
            messages.append(msg)
        
        logger = Logger()
        logger.callback = callback
        logger.info("Test message")
        
        assert len(messages) == 1
        assert "Test message" in messages[0]
    
    def test_file_logging(self, tmp_path):
        """Test logging to file."""
        log_file = tmp_path / "test.log"
        logger = Logger(log_file=log_file)
        logger.info("Test message")
        
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content
