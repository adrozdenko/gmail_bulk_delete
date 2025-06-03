# Gmail Bulk Delete - Makefile
# Following Emex development standards

.PHONY: help install dev-install quality quality-fix test test-cov clean run

help: ## Show this help message
	@echo "Gmail Bulk Delete - Development Commands"
	@echo "========================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	poetry install --only=main

dev-install: ## Install all dependencies including dev tools
	poetry install
	poetry run pre-commit install

quality: ## Run all quality checks (type-check, lint, format-check)
	@echo "🔍 Running type checking..."
	poetry run mypy src/
	@echo "🔍 Running linting..."
	poetry run flake8 src/ tests/
	@echo "🔍 Checking code formatting..."
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/
	@echo "✅ All quality checks passed!"

quality-fix: ## Fix all quality issues automatically
	@echo "🔧 Formatting code..."
	poetry run black src/ tests/
	poetry run isort src/ tests/
	@echo "🔧 Running linter fixes..."
	poetry run flake8 src/ tests/ || true
	@echo "🔧 Running type check..."
	poetry run mypy src/ || true
	@echo "✅ Quality fixes applied!"

test: ## Run tests
	poetry run pytest tests/ -v

test-cov: ## Run tests with coverage report
	poetry run pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "📊 Coverage report generated in htmlcov/"

clean: ## Clean up generated files
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -name "*.pyc" -delete

run: ## Run the application
	poetry run python -m src.main

run-dry: ## Run in dry-run mode (safe testing)
	poetry run python -m src.main --dry-run

# Development workflow commands
dev-setup: dev-install ## Complete development setup
	@echo "🚀 Development environment ready!"
	@echo "Run 'make quality' before committing"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make run-dry' to test safely"

pre-commit: quality test ## Run before committing (quality + tests)
	@echo "✅ Ready to commit!"

# Build commands
build: ## Build distribution packages
	poetry build

publish: build ## Publish to PyPI (requires authentication)
	poetry publish