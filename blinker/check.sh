#!/usr/bin/env bash
set -e;

echo "Check type hits..."
pdm run mypy src

echo "Check code style check..."
pdm run autopep8 src tests
