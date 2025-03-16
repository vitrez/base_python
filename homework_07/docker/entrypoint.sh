#!/usr/bin/env bash

echo "Applying migrations..."
alembic upgrade head
echo "Applied migrations!"

echo "Data download and fill DB..."
python crud.py
echo "DB full!"

exec "$@"
