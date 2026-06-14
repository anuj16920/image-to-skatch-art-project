"""Command-line interface for AI Art Animator."""

from __future__ import annotations
import click
from pathlib import Path
from PIL import Image
import sys

from art_animator.core.art_processor import ArtProcessor
from art_animator.core.animator import ArtAnimator
from art_animator.utils.logger import Logger
from art_animator.config.settings import Config, StyleConfig, AnimationConfig


@click.group()
@click.version_option(version="1.0.0")
def main():
    """AI Art Animator - Convert images into realistic drawing animations."""
    pass


@main.command()
@click.argument('input_image', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output video path')
@click.option('--style', '-s', default='Pencil Sketch', 
              type=click.Choice([
                  'Pencil Sketch', 'Advanced Sketch', 'Watercolor',
                  'Oil Painting', 'Charcoal', 'Anime / Manga'
              ]), help='Art style to apply')
@click.option('--speed', default=50, type=click.IntRange(1, 100), 
              help='Animation speed (1-100)')
@click.option('--detail', default=75, type=click.IntRange(10, 100),
              help='Detail level (10-100)')
@click.option('--fps', default=30, type=click.Choice(['24', '30', '60']),
              help='Frames per second')
@click.option('--resolution', type=str, help='Output resolution (e.g., 1920x1080)')
@click.option('--shading', default=0.6, type=click.FloatRange(0.0, 1.0),
              help='Shading intensity (0.0-1.0)')
@click.option('--no-texture', is_flag=True, help='Disable paper texture')
@click.option('--no-jitter', is_flag=True, help='Disable human jitter')
@click.option('--timelapse', is_flag=True, help='Enable time-lapse mode')
@click.option('--gif', is_flag=True, help='Also export as GIF')
@click.option('--background', default='White Paper',
              type=click.Choice([
                  'White Paper', 'Aged Paper', 'Dark Canvas',
                  'Pure White', 'Pure Black'
              ]), help='Background type')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def animate(
    input_image: str,
    output: str,
    style: str,
    speed: int,
    detail: int,
    fps: str,
    resolution: str,
    shading: float,
    no_texture: bool,
    no_jitter: bool,
    timelapse: bool,
    gif: bool,
    background: str,
    verbose: bool,
):
    """
    Create drawing animation from an image.
    
    Example:
        art-animator animate input.jpg -o output.mp4 --style "Pencil Sketch"
    """
    # Setup logger
    log_level = "DEBUG" if verbose else "INFO"
    logger = Logger(level=log_level)
    
    logger.info(f"🎨 AI Art Animator v1.0.0")
    logger.info(f"📂 Input: {input_image}")
    
    # Parse resolution
    res_tuple = None
    if resolution:
        try:
            w, h = map(int, resolution.lower().split('x'))
            res_tuple = (w, h)
        except:
            logger.error(f"Invalid resolution format: {resolution}")
            sys.exit(1)
    
    # Create config
    config = Config(
        style=StyleConfig(name=style, shading_intensity=shading),
        animation=AnimationConfig(
            speed=speed,
            detail_level=detail,
            fps=int(fps),
            resolution=res_tuple,
            paper_texture=not no_texture,
            human_jitter=not no_jitter,
            timelapse=timelapse,
            export_gif=gif,
            background_type=background,
        )
    )
    
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Process image
    logger.info(f"🎨 Applying style: {style}")
    processor = ArtProcessor(logger=logger)
    
    try:
        styled_image = processor.apply_style(
            input_image,
            style,
            shading_intensity=shading,
        )
    except Exception as e:
        logger.error(f"Style processing failed: {e}")
        sys.exit(1)
    
    # Create animation
    logger.info("🎬 Creating animation...")
    animator = ArtAnimator(logger=logger)
    
    def progress_callback(value: float, label: str):
        if verbose:
            logger.debug(f"Progress: {value*100:.1f}% - {label}")
    
    def preview_callback(frame):
        pass  # CLI doesn't need preview
    
    try:
        output_path = animator.create_animation(
            styled_image=styled_image,
            source_path=input_image,
            style=style,
            speed=speed,
            detail_level=detail,
            fps=int(fps),
            resolution=res_tuple,
            paper_texture=not no_texture,
            human_jitter=not no_jitter,
            timelapse=timelapse,
            export_gif=gif,
            bg_type=background,
            progress_cb=progress_callback,
            preview_cb=preview_callback,
        )
        
        # Move to specified output if provided
        if output:
            import shutil
            output_path_obj = Path(output)
            output_path_obj.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(output_path, output)
            logger.info(f"✅ Animation saved: {output}")
        else:
            logger.info(f"✅ Animation saved: {output_path}")
        
    except Exception as e:
        logger.error(f"Animation failed: {e}")
        import traceback
        if verbose:
            traceback.print_exc()
        sys.exit(1)


@main.command()
@click.argument('config_file', type=click.Path(exists=True))
def validate_config(config_file: str):
    """Validate a configuration file."""
    try:
        config = Config.from_yaml(Path(config_file))
        config.validate()
        click.echo(f"✅ Configuration is valid: {config_file}")
    except Exception as e:
        click.echo(f"❌ Configuration error: {e}", err=True)
        sys.exit(1)


@main.command()
def gui():
    """Launch the GUI application."""
    from art_animator.gui.main import launch
    launch()


if __name__ == "__main__":
    main()
