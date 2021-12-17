DOCS_BUILD_DIR    ?= _build
DOC_TARGETS       ?= html

.PHONY: help
help: ## Print this help message and exit
	@echo Usage:
	@echo "  make [target]"
	@echo
	@echo Targets:
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "  %-30s %s\n", $$1, $$NF \
		 }' $(MAKEFILE_LIST)


.PHONY: build
build: ## Build the docker containers
	docker-compose \
		-f devstack/docker-compose.yaml \
		build

.PHONY: run
run: ## Run the docker containers
	docker-compose \
		-f devstack/docker-compose.yaml \
		up autoscaler

.PHONY: run-d
run-d: ## Run the docker containers
	docker-compose \
		-f devstack/docker-compose.yaml \
		up -d autoscaler

.PHONY: down
down: ## Stops the docker containers
	docker-compose \
		-f devstack/docker-compose.yaml \
		down


.PHONY: install
install:  ## Runs the pip install command to install all dependencies
	pip install -e .[all] && pre-commit install
