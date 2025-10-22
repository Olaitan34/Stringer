#!/bin/bash

# Sevalla Deployment Script
# This script automates the deployment process on Sevalla

echo "==================================="
echo "String Analyzer - Sevalla Deployment"
echo "==================================="

# Configuration - UPDATE THESE VALUES
USERNAME="your_username"
DOMAIN="yourdomain.com"
PROJECT_DIR="$HOME/string_analyzer"
VENV_DIR="$HOME/virtualenv/string_analyzer/3.9"

echo ""
echo "Configuration:"
echo "  Username: $USERNAME"
echo "  Domain: $DOMAIN"
echo "  Project Directory: $PROJECT_DIR"
echo "  Virtual Environment: $VENV_DIR"
echo ""

# Activate virtual environment
echo "[1/8] Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Navigate to project directory
echo "[2/8] Navigating to project directory..."
cd "$PROJECT_DIR"

# Pull latest code (if using Git)
echo "[3/8] Pulling latest code from Git..."
git pull origin main

# Install/update dependencies
echo "[4/8] Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "[5/8] Running database migrations..."
python manage.py migrate

# Collect static files
echo "[6/8] Collecting static files..."
python manage.py collectstatic --noinput

# Set correct permissions
echo "[7/8] Setting file permissions..."
chmod 755 passenger_wsgi.py
chmod -R 755 staticfiles/
chmod -R 755 logs/

# Restart application
echo "[8/8] Restarting application..."
mkdir -p tmp
touch tmp/restart.txt

echo ""
echo "==================================="
echo "Deployment Complete!"
echo "==================================="
echo ""
echo "Your application should now be live at:"
echo "https://$DOMAIN"
echo ""
echo "To check if it's working:"
echo "curl https://$DOMAIN/strings/"
echo ""
