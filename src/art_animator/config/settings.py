"""Configuration management with YAML support."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import yaml


@dataclass
class StyleConfig:
    """Configuration for art style processing."""
    
    name: str = "Pencil Sketch"
    shading_intensity: float = 0.6
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not 0.0 <= self.shading_intensity <= 1.0:
            raise ValueError(f"shading_intensity must be 0-1, got {self.shading_intensity}")


@dataclass
class AnimationConfig:
    """Configuration for animation rendering."""
    
    speed: int = 50
    detail_level: int = 75
    fps: int = 30
    resolution: Optional[Tuple[int, int]] = None
    paper_texture: bool = True
    human_jitter: bool = True
    timelapse: bool = False
    export_gif: bool = False
    background_type: str = "White Paper"
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not 1 <= self.speed <= 100:
            raise ValueError(f"speed must be 1-100, got {self.speed}")
        if not 10 <= self.detail_level <= 100:
            raise ValueError(f"detail_level must be 10-100, got {self.detail_level}")
        if self.fps not in {24, 30, 60}:
            raise ValueError(f"fps must be 24, 30, or 60, got {self.fps}")


@dataclass
class Config:
    """Main application configuration."""
    
    style: StyleConfig = field(default_factory=StyleConfig)
    animation: AnimationConfig = field(default_factory=AnimationConfig)
    output_dir: Path = field(default_factory=lambda: Path.home() / "ArtAnimator_Exports")
    log_level: str = "INFO"
    max_workers: int = 4
    
    @classmethod
    def from_yaml(cls, path: Path) -> Config:
        """Load configuration from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        style_data = data.get('style', {})
        animation_data = data.get('animation', {})
        
        return cls(
            style=StyleConfig(**style_data),
            animation=AnimationConfig(**animation_data),
            output_dir=Path(data.get('output_dir', cls.output_dir)),
            log_level=data.get('log_level', 'INFO'),
            max_workers=data.get('max_workers', 4),
        )
    
    def to_yaml(self, path: Path) -> None:
        """Save configuration to YAML file."""
        data = {
            'style': asdict(self.style),
            'animation': asdict(self.animation),
            'output_dir': str(self.output_dir),
            'log_level': self.log_level,
            'max_workers': self.max_workers,
        }
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    def validate(self) -> None:
        """Validate all configuration values."""
        self.style.validate()
        self.animation.validate()
        
        if self.log_level not in {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}:
            raise ValueError(f"Invalid log_level: {self.log_level}")
        
        if self.max_workers < 1:
            raise ValueError(f"max_workers must be >= 1, got {self.max_workers}")
