#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

pip list

poetry run pip list

poetry run python manage.py migrate --no-input
poetry run python manage.py collectstatic --noinput
poetry run python manage.py runserver 0.0.0.0:8000 --noreload --nothreading
