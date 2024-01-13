VENV := .venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python
SHELL := /bin/bash
PROJECT := blango
include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	python3 -m venv $(VENV) && source $(BIN)/activate

.PHONY: install
install: venv ## Make venv and install requirements
	$(BIN)/pip install --upgrade -r requirements.txt

freeze: ## Pin current dependencies
	$(BIN)/pip freeze > requirements.txt

migrate: ## Make and run migrations
	$(PYTHON) $(PROJECT)/manage.py makemigrations
	$(PYTHON)  $(PROJECT)/manage.py migrate


db-shell: ## Access the Postgres Docker database interactively with psql. Pass in DBNAME=<name>.
	docker exec -it container_name psql -d $(DBNAME)

.PHONY: test
test: ## Run tests
	coverage run  $(PROJECT)/manage.py test blog  --keepdb  --verbosity=2  --failfast    --force-color

.PHONY: run
run: ## Run the Django server
	$(PYTHON)  $(PROJECT)/manage.py runserver

start: install migrate run ## Install requirements, apply migrations, then start development server

report:
	@echo "Code coverage report:"
	coverage html2