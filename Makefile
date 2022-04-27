VERSION = $(shell grep -oE "[0-9]+\.[0-9]+\.[0-9]+" jumparound/__init__.py)

.PHONLY: test
test:
	@poetry run pytest -s

lint:
	@poetry run isort .
	@poetry run black .

setup:
	./scripts/setup-hooks.sh
	@poetry install
