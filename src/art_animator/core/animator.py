"""
Animation Engine — Renders stroke layers frame-by-frame to produce a
realistic "artist is drawing" video.

Pipeline:
  1. StrokeEngine extracts ordered stroke layers from the image
  2. Frames are rendered by progressively drawing strokes
  3. Paper texture overlays each frame
  4. cv2.VideoWriter encodes to MP4 (H.264)
  5. Optional: GIF export via imageio
"""

from __future__ import annotations
import cv2
import numpy as np
import time
import imageio
from pathlib import Path
from PIL import Image
from typing import Callable, List, Optional, Tuple

from art_animator.utils.logger import Logger
from art_animator.utils.image_utils import pil_to_cv2, cv2_to_pil
from art_animator.utils.texture_generator import get_paper_texture
from art_animator.core.stroke_engine import StrokeEngine, StrokeLayer, Stroke


class ArtAnimator:
    """
    Main animation engine for rendering stroke-based drawing videos.
    
    Converts extracted stroke layers into frame-by-frame animations
    that simulate an artist drawing the image in real-time.
    """

    OUTPUT_DIR = Path.home() / "ArtAnimator_Exports"

    def __init__(self, logger: Logger, output_dir: Optional[Path] = None):
        """
        Initialize animator.
        
        Args:
            logger: Logger instance
            output_dir: Custom output directory (optional)
        """
        self.logger = logger
        if output_dir:
            self.OUTPUT_DIR = output_dir
        self.OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

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
        progress_cb: Callable[[float, str], None],
        preview_cb: Callable[[Image.Image], None],
    ) -> str:
        """
        Create drawing animation from styled image.
        
        Args:
            styled_image: Styled PIL image
            source_path: Path to original source image
            style: Art style name
            speed: Animation speed (1-100)
            detail_level: Stroke detail level (10-100)
            fps: Frames per second
            resolution: Output resolution (width, height) or None for source size
            paper_texture: Enable paper texture overlay
            human_jitter: Enable hand tremor simulation
            timelapse: Enable time-lapse mode (6x speed)
            export_gif: Also export as GIF
            bg_type: Background type
            progress_cb: Progress callback function
            preview_cb: Preview frame callback function
            
        Returns:
            Path to exported MP4 file
            
        Raises:
            FileNotFoundError: If source image not found
            RuntimeError: If video writer fails to initialize
        """
        self.logger.info("🔍 Extracting stroke layers...")
        progress_cb(0.05, "Extracting edges...")

        # Prepare images
        source_bgr = cv2.imread(source_path)
        if source_bgr is None:
            raise FileNotFoundError(f"Cannot read source image: {source_path}")

        styled_bgr = pil_to_cv2(styled_image)

        # Determine output resolution
        if resolution:
            out_w, out_h = resolution
            source_bgr = cv2.resize(source_bgr, (out_w, out_h), interpolation=cv2.INTER_LANCZOS4)
            styled_bgr = cv2.resize(styled_bgr, (out_w, out_h), interpolation=cv2.INTER_LANCZOS4)
        else:
            out_h, out_w = styled_bgr.shape[:2]

        # Working size for stroke extraction (max 900px for performance)
        work_scale = min(1.0, 900 / max(out_h, out_w))
        work_w = int(out_w * work_scale)
        work_h = int(out_h * work_scale)
        src_work = cv2.resize(source_bgr, (work_w, work_h))
        sty_work = cv2.resize(styled_bgr, (work_w, work_h))

        # Stroke extraction
        engine = StrokeEngine(
            detail_level=detail_level,
            human_jitter=human_jitter,
            style=style,
        )
        layers = engine.extract_stroke_layers(src_work, sty_work)
        total_strokes = sum(len(layer.strokes) for layer in layers)
        self.logger.info(f"📊 Total strokes: {total_strokes} across {len(layers)} layers")
        progress_cb(0.15, f"Found {total_strokes} strokes")

        # Background texture
        bg_texture = get_paper_texture(out_w, out_h, bg_type)

        # Video writer setup
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        out_path = str(self.OUTPUT_DIR / f"art_animation_{timestamp}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps, (out_w, out_h))
        
        if not writer.isOpened():
            raise RuntimeError("Failed to open VideoWriter — check ffmpeg installation.")

        gif_frames: Optional[List[np.ndarray]] = [] if export_gif else None

        # Canvas state
        canvas = bg_texture.copy().astype(np.float32)
        frame_count = 0

        # Speed mapping
        strokes_per_frame = max(1, int(speed / 12))
        if timelapse:
            strokes_per_frame *= 6

        drawn = 0

        # Render loop
        for layer_idx, layer in enumerate(layers):
            self.logger.info(
                f"🖊  Drawing layer {layer_idx}: {layer.name} ({len(layer.strokes)} strokes)"
            )

            for si, stroke in enumerate(layer.strokes):
                self._render_stroke(canvas, stroke, out_w, out_h, work_w, work_h)
                drawn += 1

                # Emit frame
                if drawn % strokes_per_frame == 0:
                    frame = self._compose_frame(
                        canvas, bg_texture, paper_texture, styled_bgr,
                        layer_idx, len(layers), si / max(1, len(layer.strokes))
                    )
                    writer.write(frame)
                    frame_count += 1

                    if gif_frames is not None and frame_count % 4 == 0:
                        gif_frames.append(cv2.cvtColor(
                            cv2.resize(frame, (480, int(480 * out_h / out_w))),
                            cv2.COLOR_BGR2RGB
                        ))

                    # Progress update
                    overall = 0.15 + 0.80 * (drawn / max(1, total_strokes))
                    progress_cb(
                        overall,
                        f"Layer {layer_idx + 1}/{len(layers)}: {si}/{len(layer.strokes)}"
                    )

                    # Live preview
                    if frame_count % 30 == 0:
                        preview_pil = cv2_to_pil(
                            cv2.resize(frame, (800, int(800 * out_h / out_w)))
                        )
                        preview_cb(preview_pil)

        # Hold final frame
        final_frame = self._compose_frame(
            canvas, bg_texture, paper_texture, styled_bgr,
            len(layers) - 1, len(layers), 1.0
        )
        for _ in range(fps * 2):
            writer.write(final_frame)

        writer.release()
        self.logger.info(f"✅ Video: {frame_count} frames @ {fps}fps → {out_path}")

        # GIF export
        if export_gif and gif_frames:
            gif_path = out_path.replace(".mp4", ".gif")
            imageio.mimsave(gif_path, gif_frames, fps=fps // 2, loop=0)
            self.logger.info(f"🎞  GIF: {gif_path}")

        progress_cb(1.0, "Complete!")
        return out_path

    def _compose_frame(
        self,
        canvas: np.ndarray,
        bg_texture: np.ndarray,
        use_texture: bool,
        styled_bgr: np.ndarray,
        current_layer: int,
        total_layers: int,
        layer_progress: float,
    ) -> np.ndarray:
        """
        Compose final frame from canvas and paper texture.
        
        Args:
            canvas: Current drawing canvas (float32)
            bg_texture: Paper texture background
            use_texture: Whether to apply texture overlay
            styled_bgr: Styled reference image
            current_layer: Current layer index
            total_layers: Total number of layers
            layer_progress: Progress within current layer (0-1)
            
        Returns:
            Composed frame in BGR format (uint8)
        """
        frame = np.clip(canvas, 0, 255).astype(np.uint8)

        if use_texture:
            # Multiply-blend paper texture
            tex_f = bg_texture.astype(np.float32) / 255.0
            frame_f = frame.astype(np.float32) / 255.0
            blended = frame_f * (0.92 + tex_f * 0.08)
            frame = np.clip(blended * 255, 0, 255).astype(np.uint8)

        return frame

    def _render_stroke(
        self,
        canvas: np.ndarray,
        stroke: Stroke,
        out_w: int,
        out_h: int,
        work_w: int,
        work_h: int,
    ) -> None:
        """
        Draw one stroke onto the floating-point canvas.
        
        Args:
            canvas: Canvas to draw on (modified in-place)
            stroke: Stroke to render
            out_w: Output width
            out_h: Output height
            work_w: Working width (stroke coordinates)
            work_h: Working height (stroke coordinates)
        """
        pts = stroke.points.copy()
        thickness = stroke.thickness.copy()
        color_rgb = stroke.color
        darkness = stroke.darkness

        # Scale from work-space to output-space
        sx = out_w / max(1, work_w)
        sy = out_h / max(1, work_h)
        pts[:, 0] *= sx
        pts[:, 1] *= sy
        thickness = thickness * max(sx, sy)

        # Convert color to BGR float
        bgr = np.array([color_rgb[2], color_rgb[1], color_rgb[0]], dtype=np.float32)

        # Draw segment by segment
        for i in range(len(pts) - 1):
            p0 = (int(pts[i, 0]), int(pts[i, 1]))
            p1 = (int(pts[i + 1, 0]), int(pts[i + 1, 1]))
            t = max(0.5, float(thickness[i]))

            # Clip to canvas bounds
            if (0 <= p0[0] < out_w and 0 <= p0[1] < out_h and
                    0 <= p1[0] < out_w and 0 <= p1[1] < out_h):

                # Anti-aliased line with alpha blending
                alpha = darkness * np.clip(thickness[i] / 3.0, 0.3, 1.0)
                line_img = np.zeros_like(canvas, dtype=np.float32)
                cv2.line(
                    line_img, p0, p1,
                    (float(bgr[0]), float(bgr[1]), float(bgr[2])),
                    max(1, int(t)),
                    cv2.LINE_AA
                )

                # Update only where stroke was drawn
                mask = line_img.sum(axis=2) > 0
                canvas[mask] = canvas[mask] * (1 - alpha) + line_img[mask] * alpha
