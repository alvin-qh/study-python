#!/usr/bin/env bash

for DIR in ./*
do
    if [[ -d $DIR && $DIR != *_ && $DIR != *. ]];
    then
        echo "Check .py files in folder $DIR ..."
        flake8 $DIR
    fi
done