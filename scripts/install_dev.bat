@echo off
REM Development environment setup script for Windows

echo Setting up AI Art Animator development environment...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install package in development mode
pip install -e ".[dev]"

REM Install pre-commit hooks
pre-commit install

echo.
echo Development environment ready!
echo.
echo To activate: venv\Scripts\activate.bat
echo To run tests: pytest tests/
echo To run GUI: art-animator-gui
