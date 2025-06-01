#!/usr/bin/env bash

poetry run mypy .
poetry run autopep8 .
poetry run pycln --config=pyproject.toml .

poetry run pytest
