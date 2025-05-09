#/bin/env bash

mypy
autopep8 .
pycln --config=pycln.cfg

pytest
