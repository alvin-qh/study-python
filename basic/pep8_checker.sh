#!/usr/bin/env bash

function travel() {
    for FILE in $1
    do
        echo $FILE
        # if [[ -f "$FILE" && "$FILE" == *.py ]];
        # then
            # echo "Check $FILE ..."
        # fi
    done
}

travel ./*
