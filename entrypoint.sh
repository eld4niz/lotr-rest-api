#!/bin/bash
echo "Creating Migrations..."
python manage.py makemigrations --noinput
echo ====================================

echo "Starting Migrations..."
python manage.py migrate --noinput
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000