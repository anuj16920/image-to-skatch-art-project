# Complete Setup Guide

## For End Users

### Quick Install

```bash
pip install ai-art-animator
art-animator-gui
```

### From This Repository

```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI
python run_gui.py

# Or run CLI
python run_cli.py --help
```

## For Developers

### Initial Setup

**Linux/Mac:**
```bash
chmod +x scripts/install_dev.sh
./scripts/install_dev.sh
source venv/bin/activate
```

**Windows:**
```cmd
scripts\install_dev.bat
venv\Scripts\activate.bat
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=art_animator --cov-report=html

# Specific test
pytest tests/test_stroke_engine.py -v

# Watch mode (requires pytest-watch)
ptw tests/
```

### Code Quality

```bash
# Format code
black src/art_animator tests
isort src/art_animator tests

# Lint
flake8 src/art_animator tests

# Type check
mypy src/art_animator

# Or use Makefile
make format
make lint
make test
```

### Building Package

```bash
# Build distribution
python -m build

# Or use Makefile
make build
```

### Running Application

```bash
# GUI
art-animator-gui
# or
python run_gui.py

# CLI
art-animator animate input.jpg -o output.mp4
# or
python run_cli.py animate input.jpg -o output.mp4
```

## Docker Setup

### Build Image

```bash
docker build -t ai-art-animator .
```

### Run with Docker

```bash
# Create directories
mkdir inputs outputs

# Copy image to inputs/
cp your_image.jpg inputs/

# Run animation
docker run -v $(pwd)/inputs:/inputs -v $(pwd)/outputs:/outputs \
  ai-art-animator animate /inputs/your_image.jpg -o /outputs/animation.mp4
```

### Docker Compose

```bash
# Edit docker-compose.yml to set your input image
docker-compose up
```

## Project Commands

### Using Makefile

```bash
make install      # Install package
make dev          # Install with dev dependencies
make test         # Run tests with coverage
make lint         # Run linters
make format       # Format code
make clean        # Clean build artifacts
make build        # Build distribution
make docs         # Build documentation
make run-gui      # Launch GUI
make run-cli      # Show CLI help
```

### Manual Commands

```bash
# Install
pip install -e .

# Test
pytest tests/ -v --cov=art_animator

# Lint
flake8 src/art_animator tests
mypy src/art_animator

# Format
black src/art_animator tests
isort src/art_animator tests

# Build
python -m build

# Clean
rm -rf build/ dist/ *.egg-info __pycache__
```

## Troubleshooting

### Import Errors

```bash
# Ensure package is installed
pip install -e .

# Check Python path
python -c "import sys; print(sys.path)"
```

### FFmpeg Not Found

```bash
# Check FFmpeg installation
ffmpeg -version

# Install if missing (see docs/installation.md)
```

### Test Failures

```bash
# Run with verbose output
pytest tests/ -vv

# Run specific test
pytest tests/test_stroke_engine.py::TestStrokeEngine::test_initialization -v

# Show print statements
pytest tests/ -v -s
```

### GUI Won't Launch

```bash
# Check CustomTkinter
pip install --upgrade customtkinter

# Try from Python
python -c "from art_animator.gui.main import launch; launch()"
```

## Development Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes**
   - Write code in `src/art_animator/`
   - Add tests in `tests/`
   - Update docs if needed

3. **Run quality checks**
   ```bash
   make format
   make lint
   make test
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "Add my feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

## Configuration

### User Config

Create `~/.art_animator/config.yaml`:

```yaml
style:
  name: "Pencil Sketch"
  shading_intensity: 0.6

animation:
  speed: 50
  detail_level: 75
  fps: 30

output_dir: "~/MyAnimations"
log_level: "INFO"
```

### Project Config

Create `config/custom.yaml` in project root.

## Environment Variables

```bash
export OUTPUT_DIR=/path/to/outputs
export LOG_LEVEL=DEBUG
export MAX_WORKERS=8
```

## Performance Tuning

### For Faster Processing
- Lower detail level (50-60)
- Use 720p resolution
- Disable paper texture
- Enable time-lapse mode
- Increase max_workers

### For Higher Quality
- Increase detail level (85-95)
- Use 1080p or source resolution
- Enable paper texture
- Use 60 FPS
- Slower animation speed

## Next Steps

- Read [User Guide](docs/user-guide.md)
- Check [API Reference](docs/api-reference.md)
- See [Examples](examples/)
- Join [Discussions](https://github.com/yourusername/ai-art-animator/discussions)
