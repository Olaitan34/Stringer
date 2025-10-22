@echo off
REM Windows Setup Script for String Analyzer Service
REM This script automates the local setup process

echo ===================================
echo String Analyzer - Local Setup
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

echo [1/9] Python found: 
python --version
echo.

REM Create virtual environment
echo [2/9] Creating virtual environment...
if not exist "env" (
    python -m venv env
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo [3/9] Activating virtual environment...
call env\Scripts\activate.bat
echo.

REM Upgrade pip
echo [4/9] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [5/9] Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
echo [6/9] Setting up environment variables...
if not exist ".env" (
    copy .env.example .env
    echo Created .env file from .env.example
    echo IMPORTANT: Please edit .env and update the settings!
) else (
    echo .env file already exists.
)
echo.

REM Create logs directory
echo [7/9] Creating logs directory...
if not exist "logs" mkdir logs
echo.

REM Run migrations
echo [8/9] Running database migrations...
echo NOTE: Make sure PostgreSQL is running and .env is configured!
echo.
set /p continue="Continue with migrations? (Y/N): "
if /i "%continue%"=="Y" (
    python manage.py makemigrations
    python manage.py migrate
    echo.
    echo Migrations complete!
) else (
    echo Skipping migrations. Run manually later with:
    echo   python manage.py makemigrations
    echo   python manage.py migrate
)
echo.

REM Collect static files
echo [9/9] Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo Next steps:
echo 1. Edit .env file with your database settings
echo 2. Run migrations: python manage.py migrate
echo 3. Create superuser: python manage.py createsuperuser
echo 4. Start server: python manage.py runserver
echo.
echo To run tests:
echo   python manage.py test
echo.
pause
