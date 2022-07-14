.PHONY: help
help:  ## Print this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: require
require: ## Check that prerequisites are installed.
	@if ! command -v python3 > /dev/null; then \
            printf "\033[1m\033[31mERROR\033[0m: python3 not installed\n" >&2 ; \
	    exit 1; \
	fi
	@if ! python3 -c "import sys; sys.exit(sys.version_info < (3,6))"; then \
            printf "\033[1m\033[31mERROR\033[0m: python 3.6+ required\n" >&2 ; \
	    exit 1; \
	fi
	@if ! command -v poetry > /dev/null; then \
	    printf "\033[1m\033[31mERROR\033[0m: poetry not installed.\n" >&2 ; \
	    printf "Please install with 'python3 -mpip install --user poetry'\n" >&2 ; \
	    exit 1; \
	fi

.PHONY: setup
setup:  require .setup_complete ## Set up the local development environment

.setup_complete:  poetry.lock ## Internal helper to run the setup.
	poetry install
	poetry run pre-commit install
	touch .setup_complete

.PHONY: test
test:  setup ## Run the tests, but only for current Python version
	poetry run tox -e py

.PHONY: test-all
test-all:  setup ## Run the tests for all relevant Python version
	poetry run tox

.PHONY: publish
publish:  setup ## Build & publish the new version
	poetry build
	poetry publish

.PHONY: format
format:  setup ## Autoformat all files in the repo. WARNING: changes files in-place
	poetry run black mm_language_server tests
	poetry run isort mm_language_server tests
	poetry run docformatter --recursive --in-place mm_language_server tests

.PHONY:  clean
clean: ## Remove local development environment
	if poetry env list | grep -q Activated; then \
	    poetry env remove python3; \
	fi
	rm -f .setup_complete
