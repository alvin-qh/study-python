#!/usr/bin/env bash

if [[ ! -f "./.python-version" ]]; then
  echo "> Use python version 3.8.5..."
  pyenv local 3.8.5
fi

if [[ ! -d ".venv" ]]; then
  echo "> Create virtualenv..."
  python -m venv .venv --prompt="study-python-graphene-example"

  . .venv/bin/activate

  echo "> Install python requirement packages..."
  pip install -r requirements.txt
fi

echo "Python environment was setup."
