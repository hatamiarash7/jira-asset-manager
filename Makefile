.PHONY: clean install lock build test help
.DEFAULT_GOAL := help

clean: ## Clean build files
	rm -rf dist

install: ## Install dependencies
	poetry install

lock: ## Update poetry.lock
	poetry lock

build: clean ## Build package
	poetry build

test: ## Run tests
	poetry run pytest

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'