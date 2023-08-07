.PHONY: clean shell install lock build init test help
.DEFAULT_GOAL := help

clean: ## Clean build files
	rm -rf dist

shell: ## Activate virtualenv
	poetry shell

install: ## Install dependencies
	poetry install

lock: ## Update poetry.lock
	poetry lock

build: clean ## Build package
	poetry build

init: ## Run the application - Initialize JIRA
	JIRA_SERVER="" JIRA_PAT="" jira-amt init

test: ## Run tests
	poetry run pytest

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'