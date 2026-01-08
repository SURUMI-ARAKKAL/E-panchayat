#!/bin/bash

echo "Setting up Panchayat Survey System..."
echo ""

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Creating database migrations..."
python manage.py makemigrations

echo ""
echo "Applying migrations..."
python manage.py migrate

echo ""
echo "Setup complete!"
echo ""
echo "To create an admin user, run: python manage.py createsuperuser"
echo "To start the server, run: python manage.py runserver"

