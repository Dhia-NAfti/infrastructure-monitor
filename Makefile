.PHONY: help install test lint ruff typecheck check run clean

PYTHON := python

help:
	@echo "install    Install dependencies"
	@echo "test       Run pytest"
	@echo "lint       Run Flake8"
	@echo "ruff       Run Ruff"
	@echo "typecheck  Run mypy"
	@echo "check      Run all quality checks"
	@echo "run        Start the Flask API"
	@echo "clean      Remove generated cache files"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest tests/ -v

lint:
	$(PYTHON) -m flake8 app/ tests/

ruff:
	$(PYTHON) -m ruff check app/ tests/

typecheck:
	$(PYTHON) -m mypy app/

check: lint ruff typecheck test

run:
	$(PYTHON) -m flask --app app run --debug

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache
