#!/usr/bin/env bash

function travel() {
    for FILE in $1
    do
        if [[ -f "$FILE" && "$FILE" == *.py ]]
        then
            echo "Check $FILE ...";
            mypy "$FILE"
            flake8 "$FILE"
        elif [[ -d "$FILE" && ( "$FILE" != __* || "$FILE" != .* ) ]]
        then
            travel "$FILE/*"
        fi
    done
}

arg="./"

if [[ -n "$1" ]]
then
    arg="$1"
fi

travel "$arg"
