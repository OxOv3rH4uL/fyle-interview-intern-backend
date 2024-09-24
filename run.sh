#!/bin/bash
set -e
export FLASK_APP=core/server.py
gunicorn -c gunicorn_config.py core.server:app

