#!/usr/bin/env bash

rm -rf .mypy_cache
rm -rf .pytest_cache
rm -rf .hypothesis
find . -name "__pycache__" | xargs -I{} rm -rf {}

