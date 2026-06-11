# PropSim Platform Make Shortcut System

.PHONY: setup test lint build run clean help

setup:
	@echo "Setting up development environment..."
	python -m venv .venv
	.venv/Scripts/pip install -e .[dev]
	pre-commit install

test:
	@echo "Running verification test suites..."
	pytest tests/ -v

lint:
	@echo "Linting source directories..."
	ruff check .
	mypy core engines

build:
	@echo "Building package distribution..."
	python -m build

run:
	@echo "Starting local development stack..."
	docker-compose up -d

clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
