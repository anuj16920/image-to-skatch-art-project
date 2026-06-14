# Architecture Overview

## System Design

AI Art Animator follows a modular, layered architecture with clear separation of concerns.

## Core Components

### 1. Art Processor (`core/art_processor.py`)

Transforms source images into artistic styles using computer vision techniques.

**Responsibilities:**
- Image loading and preprocessing
- Style-specific filtering and effects
- Color quantization and edge detection
- Texture overlay

**Styles Implemented:**
- Pencil Sketch: Dodge-blend technique
- Advanced Sketch: Multi-scale edge detection
- Watercolor: Bilateral filtering + K-means
- Oil Painting: xPhoto filter + brushstrokes
- Charcoal: Heavy blur + grain
- Anime/Manga: Cel-shading + bold outlines

### 2. Stroke Engine (`core/stroke_engine.py`)

Extracts realistic drawing strokes from images.

**Algorithm:**
1. Multi-scale Canny edge detection
2. Contour extraction and hierarchical ordering
3. Catmull-Rom spline smoothing
4. Pressure simulation from gradient magnitude
5. Human jitter via Perlin-like noise
6. Adaptive shading stroke generation

**Output:**
- Layer 0: Outline strokes (main contours)
- Layer 1: Detail strokes (secondary edges)
- Layer 2: Shading strokes (tonal hatching)

### 3. Animator (`core/animator.py`)

Renders stroke layers into frame-by-frame video.

**Pipeline:**
1. Initialize canvas with paper texture
2. Progressively render strokes
3. Emit frames at configured intervals
4. Apply paper texture overlay
5. Encode to MP4 using H.264
6. Optional GIF export

**Performance:**
- Adaptive frame emission based on speed
- Working resolution downsampling
- Lazy frame composition

### 4. Configuration System (`config/settings.py`)

Manages application settings with validation.

**Features:**
- YAML-based configuration
- Dataclass-based settings
- Validation and type checking
- Default configuration presets

### 5. Utilities (`utils/`)

Shared functionality across modules.

**Modules:**
- `logger.py`: Professional logging with file/console output
- `image_utils.py`: Image I/O and format conversion
- `texture_generator.py`: Procedural paper texture generation

## Data Flow

```
Input Image
    ↓
[Art Processor]
    ↓
Styled Image
    ↓
[Stroke Engine]
    ↓
Stroke Layers (3)
    ↓
[Animator]
    ↓
Video Frames
    ↓
MP4/GIF Output
```

## Design Patterns

### Factory Pattern
Style processors use factory pattern via `StyleRegistry` for dynamic style loading.

### Strategy Pattern
Different artistic styles implement the same `BaseStyleProcessor` interface.

### Observer Pattern
Progress callbacks allow UI updates without tight coupling.

### Dependency Injection
Components receive dependencies (logger, config) via constructor injection.

## Extensibility

### Adding New Styles

1. Create class inheriting from `BaseStyleProcessor`
2. Implement `process()` method
3. Register with `@register_style` decorator

```python
from art_animator.styles import BaseStyleProcessor, register_style

@register_style("My Style")
class MyStyleProcessor(BaseStyleProcessor):
    def process(self, img_bgr, shading_intensity, progress_cb):
        # Your implementation
        return styled_img
```

### Custom Export Formats

Extend `ArtAnimator` class and override export methods.

### Plugin System

Future: Plugin architecture for third-party extensions.

## Performance Considerations

- **Working Resolution**: Images downsampled to 900px for stroke extraction
- **Contour Subsampling**: Dense contours limited to 200 points
- **Adaptive Frame Emission**: Only emit frames when threshold met
- **Lazy Composition**: Frame composition only when needed

## Thread Safety

- GUI operations run on main thread
- Processing/animation run on worker threads
- Thread-safe callbacks for progress updates
- Logger supports concurrent access

## Error Handling

- Validation at configuration level
- Graceful fallbacks for missing features
- Detailed error messages with context
- Exception propagation with logging
