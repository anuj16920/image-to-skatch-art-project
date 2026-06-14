# Changelog

All notable changes to AI Art Animator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-05

### Added
- Professional package structure with `src/` layout
- Command-line interface with Click
- Configuration management with YAML support
- Comprehensive test suite with pytest
- Full documentation (user guide, API reference, architecture)
- Docker support with Dockerfile and docker-compose
- CI/CD pipeline with GitHub Actions
- Pre-commit hooks for code quality
- Type hints throughout codebase
- Professional logging system
- Style registry for extensible style system
- Batch processing examples
- Development setup scripts
- Makefile for common tasks
- Contributing guidelines

### Changed
- Refactored monolithic files into modular structure
- Improved error handling and validation
- Enhanced documentation with docstrings
- Better separation of concerns
- Optimized imports and dependencies

### Fixed
- ValueError in stroke_engine.py (low >= high) by ensuring minimum bounds
- Thread safety in GUI callbacks
- Import path issues with proper package structure

### Deprecated
- Root-level files (main.py, animator.py, etc.) now redirect to new structure
- Old import paths still work but will be removed in 2.0.0

## [0.1.0] - Initial Release

### Added
- Basic GUI with CustomTkinter
- 6 artistic styles
- Stroke-based animation
- Paper texture generation
- MP4 and GIF export
