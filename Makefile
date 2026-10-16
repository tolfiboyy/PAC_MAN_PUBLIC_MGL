CONFIG ?= config.json
VENV = PacmanEnv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
PYINSTALLER = $(VENV)/bin/pyinstaller

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) pac-man.py $(CONFIG)

debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	$(FLAKE8) . --exclude=PacmanEnv,build,dist,.git,__pycache__
	$(MYPY) . \
	--exclude '^(PacmanEnv|build|dist)' \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(FLAKE8) . --exclude=PacmanEnv,build,dist,.git,__pycache__
	$(MYPY) . --exclude '^(PacmanEnv|build|dist)/' --strict

package:
	$(PYINSTALLER) --clean pacman.spec
	cp $(CONFIG) dist/pacman/
	cp .itch.toml dist/pacman/
	cp INSTRUCTIONS.txt dist/pacman/

clean_build:
	rm -rf build dist

clean_env:
	rm -rf $(VENV)

.PHONY: install run debug clean lint lint-strict package clean_build clean_env
