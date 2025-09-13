# SuperPrompts MCP Server Makefile (Poetry-Enhanced)
# ==================================================

# Variables
POETRY := poetry
PROJECT_NAME := superprompts
PACKAGE_NAME := superprompts
TEST_DIR := tests
SCRIPTS_DIR := scripts
SCHEMAS_DIR := schemas

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Default target
.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)SuperPrompts MCP Server - Available Commands$(NC)"
	@echo "=============================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# =============================================================================
# Testing (Simplified with Poetry)
# =============================================================================

.PHONY: test
test: ## Run all tests
	@echo "$(BLUE)Running SuperPrompts MCP Server Tests$(NC)"
	@echo "====================================="
	@echo "$(BLUE)Running startup regression tests...$(NC)"
	$(POETRY) run python $(TEST_DIR)/test_startup.py
	@echo ""
	@echo "$(BLUE)Running server functionality tests...$(NC)"
	$(POETRY) run python $(TEST_DIR)/test_server.py
	@echo ""
	@echo "$(GREEN)All tests completed successfully! 🎉$(NC)"

.PHONY: test-unit
test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	$(POETRY) run pytest $(TEST_DIR)/ -v

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	$(POETRY) run python $(TEST_DIR)/test_server.py

.PHONY: test-startup
test-startup: ## Run startup regression tests
	@echo "$(BLUE)Running startup regression tests...$(NC)"
	$(POETRY) run python $(TEST_DIR)/test_startup.py

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(POETRY) run pytest $(TEST_DIR)/ --cov=$(PACKAGE_NAME) --cov-report=html --cov-report=term
	@echo "$(GREEN)Coverage report generated in htmlcov/$(NC)"

# =============================================================================
# Code Quality (Simplified with Poetry)
# =============================================================================

.PHONY: format
format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	$(POETRY) run black $(PACKAGE_NAME)/ $(TEST_DIR)/ $(SCRIPTS_DIR)/
	$(POETRY) run isort $(PACKAGE_NAME)/ $(TEST_DIR)/ $(SCRIPTS_DIR)/
	@echo "$(GREEN)Code formatted$(NC)"

.PHONY: lint
lint: ## Run linting with flake8
	@echo "$(BLUE)Running linter...$(NC)"
	$(POETRY) run flake8 $(PACKAGE_NAME)/ $(TEST_DIR)/ $(SCRIPTS_DIR)/
	@echo "$(GREEN)Linting completed$(NC)"

.PHONY: type-check
type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running type checker...$(NC)"
	$(POETRY) run mypy $(PACKAGE_NAME)/
	@echo "$(GREEN)Type checking completed$(NC)"

.PHONY: check-all
check-all: lint type-check ## Run all code quality checks
	@echo "$(GREEN)All code quality checks passed$(NC)"

# =============================================================================
# Validation (Project-specific)
# =============================================================================

.PHONY: validate
validate: ## Run all validation checks
	@echo "$(BLUE)Running validation checks...$(NC)"
	$(MAKE) validate-cursor-rules
	$(MAKE) validate-schemas
	@echo "$(GREEN)All validation checks passed$(NC)"

.PHONY: validate-cursor-rules
validate-cursor-rules: ## Validate cursor rules
	@echo "$(BLUE)Validating cursor rules...$(NC)"
	mkdir -p artifacts
	$(POETRY) run python $(SCRIPTS_DIR)/validate_cursor_rules.py --strict --report-json artifacts/cursor_rules_report.json .cursor/rules prompts/generate_cursor_rules.prompt.md
	@echo "$(GREEN)Cursor rules validation completed$(NC)"

.PHONY: validate-schemas
validate-schemas: ## Validate JSON schemas
	@echo "$(BLUE)Validating JSON schemas...$(NC)"
	@for schema in $(SCHEMAS_DIR)/*.json; do \
		echo "Validating $$schema..."; \
		$(POETRY) run python -c "import json; json.load(open('$$schema'))" || exit 1; \
	done
	@echo "$(GREEN)Schema validation completed$(NC)"

# =============================================================================
# Server Operations (Simplified with Poetry)
# =============================================================================

.PHONY: run-server
run-server: ## Run the MCP server
	@echo "$(BLUE)Starting MCP server...$(NC)"
	$(POETRY) run python -m $(PACKAGE_NAME).mcp.server

.PHONY: dev-server
dev-server: ## Run server in development mode
	@echo "$(BLUE)Starting development server...$(NC)"
	$(POETRY) run python -m $(PACKAGE_NAME).mcp.server --debug

# =============================================================================
# Documentation
# =============================================================================

.PHONY: docs
docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	@echo "$(YELLOW)Documentation generation not yet implemented$(NC)"

# =============================================================================
# Cleanup (Project-specific)
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts and temporary files
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf artifacts/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup completed$(NC)"

.PHONY: clean-cache
clean-cache: ## Clean Python cache files only
	@echo "$(BLUE)Cleaning cache files...$(NC)"
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)Cache cleanup completed$(NC)"

.PHONY: clean-all
clean-all: clean ## Clean everything including Poetry cache
	@echo "$(BLUE)Cleaning everything...$(NC)"
	$(POETRY) cache clear --all pypi
	@echo "$(GREEN)Complete cleanup finished$(NC)"

# =============================================================================
# Development Workflow (Simplified)
# =============================================================================

.PHONY: setup
setup: ## Complete development setup (Poetry handles dependencies)
	@echo "$(BLUE)Setting up development environment...$(NC)"
	$(POETRY) install
	$(MAKE) format
	$(MAKE) check-all
	@echo "$(GREEN)Development environment ready$(NC)"

.PHONY: pre-commit
pre-commit: format lint type-check test ## Run pre-commit checks
	@echo "$(GREEN)Pre-commit checks completed$(NC)"

.PHONY: ci
ci: check-all test validate ## Run CI pipeline locally
	@echo "$(GREEN)CI pipeline completed successfully$(NC)"

# =============================================================================
# Poetry-specific targets
# =============================================================================

.PHONY: install
install: ## Install dependencies (Poetry)
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(POETRY) install
	@echo "$(GREEN)Dependencies installed$(NC)"

.PHONY: update
update: ## Update dependencies (Poetry)
	@echo "$(BLUE)Updating dependencies...$(NC)"
	$(POETRY) update
	@echo "$(GREEN)Dependencies updated$(NC)"

.PHONY: build
build: ## Build the package (Poetry)
	@echo "$(BLUE)Building package...$(NC)"
	$(POETRY) build
	@echo "$(GREEN)Package built in dist/$(NC)"

.PHONY: publish
publish: ## Publish package to PyPI (Poetry)
	@echo "$(BLUE)Publishing package...$(NC)"
	$(POETRY) publish
	@echo "$(GREEN)Package published$(NC)"

.PHONY: status
status: ## Show project status
	@echo "$(BLUE)Project Status$(NC)"
	@echo "==============="
	@echo "Python version: $$($(POETRY) run python --version)"
	@echo "Poetry version: $$($(POETRY) --version)"
	@echo "Dependencies: $$(if [ -f pyproject.toml ]; then echo '$(GREEN)Configured$(NC)'; else echo '$(RED)Missing$(NC)'; fi)"
	@echo "Tests: $$(if [ -d $(TEST_DIR) ]; then echo '$(GREEN)Found$(NC)'; else echo '$(RED)Missing$(NC)'; fi)"
	@echo "Virtual environment: $$($(POETRY) env info --path)"