#!/usr/bin/env bash
set -e;

# function travel() {
#     for FILE in $1
#     do
#         if [[ -f "$FILE" && "$FILE" == *.py ]]
#         then
#             echo "Check $FILE ...";
#             pdm run mypy "$FILE"
#             pdm run flake8 "$FILE"
#         elif [[ -d "$FILE" && ( "$FILE" != __* || "$FILE" != .* ) ]]
#         then
#             travel "$FILE/*"
#         fi
#     done
# }

# arg="./"

# if [[ -n "$1" ]]
# then
#     arg="$1"
# fi

# travel "$arg"

echo "Check type hits..."
pdm run mypy src

echo "Check code style check..."
pdm run autopep8 src tests
