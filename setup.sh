#!/bin/bash

# Unix/Linux/macOS Setup Script for String Analyzer Service
# This script automates the local setup process

echo "==================================="
echo "String Analyzer - Local Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "[1/9] Python found:"
python3 --version
echo ""

# Create virtual environment
echo "[2/9] Creating virtual environment..."
if [ ! -d "env" ]; then
    python3 -m venv env
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi
echo ""

# Activate virtual environment
echo "[3/9] Activating virtual environment..."
source env/bin/activate
echo ""

# Upgrade pip
echo "[4/9] Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "[5/9] Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create .env file if it doesn't exist
echo "[6/9] Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file from .env.example"
    echo "IMPORTANT: Please edit .env and update the settings!"
else
    echo ".env file already exists."
fi
echo ""

# Create logs directory
echo "[7/9] Creating logs directory..."
mkdir -p logs
echo ""

# Run migrations
echo "[8/9] Running database migrations..."
echo "NOTE: Make sure PostgreSQL is running and .env is configured!"
echo ""
read -p "Continue with migrations? (y/n): " continue
if [ "$continue" = "y" ] || [ "$continue" = "Y" ]; then
    python manage.py makemigrations
    python manage.py migrate
    echo ""
    echo "Migrations complete!"
else
    echo "Skipping migrations. Run manually later with:"
    echo "  python manage.py makemigrations"
    echo "  python manage.py migrate"
fi
echo ""

# Collect static files
echo "[9/9] Collecting static files..."
python manage.py collectstatic --noinput
echo ""

echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database settings"
echo "2. Run migrations: python manage.py migrate"
echo "3. Create superuser: python manage.py createsuperuser"
echo "4. Start server: python manage.py runserver"
echo ""
echo "To run tests:"
echo "  python manage.py test"
echo ""
