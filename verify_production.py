#!/usr/bin/env python3
"""
Production Environment Verification Script
Run this on your Sevalla server to check if everything is configured correctly.
"""

import sys
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print()

# Check if required packages are installed
packages = [
    'django',
    'rest_framework',
    'decouple',
    'psycopg2',
    'dj_database_url',
    'whitenoise',
    'corsheaders',
    'gunicorn'
]

print("Checking installed packages:")
print("-" * 50)

for package in packages:
    try:
        if package == 'rest_framework':
            import rest_framework
            print(f"✅ djangorestframework: {rest_framework.__version__}")
        elif package == 'decouple':
            import decouple
            print(f"✅ python-decouple: installed")
        elif package == 'psycopg2':
            import psycopg2
            print(f"✅ psycopg2-binary: {psycopg2.__version__}")
        elif package == 'dj_database_url':
            import dj_database_url
            print(f"✅ dj-database-url: installed")
        elif package == 'whitenoise':
            import whitenoise
            print(f"✅ whitenoise: {whitenoise.__version__}")
        elif package == 'corsheaders':
            import corsheaders
            print(f"✅ django-cors-headers: installed")
        else:
            module = __import__(package)
            version = getattr(module, '__version__', 'installed')
            print(f"✅ {package}: {version}")
    except ImportError:
        print(f"❌ {package}: NOT INSTALLED")

print()
print("-" * 50)
print("Checking Django settings...")
print("-" * 50)

try:
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'string_analyzer.settings')
    
    import django
    django.setup()
    
    from django.conf import settings
    
    print(f"✅ Django settings loaded successfully")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"   DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
    print(f"   DATABASE NAME: {settings.DATABASES['default'].get('NAME', 'Not set')}")
    
except Exception as e:
    print(f"❌ Error loading Django settings: {e}")

print()
print("=" * 50)
print("Verification complete!")
