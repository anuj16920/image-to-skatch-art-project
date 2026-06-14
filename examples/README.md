# Examples

This directory contains example scripts demonstrating various features of AI Art Animator.

## Available Examples

### basic_usage.py
Simple example showing core functionality:
- Apply artistic style
- Create animation
- Save output

```bash
python examples/basic_usage.py
```

### batch_processing.py
Process multiple images in parallel:
- Batch processing workflow
- ThreadPoolExecutor usage
- Progress tracking

```bash
python examples/batch_processing.py input_dir/ output_dir/ 4
```

### config_usage.py
Configuration file management:
- Create Config objects
- Save/load YAML files
- Validation

```bash
python examples/config_usage.py
```

### custom_style.py
Create custom artistic styles:
- Inherit from BaseStyleProcessor
- Register with decorator
- Use StyleRegistry

```bash
python examples/custom_style.py
```

## Running Examples

Ensure the package is installed:

```bash
pip install -e .
```

Then run any example:

```bash
python examples/basic_usage.py
```

## Creating Your Own Examples

1. Import from `art_animator` package
2. Use proper type hints
3. Add error handling
4. Document your code
5. Share via pull request!

## Sample Images

For testing, you can use:
- Your own photos
- Free stock images from Unsplash/Pexels
- Test images from `tests/fixtures/` (if available)

## Need Help?

- Check [User Guide](../docs/user-guide.md)
- See [API Reference](../docs/api-reference.md)
- Open an [Issue](https://github.com/yourusername/ai-art-animator/issues)
