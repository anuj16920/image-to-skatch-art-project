# Contributing to AI Art Animator

Thank you for your interest in contributing!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-art-animator.git
cd ai-art-animator
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for all public APIs (Google style)
- Keep line length under 100 characters
- Run `black` and `isort` before committing

## Testing

Run tests:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=art_animator --cov-report=html
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Run linters: `make lint`
6. Format code: `make format`
7. Commit with clear messages
8. Push and create a pull request

## Adding New Styles

To add a new artistic style:

1. Create a new class in `src/art_animator/styles/`
2. Inherit from `BaseStyleProcessor`
3. Implement the `process()` method
4. Register with `@register_style("Style Name")`
5. Add tests in `tests/test_styles.py`

## Reporting Issues

- Use GitHub Issues
- Include Python version, OS, and error messages
- Provide minimal reproducible examples
- Attach sample images if relevant

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.
