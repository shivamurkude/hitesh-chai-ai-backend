#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files (if any)
# python manage.py collectstatic --no-input

# Run migrations (if any)
# python manage.py migrate 