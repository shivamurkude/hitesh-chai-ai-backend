#!/usr/bin/env bash
# Start the application
gunicorn app.main:app --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker 