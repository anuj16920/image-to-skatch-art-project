# API Reference

## Core Classes

### ArtProcessor

```python
class ArtProcessor:
    def __init__(self, logger: Logger)
    
    def apply_style(
        self,
        image_path: str,
        style: str,
        shading_intensity: float = 0.6,
        progress_cb: Optional[Callable] = None,
    ) -> Image.Image
```

**Parameters:**
- `image_path`: Path to source image
- `style`: One of: "Pencil Sketch", "Advanced Sketch", "Watercolor", "Oil Painting", "Charcoal", "Anime / Manga"
- `shading_intensity`: 0.0-1.0, controls shading darkness
- `progress_cb`: Optional callback(value: float, label: str)

**Returns:** Styled PIL Image

### StrokeEngine

```python
class StrokeEngine:
    def __init__(
        self,
        detail_level: int = 75,
        human_jitter: bool = True,
        style: str = "Pencil Sketch",
    )
    
    def extract_stroke_layers(
        self,
        source_bgr: np.ndarray,
        styled_bgr: np.ndarray,
    ) -> List[StrokeLayer]
```

**Parameters:**
- `detail_level`: 10-100, stroke density
- `human_jitter`: Enable hand tremor simulation
- `style`: Art style name

**Returns:** List of 3 StrokeLayer objects

### ArtAnimator

```python
class ArtAnimator:
    def __init__(self, logger: Logger, output_dir: Optional[Path] = None)
    
    def create_animation(
        self,
        styled_image: Image.Image,
        source_path: str,
        style: str,
        speed: int,
        detail_level: int,
        fps: int,
        resolution: Optional[Tuple[int, int]],
        paper_texture: bool,
        human_jitter: bool,
        timelapse: bool,
        export_gif: bool,
        bg_type: str,
        progress_cb: Callable,
        preview_cb: Callable,
    ) -> str
```

**Parameters:**
- `styled_image`: Styled PIL image
- `source_path`: Path to original image
- `style`: Art style name
- `speed`: 1-100, animation speed
- `detail_level`: 10-100, stroke count
- `fps`: 24, 30, or 60
- `resolution`: (width, height) or None
- `paper_texture`: Enable texture overlay
- `human_jitter`: Enable hand tremor
- `timelapse`: 6x speed mode
- `export_gif`: Also save as GIF
- `bg_type`: Background type
- `progress_cb`: Progress callback
- `preview_cb`: Preview frame callback

**Returns:** Path to output MP4 file

## Data Structures

### Stroke

```python
@dataclass
class Stroke:
    points: np.ndarray      # (N, 2) float32
    thickness: np.ndarray   # (N,) float32
    darkness: float = 0.85
    layer: int = 0
    color: Tuple[int, int, int] = (20, 20, 20)
```

### StrokeLayer

```python
@dataclass
class StrokeLayer:
    name: str
    strokes: List[Stroke]
```

### Config

```python
@dataclass
class Config:
    style: StyleConfig
    animation: AnimationConfig
    output_dir: Path
    log_level: str
    max_workers: int
    
    @classmethod
    def from_yaml(cls, path: Path) -> Config
    
    def to_yaml(self, path: Path) -> None
    
    def validate(self) -> None
```

## Utilities

### Logger

```python
class Logger:
    def __init__(
        self,
        name: str = "ArtAnimator",
        level: str = "INFO",
        log_file: Optional[Path] = None,
    )
    
    def info(self, msg: str) -> None
    def debug(self, msg: str) -> None
    def warning(self, msg: str) -> None
    def error(self, msg: str) -> None
```

### Image Utils

```python
def pil_to_cv2(pil_img: Image.Image) -> np.ndarray
def cv2_to_pil(cv2_img: np.ndarray) -> Image.Image
def validate_image_path(path: str) -> Tuple[bool, str]
def resize_for_processing(img: np.ndarray, max_dim: int) -> Tuple[np.ndarray, float]
```

### Texture Generator

```python
def get_paper_texture(
    width: int,
    height: int,
    bg_type: str = "White Paper",
) -> np.ndarray
```

## CLI Commands

### animate

```bash
art-animator animate INPUT_IMAGE [OPTIONS]
```

**Options:**
- `-o, --output PATH`: Output video path
- `-s, --style STYLE`: Art style
- `--speed INT`: Animation speed (1-100)
- `--detail INT`: Detail level (10-100)
- `--fps CHOICE`: 24, 30, or 60
- `--resolution WxH`: Output resolution
- `--shading FLOAT`: Shading intensity (0.0-1.0)
- `--no-texture`: Disable paper texture
- `--no-jitter`: Disable human jitter
- `--timelapse`: Enable time-lapse mode
- `--gif`: Also export as GIF
- `--background TYPE`: Background type
- `-v, --verbose`: Verbose output

### validate-config

```bash
art-animator validate-config CONFIG_FILE
```

### gui

```bash
art-animator gui
```

## Configuration File Format

```yaml
style:
  name: "Pencil Sketch"
  shading_intensity: 0.6

animation:
  speed: 50
  detail_level: 75
  fps: 30
  resolution: [1920, 1080]
  paper_texture: true
  human_jitter: true
  timelapse: false
  export_gif: false
  background_type: "White Paper"

output_dir: "~/ArtAnimator_Exports"
log_level: "INFO"
max_workers: 4
```
