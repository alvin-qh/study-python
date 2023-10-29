#!/usr/bin/env bash
set -e;

pdm run pytest -v -s tests;
