# Contributing Guide

See [CONTRIBUTING.md](../CONTRIBUTING.md) in the root directory.

## Development Workflow

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Run quality checks
5. Submit pull request

## Code Quality Standards

- Type hints required
- Docstrings for all public APIs
- Test coverage > 80%
- Pass all linters (black, flake8, mypy)
- Follow PEP 8 guidelines

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=art_animator --cov-report=html

# Specific test file
pytest tests/test_stroke_engine.py -v
```

## Documentation

Update documentation when adding features:
- API reference for new classes/functions
- User guide for new features
- Examples for common use cases
