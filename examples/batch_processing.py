"""Batch processing example."""

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from art_animator import ArtProcessor, ArtAnimator
from art_animator.utils import Logger


def process_image(image_path: Path, output_dir: Path, style: str = "Pencil Sketch"):
    """Process single image."""
    logger = Logger(level="INFO")
    processor = ArtProcessor(logger)
    animator = ArtAnimator(logger, output_dir=output_dir)
    
    print(f"Processing: {image_path.name}")
    
    try:
        # Apply style
        styled = processor.apply_style(
            str(image_path),
            style=style,
            shading_intensity=0.6,
        )
        
        # Create animation
        output = animator.create_animation(
            styled_image=styled,
            source_path=str(image_path),
            style=style,
            speed=60,
            detail_level=70,
            fps=30,
            resolution=(1280, 720),
            paper_texture=True,
            human_jitter=True,
            timelapse=True,
            export_gif=False,
            bg_type="White Paper",
            progress_cb=lambda v, l: None,
            preview_cb=lambda f: None,
        )
        
        print(f"  ✅ Completed: {output}")
        return output
        
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return None


def batch_process(input_dir: str, output_dir: str, max_workers: int = 4):
    """Process all images in directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    # Find all images
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    images = [f for f in input_path.iterdir() if f.suffix.lower() in image_extensions]
    
    print(f"Found {len(images)} images to process")
    print(f"Using {max_workers} workers\n")
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_image, img, output_path): img
            for img in images
        }
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            img = futures[future]
            print(f"[{completed}/{len(images)}] Finished: {img.name}\n")
    
    print(f"\nBatch processing complete! Output: {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python batch_processing.py <input_dir> <output_dir> [max_workers]")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    
    batch_process(input_dir, output_dir, max_workers)
