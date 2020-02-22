#!/bin/bash
BACKEND_SCREEN="obd_dashboard_backend"
FRONTEND_SCREEN="obd_dashboard_frontend"

cd $BASE_DIR
source .venv/bin/activate

screen -S $BACKEND_SCREEN -X quit
screen -S $BACKEND_SCREEN -dm bash -c "./manage.py runserver"

screen -S $FRONTEND_SCREEN -X quit
screen -S $FRONTEND_SCREEN -dm bash -c "cd frontend; npm run serve"

screen -ls
