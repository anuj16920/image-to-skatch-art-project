# Test Suite

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### With Coverage
```bash
pytest tests/ --cov=art_animator --cov-report=html
```

### Specific Test File
```bash
pytest tests/test_stroke_engine.py -v
```

### Specific Test
```bash
pytest tests/test_stroke_engine.py::TestStrokeEngine::test_initialization -v
```

## Test Structure

- `conftest.py`: Shared fixtures and configuration
- `test_animator.py`: Animation engine tests
- `test_art_processor.py`: Style processing tests
- `test_config.py`: Configuration management tests
- `test_image_utils.py`: Image utility tests
- `test_logger.py`: Logging system tests
- `test_stroke_engine.py`: Stroke extraction tests

## Writing Tests

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Using Fixtures

```python
def test_something(logger, test_image_bgr):
    # logger and test_image_bgr are fixtures from conftest.py
    processor = ArtProcessor(logger)
    result = processor.process(test_image_bgr)
    assert result is not None
```

### Adding New Tests

1. Create test file in `tests/`
2. Import module to test
3. Write test class and methods
4. Use fixtures from `conftest.py`
5. Run tests to verify

## Coverage Goals

- Overall coverage: > 80%
- Core modules: > 90%
- Utilities: > 85%

## Continuous Integration

Tests run automatically on:
- Every push to main/develop
- Every pull request
- Multiple Python versions (3.9, 3.10, 3.11)
- Multiple OS (Ubuntu, Windows, macOS)

See `.github/workflows/ci.yml` for details.
