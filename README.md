# 🎨 AI Art Animator.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Professional stroke-level drawing animation system** that converts static images into realistic "artist drawing" videos..

## ✨ Features

- **6 Artistic Styles**: Pencil Sketch, Advanced Sketch, Watercolor, Oil Painting, Charcoal, Anime/Manga
- **Realistic Stroke Simulation**: Multi-layer rendering with human-like jitter and pressure variation
- **Dual Interface**: Modern GUI and powerful CLI
- **Extensive Customization**: Speed, detail level, shading, resolution, FPS
- **Multiple Export Formats**: MP4 (H.264), GIF, image sequences
- **Paper Textures**: 5 background types with procedural generation
- **Professional Architecture**: Modular, extensible, well-documented

## 🚀 Quick Start

### Installation

```bash
pip install ai-art-animator
```

### GUI Usage

```bash
art-animator-gui
```

### CLI Usage

```bash
art-animator animate input.jpg -o output.mp4 --style "Pencil Sketch"
```

### Python API

```python
from art_animator import ArtProcessor, ArtAnimator
from art_animator.utils import Logger

logger = Logger()
processor = ArtProcessor(logger)
animator = ArtAnimator(logger)

# Apply style
styled = processor.apply_style("input.jpg", style="Pencil Sketch")

# Create animation
output = animator.create_animation(
    styled_image=styled,
    source_path="input.jpg",
    style="Pencil Sketch",
    speed=50,
    detail_level=75,
    fps=30,
    resolution=(1920, 1080),
    paper_texture=True,
    human_jitter=True,
    timelapse=False,
    export_gif=False,
    bg_type="White Paper",
    progress_cb=lambda v, l: print(f"{v*100:.0f}%"),
    preview_cb=lambda f: None,
)
```

## 📋 Requirements

- Python 3.9+
- OpenCV 4.8+
- NumPy 1.24+
- Pillow 10.0+
- CustomTkinter 5.2+ (for GUI)
- FFmpeg (for video encoding)

## 🏗️ Architecture

```
src/art_animator/
├── core/              # Core animation engine
│   ├── animator.py    # Frame-by-frame rendering
│   ├── stroke_engine.py  # Stroke extraction
│   └── art_processor.py  # Style processing
├── styles/            # Style system
│   ├── base.py        # Base style class
│   └── registry.py    # Style registry
├── gui/               # GUI application
│   └── main.py        # CustomTkinter interface
├── utils/             # Utilities
│   ├── logger.py      # Logging system
│   ├── image_utils.py # Image processing
│   └── texture_generator.py  # Paper textures
├── config/            # Configuration
│   └── settings.py    # Config management
└── cli.py             # Command-line interface
```

## 🎯 Use Cases

- Create time-lapse drawing videos for social media
- Generate artistic animations from photos
- Educational content showing drawing process
- Portfolio presentations
- Art style exploration and experimentation

## 📖 Documentation

Full documentation available in the [docs/](docs/) directory:

- [Installation Guide](docs/installation.md)
- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Architecture Overview](docs/architecture.md)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- OpenCV for image processing
- CustomTkinter for modern GUI
- NumPy/SciPy for numerical operations
- FFmpeg for video encoding

## 📧 Contact

- Issues: [GitHub Issues](https://github.com/yourusername/ai-art-animator/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/ai-art-animator/discussions)

---

Made with ❤️ by the AI Art Animator Team
