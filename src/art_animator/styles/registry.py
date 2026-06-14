"""Style registry for dynamic style loading."""

from __future__ import annotations
from typing import Dict, Type
from art_animator.styles.base import BaseStyleProcessor


class StyleRegistry:
    """
    Registry for managing available artistic styles.
    
    Allows dynamic registration and retrieval of style processors.
    """
    
    _styles: Dict[str, Type[BaseStyleProcessor]] = {}
    
    @classmethod
    def register(cls, name: str, processor_class: Type[BaseStyleProcessor]) -> None:
        """
        Register a style processor.
        
        Args:
            name: Style name (must be unique)
            processor_class: Style processor class
        """
        if name in cls._styles:
            raise ValueError(f"Style '{name}' is already registered")
        cls._styles[name] = processor_class
    
    @classmethod
    def get(cls, name: str) -> Type[BaseStyleProcessor]:
        """
        Get a style processor class by name.
        
        Args:
            name: Style name
            
        Returns:
            Style processor class
            
        Raises:
            KeyError: If style is not registered
        """
        if name not in cls._styles:
            raise KeyError(f"Style '{name}' not found. Available: {cls.list_styles()}")
        return cls._styles[name]
    
    @classmethod
    def list_styles(cls) -> list[str]:
        """Get list of all registered style names."""
        return list(cls._styles.keys())
    
    @classmethod
    def create(cls, name: str) -> BaseStyleProcessor:
        """
        Create an instance of a style processor.
        
        Args:
            name: Style name
            
        Returns:
            Style processor instance
        """
        processor_class = cls.get(name)
        return processor_class(name)


def register_style(name: str):
    """
    Decorator for registering style processors.
    
    Usage:
        @register_style("My Style")
        class MyStyleProcessor(BaseStyleProcessor):
            ...
    """
    def decorator(cls: Type[BaseStyleProcessor]):
        StyleRegistry.register(name, cls)
        return cls
    return decorator
