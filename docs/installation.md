# Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager
- FFmpeg (for video encoding)

## Installing FFmpeg

### Windows
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Chocolatey:
```bash
choco install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## Installation Methods

### Method 1: From PyPI (Recommended)

```bash
pip install ai-art-animator
```

### Method 2: From Source

```bash
git clone https://github.com/yourusername/ai-art-animator.git
cd ai-art-animator
pip install -e .
```

### Method 3: Development Installation

For contributors:

```bash
git clone https://github.com/yourusername/ai-art-animator.git
cd ai-art-animator
pip install -e ".[dev]"
pre-commit install
```

## Docker Installation

### Build Image

```bash
docker build -t ai-art-animator .
```

### Run Container

```bash
docker run -v $(pwd)/inputs:/inputs -v $(pwd)/outputs:/outputs \
  ai-art-animator animate /inputs/photo.jpg -o /outputs/animation.mp4
```

### Docker Compose

```bash
docker-compose up
```

## Verifying Installation

### Check CLI

```bash
art-animator --version
```

### Check GUI

```bash
art-animator-gui
```

### Run Tests

```bash
pytest tests/
```

## Troubleshooting

### Import Errors

If you get import errors, ensure the package is installed:
```bash
pip install -e .
```

### FFmpeg Not Found

Ensure FFmpeg is in your PATH:
```bash
ffmpeg -version
```

### OpenCV Issues

On some systems, you may need:
```bash
pip install opencv-python-headless
```

### GUI Not Launching

Ensure CustomTkinter is installed:
```bash
pip install customtkinter
```

## Virtual Environment (Recommended)

Create isolated environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install ai-art-animator
```

## Upgrading

```bash
pip install --upgrade ai-art-animator
```

## Uninstalling

```bash
pip uninstall ai-art-animator
```
