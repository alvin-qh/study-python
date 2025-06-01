#!/usr/bin/env bash

uv run mypy .
uv run autopep8 .
uv run pycln --config=pyproject.toml .

uv run pytest
