# Quick Start Guide

## Installation

```bash
pip install ai-art-animator
```

## GUI Usage

Launch the graphical interface:

```bash
art-animator-gui
```

Then:
1. Click "Upload Image" to select your source image
2. Choose an art style from the dropdown
3. Adjust parameters (speed, detail, shading)
4. Click "Generate Art" to apply the style
5. Click "Create Animation" to render the video
6. Click "Export MP4" to save to your desired location

## CLI Usage

Basic command:

```bash
art-animator animate input.jpg -o output.mp4
```

With options:

```bash
art-animator animate input.jpg \
  --style "Pencil Sketch" \
  --speed 70 \
  --detail 80 \
  --fps 30 \
  --resolution 1920x1080 \
  --gif
```

## Python API

```python
from art_animator import ArtProcessor, ArtAnimator
from art_animator.utils import Logger
from PIL import Image

# Setup
logger = Logger()
processor = ArtProcessor(logger)
animator = ArtAnimator(logger)

# Apply style
styled = processor.apply_style(
    "input.jpg",
    style="Pencil Sketch",
    shading_intensity=0.6
)

# Create animation
output_path = animator.create_animation(
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

print(f"Animation saved: {output_path}")
```

## Next Steps

- Read the [User Guide](user-guide.md) for detailed feature documentation
- Check the [API Reference](api-reference.md) for programmatic usage
- See [Architecture](architecture.md) to understand the system design
