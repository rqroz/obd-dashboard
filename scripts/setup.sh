#!/bin/bash
cd $BASE_DIR
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
cd frontend/
npm install
