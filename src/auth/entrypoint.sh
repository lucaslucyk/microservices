#!/bin/bash

APP_PORT=${PORT:-8000}
poetry run gunicorn -k "uvicorn.workers.UvicornWorker" --chdir "./api" --bind "0.0.0.0:${APP_PORT}" main:app