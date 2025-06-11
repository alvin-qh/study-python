#/bin/env bash

pycln --config=pycln.cfg
autopep8 .

mypy

pytest
