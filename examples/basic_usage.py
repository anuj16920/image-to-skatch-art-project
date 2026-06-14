"""Basic usage example for AI Art Animator."""

from art_animator import ArtProcessor, ArtAnimator
from art_animator.utils import Logger

# Setup
logger = Logger(level="INFO")
processor = ArtProcessor(logger)
animator = ArtAnimator(logger)

# Input image
input_image = "sample.jpg"

# Apply artistic style
print("Applying style...")
styled_image = processor.apply_style(
    image_path=input_image,
    style="Pencil Sketch",
    shading_intensity=0.6,
    progress_cb=lambda v, l: print(f"  {v*100:.0f}% - {l}"),
)

# Create animation
print("Creating animation...")
output_path = animator.create_animation(
    styled_image=styled_image,
    source_path=input_image,
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
    progress_cb=lambda v, l: print(f"  {v*100:.0f}% - {l}"),
    preview_cb=lambda f: None,
)

print(f"\nAnimation saved: {output_path}")
