#!/bin/bash

set -e

# python3 -m http.server --bind 0.0.0.0

python3 manage.py migrate --noinput
python3 manage.py runserver 0.0.0.0:8000
exec "$@"