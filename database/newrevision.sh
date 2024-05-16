#!/usr/bin/env bash

if [[ -n $1 ]];then
    alembic revision -m "_${1}" --rev-id "`date +%Y%m%d_%H%M`"
else
    echo 'Please press migration comments.'
fi
