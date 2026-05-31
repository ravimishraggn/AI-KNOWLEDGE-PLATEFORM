.PHONY: help install dev-install lint format test test-unit test-integration clean docker-up docker-down

PYTHON := python3
PIP := pip
RUFF := ruff
MYPY := mypy

help:
	@echo "Knowledge Operating Platform — Make Targets"
	@echo ""
	@echo "  install          Install production dependencies"
	@echo "  dev-install      Install all development dependencies"
	@echo "  lint             Run ruff + mypy"
	@echo "  format           Auto-format with ruff"
	@echo "  test             Run all tests"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests (requires services)"
	@echo "  docker-up        Start all platform services"
	@echo "  docker-down      Stop all platform services"
	@echo "  clean            Remove build artifacts"

install:
	$(PIP) install -e "01-foundation/."

dev-install:
	$(PIP) install -e "01-foundation/.[dev]"
	pre-commit install

lint:
	$(RUFF) check .
	$(MYPY) 01-foundation/src

format:
	$(RUFF) format .
	$(RUFF) check --fix .

test:
	pytest --tb=short -q

test-unit:
	pytest --tb=short -q -m "not integration"

test-integration:
	pytest --tb=short -q -m integration

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

.DEFAULT_GOAL := help
