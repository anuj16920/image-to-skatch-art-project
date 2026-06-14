# User Guide

## Installation

### From PyPI

```bash
pip install ai-art-animator
```

### From Source

```bash
git clone https://github.com/yourusername/ai-art-animator.git
cd ai-art-animator
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## GUI Application

### Launching

```bash
art-animator-gui
```

### Workflow

1. **Upload Image**: Click "Upload Image" and select your source photo
2. **Choose Style**: Select from 6 artistic styles
3. **Adjust Parameters**:
   - Drawing Speed: How fast strokes are drawn (1-100)
   - Detail Level: Number of strokes (10-100)
   - Shading Intensity: Darkness of shading (0-100%)
   - Frame Rate: 24, 30, or 60 FPS
   - Resolution: 720p, 1080p, or source size
4. **Generate Art**: Apply the artistic style
5. **Create Animation**: Render the drawing video
6. **Export**: Save to your desired location

### Advanced Options

- **Paper Texture Overlay**: Adds realistic paper grain
- **Human Stroke Jitter**: Simulates hand tremor
- **Time-lapse Mode**: 6x faster animation
- **Export GIF**: Also save as animated GIF

## Command-Line Interface

### Basic Usage

```bash
art-animator animate input.jpg -o output.mp4
```

### Common Examples

**High-quality pencil sketch:**
```bash
art-animator animate photo.jpg \
  --style "Pencil Sketch" \
  --detail 90 \
  --speed 40 \
  --fps 60 \
  --resolution 1920x1080
```

**Fast watercolor animation:**
```bash
art-animator animate photo.jpg \
  --style "Watercolor" \
  --speed 80 \
  --timelapse \
  --gif
```

**Charcoal with dark canvas:**
```bash
art-animator animate photo.jpg \
  --style "Charcoal" \
  --background "Dark Canvas" \
  --shading 0.8
```

## Configuration Files

Create a config file for reusable settings:

```yaml
# my-config.yaml
style:
  name: "Pencil Sketch"
  shading_intensity: 0.7

animation:
  speed: 60
  detail_level: 85
  fps: 30
  resolution: [1920, 1080]
  paper_texture: true
  human_jitter: true
```

Validate configuration:
```bash
art-animator validate-config my-config.yaml
```

## Parameter Guide

### Speed (1-100)
- **1-30**: Slow, meditative drawing
- **31-70**: Medium pace (default: 50)
- **71-100**: Fast, energetic strokes

### Detail Level (10-100)
- **10-35**: Minimal, loose sketch
- **36-65**: Balanced detail
- **66-100**: High detail, many strokes (default: 75)

### Shading Intensity (0.0-1.0)
- **0.0-0.3**: Light, subtle shading
- **0.4-0.7**: Moderate shading (default: 0.6)
- **0.8-1.0**: Heavy, dramatic shading

### Frame Rate
- **24 FPS**: Cinematic feel
- **30 FPS**: Standard video (default)
- **60 FPS**: Smooth, high-quality

### Resolution
- **720p**: 1280×720 (faster processing)
- **1080p**: 1920×1080 (default)
- **Source Size**: Match input image

## Background Types

- **White Paper**: Clean white with subtle texture (default)
- **Aged Paper**: Yellowed vintage look
- **Dark Canvas**: Grainy dark background
- **Pure White**: Solid white, no texture
- **Pure Black**: Solid black, no texture

## Tips & Best Practices

### For Best Results

1. **Image Quality**: Use high-resolution source images (1000px+)
2. **Subject Matter**: Clear subjects with defined edges work best
3. **Lighting**: Well-lit photos produce better edge detection
4. **Detail Level**: Start at 75, adjust based on image complexity
5. **Speed**: Use slower speeds for detailed images

### Performance Optimization

- Lower detail level for faster processing
- Use 720p for quick previews
- Enable time-lapse mode for long animations
- Disable paper texture for faster rendering

### Artistic Choices

- **Portraits**: Pencil Sketch or Charcoal at detail 80+
- **Landscapes**: Watercolor or Oil Painting at detail 60-75
- **Architecture**: Advanced Sketch at detail 85+
- **Anime Art**: Anime/Manga style with high shading

## Troubleshooting

### Video Won't Play
- Ensure FFmpeg is installed
- Try different video player
- Check output file isn't corrupted

### Processing Too Slow
- Reduce detail level
- Lower output resolution
- Disable paper texture
- Use time-lapse mode

### Not Enough Detail
- Increase detail level
- Try Advanced Sketch style
- Increase shading intensity
- Use higher resolution source image

### Too Many Strokes
- Decrease detail level
- Adjust speed to show fewer strokes per frame
- Use simpler art style

## Batch Processing

Process multiple images:

```bash
for img in *.jpg; do
  art-animator animate "$img" -o "output_${img%.jpg}.mp4"
done
```

## Docker Usage

Build image:
```bash
docker build -t ai-art-animator .
```

Run:
```bash
docker run -v $(pwd)/inputs:/inputs -v $(pwd)/outputs:/outputs \
  ai-art-animator animate /inputs/photo.jpg -o /outputs/animation.mp4
```
