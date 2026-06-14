"""Example of using configuration files."""

from pathlib import Path
from art_animator.config import Config, StyleConfig, AnimationConfig

# Create configuration
config = Config(
    style=StyleConfig(
        name="Watercolor",
        shading_intensity=0.7,
    ),
    animation=AnimationConfig(
        speed=60,
        detail_level=85,
        fps=30,
        resolution=(1920, 1080),
        paper_texture=True,
        human_jitter=True,
        timelapse=False,
        export_gif=True,
        background_type="Aged Paper",
    ),
    output_dir=Path("./my_animations"),
    log_level="DEBUG",
    max_workers=4,
)

# Validate
try:
    config.validate()
    print("✅ Configuration is valid")
except ValueError as e:
    print(f"❌ Configuration error: {e}")

# Save to file
config_path = Path("my_config.yaml")
config.to_yaml(config_path)
print(f"Configuration saved to: {config_path}")

# Load from file
loaded_config = Config.from_yaml(config_path)
print(f"Loaded configuration: {loaded_config.style.name}")

# Use with animator
from art_animator import ArtAnimator
from art_animator.utils import Logger

logger = Logger(level=loaded_config.log_level)
animator = ArtAnimator(logger, output_dir=loaded_config.output_dir)

print(f"Animator output directory: {animator.OUTPUT_DIR}")
