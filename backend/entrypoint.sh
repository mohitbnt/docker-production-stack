#!/bin/sh

set -e

echo "========================================"
echo "Starting OpsPortal Backend"
echo "========================================"

echo "Waiting for PostgreSQL..."

MAX_RETRIES=30
COUNT=0

until pg_isready \
    -h "$POSTGRES_HOST" \
    -p "$POSTGRES_PORT" \
    -U "$POSTGRES_USER"
do
    COUNT=$((COUNT + 1))

    if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
        echo "ERROR: PostgreSQL did not become ready."
        exit 1
    fi

    sleep 2
done

echo "PostgreSQL is ready."

echo "Running application seed..."

python -m app.seed

echo "Starting Gunicorn..."

exec gunicorn -c gunicorn_conf.py wsgi:app