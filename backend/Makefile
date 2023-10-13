BASH=bash -l -c
export PYTHONPATH := /code/src

.PHONY: Makefile

dc_%: #
	docker-compose run -w /code/ fastapi make $*

bash: #
	bash

poetry_install: ## Update packages
	poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

poetry_lock: #
	poetry lock --no-update

all: lint mypy test #

black-check: #
	black src/ --diff --check --color

isort-check: #
	isort src/ --diff --check --color

flake8-check: #
	flake8 src/

lint_full full_lint: lint mypy #

lint: black-check isort-check flake8-check

lint_fix: #
	black .
	isort .

mypy: #
	mypy src/ --show-error-codes --show-traceback --implicit-reexport


