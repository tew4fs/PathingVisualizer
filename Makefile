.DEFAULT_GOAL := build

run:
	pipenv run python pathingApp/gui.py

lint:
	pipenv run flake8 .

format:
	pipenv run black .

test:
	pipenv run pytest

pre-commit:
	pipenv run pre-commit install

build: pre-commit format lint run