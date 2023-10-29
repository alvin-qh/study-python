#!/usr/bin/env bash

gunicorn -w 4 -k gevent -b 0.0.0.0:8899 --log-level=debug -c app.py app:app
