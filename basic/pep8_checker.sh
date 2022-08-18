#!/usr/bin/env bash

for DIR in ./*
do
    if [[ -d $DIR && $DIR != *_ && $DIR != *. ]];
    then
        flake8 $DIR
    fi
done