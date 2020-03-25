#!/bin/bash
if [ "${ENVIRONMENT:=dev}" = "dev" ]; then
    python run.py
else
    gunicorn -c gunicorn.conf.py run:server
fi
