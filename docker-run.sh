#! /bin/sh

cd /isqlapi

# Create odbc config
envsubst < /isqlapi/odbc.ini.example > /etc/odbc.ini

# Source python venv
source venv/bin/activate

# Serve
gunicorn --bind 0.0.0.0:${ISQL_API_SERVER_PORT} wsgi:app