#!/usr/bin/env bash

poetry run pycln --config=pyproject.toml
poetry run autopep8 .

poetry run mypy

poetry run pytest
