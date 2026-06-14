.PHONY: install dev test lint format clean build docs

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=art_animator --cov-report=html

lint:
	flake8 src/art_animator tests
	mypy src/art_animator

format:
	black src/art_animator tests
	isort src/art_animator tests

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python -m build

docs:
	cd docs && make html

run-gui:
	art-animator-gui

run-cli:
	art-animator --help
