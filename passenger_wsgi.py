"""
Passenger WSGI file for Sevalla deployment.
This file is used by Passenger (Sevalla's Python application server) to run Django.

IMPORTANT: Update the paths below with your actual Sevalla account username and paths.
"""
import sys
import os

# Path to your Python virtual environment
# Replace 'username' with your actual Sevalla username
INTERP = os.path.expanduser("~/virtualenv/string_analyzer/3.9/bin/python3")

# Check if we're using the correct Python interpreter
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add your project directory to the Python path
# Replace 'username' with your actual Sevalla username
sys.path.insert(0, os.path.expanduser('~/string_analyzer'))
sys.path.insert(0, os.path.expanduser('~/public_html'))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'string_analyzer.settings'

# Load environment variables from .env file
from pathlib import Path
env_path = Path.home() / 'string_analyzer' / '.env'
if env_path.exists():
    from decouple import Config, RepositoryEnv
    config = Config(RepositoryEnv(str(env_path)))

# Initialize Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
