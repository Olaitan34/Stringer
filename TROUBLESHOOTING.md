# Troubleshooting Guide - String Analyzer Service

## Common Issues and Solutions

### 🐍 Python/Django Issues

#### Issue: "Import 'django' could not be resolved"
**Cause**: Django not installed or virtual environment not activated

**Solution**:
```bash
# Windows
.\env\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
source env/bin/activate
pip install -r requirements.txt
```

#### Issue: "ModuleNotFoundError: No module named 'rest_framework'"
**Cause**: Django REST Framework not installed

**Solution**:
```bash
pip install djangorestframework
# Or reinstall all dependencies
pip install -r requirements.txt
```

#### Issue: "SECRET_KEY environment variable not set"
**Cause**: Missing or incorrect .env file

**Solution**:
1. Copy `.env.example` to `.env`
2. Edit `.env` and set all required variables
3. Ensure `python-decouple` is installed: `pip install python-decouple`

---

### 🗄️ Database Issues

#### Issue: "django.db.utils.OperationalError: could not connect to server"
**Cause**: PostgreSQL not running or incorrect connection settings

**Solution**:
1. Check if PostgreSQL is running:
   ```bash
   # Windows
   sc query postgresql-x64-14
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Verify DATABASE_URL in `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

3. Test connection:
   ```bash
   psql -h localhost -U username -d dbname
   ```

#### Issue: "relation 'string_analysis' does not exist"
**Cause**: Database migrations not run

**Solution**:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Issue: "FATAL: password authentication failed"
**Cause**: Incorrect database credentials

**Solution**:
1. Reset PostgreSQL password:
   ```sql
   ALTER USER username WITH PASSWORD 'newpassword';
   ```

2. Update DATABASE_URL in `.env`

#### Issue: "duplicate key value violates unique constraint"
**Cause**: Trying to create a string that already exists

**Solution**: This is expected behavior (409 Conflict). Check if string exists before creating.

---

### 🌐 API Issues

#### Issue: 404 Not Found on all endpoints
**Cause**: URL configuration issue

**Solution**:
1. Check `string_analyzer/urls.py` includes strings_app urls:
   ```python
   path('', include('strings_app.urls')),
   ```

2. Verify server is running:
   ```bash
   python manage.py runserver
   ```

3. Access correct URL: `http://localhost:8000/strings/`

#### Issue: CORS errors in browser
**Cause**: Frontend domain not in CORS_ALLOWED_ORIGINS

**Solution**:
Add your frontend domain to `.env`:
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourfrontend.com
```

#### Issue: "Method Not Allowed" (405)
**Cause**: Using wrong HTTP method

**Solution**:
- POST /strings (not GET)
- GET /strings/ (not POST)
- DELETE /strings/value (not POST)

Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for correct methods.

#### Issue: "String not found" (404) but string exists
**Cause**: URL encoding issue or searching by hash instead of value

**Solution**:
- URL-encode special characters: `hello world` → `hello%20world`
- Use the actual string value, not the SHA-256 hash
- Example: `/strings/hello%20world` (correct) vs `/strings/b94d27b...` (incorrect)

---

### 🧪 Testing Issues

#### Issue: "No module named 'tests'"
**Cause**: Test file structure issue

**Solution**:
Ensure `strings_app/tests.py` exists (not `strings_app/tests/` directory)

#### Issue: Tests fail with database errors
**Cause**: Test database not configured

**Solution**:
Django automatically creates a test database. Ensure your DATABASE_URL user has permission to create databases:
```sql
ALTER USER username CREATEDB;
```

#### Issue: "AssertionError" in tests
**Cause**: Expected behavior changed

**Solution**:
1. Run specific test to see details:
   ```bash
   python manage.py test strings_app.tests.TestClassName.test_method_name --verbosity=2
   ```

2. Check test expectations match actual API behavior

---

### 🚀 Sevalla Deployment Issues

#### Issue: 500 Internal Server Error
**Cause**: Multiple possible causes

**Solutions**:
1. Check Passenger error log:
   ```bash
   tail -100 ~/logs/yourdomain.com/http/error.log
   ```

2. Check Django error log:
   ```bash
   tail -100 ~/string_analyzer/logs/django_errors.log
   ```

3. Verify Python interpreter path in `passenger_wsgi.py`:
   ```bash
   which python
   ```

4. Test settings manually:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   cd ~/string_analyzer
   python manage.py check
   ```

5. Common fixes:
   ```bash
   # Fix permissions
   chmod 755 ~/string_analyzer/passenger_wsgi.py
   
   # Restart application
   touch ~/string_analyzer/tmp/restart.txt
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

#### Issue: "Passenger application failed to start"
**Cause**: Syntax error or import error in passenger_wsgi.py

**Solution**:
1. Test passenger_wsgi.py directly:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   cd ~/string_analyzer
   python passenger_wsgi.py
   ```

2. Check for import errors:
   ```bash
   python -c "import django; print(django.get_version())"
   python -c "from decouple import config; print('OK')"
   ```

#### Issue: Static files not loading (CSS/images)
**Cause**: Static files not collected or incorrect configuration

**Solution**:
```bash
source ~/virtualenv/string_analyzer/3.9/bin/activate
cd ~/string_analyzer
python manage.py collectstatic --noinput
chmod -R 755 staticfiles/
touch tmp/restart.txt
```

#### Issue: Database connection fails on Sevalla
**Cause**: Incorrect DATABASE_URL or PostgreSQL not accessible

**Solution**:
1. Get correct database info from Sevalla cPanel
2. Test connection:
   ```bash
   psql -h localhost -U username_dbuser -d username_dbname
   ```

3. Update `.env` with correct credentials
4. Ensure PostgreSQL allows connections from your application

#### Issue: Application won't restart
**Cause**: Passenger restart mechanism not working

**Solutions**:
```bash
# Method 1: Touch restart.txt
mkdir -p ~/string_analyzer/tmp
touch ~/string_analyzer/tmp/restart.txt

# Method 2: Change passenger_wsgi.py
touch ~/string_analyzer/passenger_wsgi.py

# Method 3: Via cPanel
# Go to: Software → Setup Python App → Restart
```

---

### 📦 Installation Issues

#### Issue: "pip: command not found"
**Cause**: Python not installed correctly or not in PATH

**Solution**:
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

#### Issue: "psycopg2 installation fails"
**Cause**: PostgreSQL development headers missing

**Solution**:
```bash
# Use binary version (recommended)
pip install psycopg2-binary

# Or install PostgreSQL development headers
# Ubuntu/Debian
sudo apt-get install postgresql-dev libpq-dev

# macOS
brew install postgresql

# Windows
# Download PostgreSQL installer from postgresql.org
```

#### Issue: "error: Microsoft Visual C++ 14.0 is required" (Windows)
**Cause**: C++ build tools not installed

**Solution**:
1. Use binary packages when available: `pip install psycopg2-binary`
2. Or install Visual C++ Build Tools from Microsoft

---

### 🔧 Development Issues

#### Issue: "Port 8000 already in use"
**Cause**: Another application using port 8000

**Solution**:
```bash
# Use different port
python manage.py runserver 8001

# Or kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### Issue: Changes not reflected after code update
**Cause**: Django dev server needs restart or cached files

**Solution**:
1. Restart development server (Ctrl+C, then `python manage.py runserver`)
2. Clear Python cache:
   ```bash
   find . -type d -name "__pycache__" -exec rm -r {} +
   find . -type f -name "*.pyc" -delete
   ```

3. On Sevalla:
   ```bash
   touch ~/string_analyzer/tmp/restart.txt
   ```

---

### 🔒 Security/Permission Issues

#### Issue: "Permission denied" when running scripts
**Cause**: Script not executable

**Solution**:
```bash
# Linux/macOS
chmod +x setup.sh
chmod +x deploy_sevalla.sh

# Windows - use .bat files instead
setup.bat
```

#### Issue: ALLOWED_HOSTS validation failed
**Cause**: Domain not in ALLOWED_HOSTS

**Solution**:
Add your domain to `.env`:
```env
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost
```

---

## Debugging Tips

### Enable Debug Mode (Local Only!)
```env
# .env
DEBUG=True
```
**WARNING**: Never set `DEBUG=True` in production!

### Check Django Settings
```bash
python manage.py diffsettings
```

### Validate Models
```bash
python manage.py check
```

### View SQL Queries (Debug Mode)
```bash
python manage.py shell
>>> from django.db import connection
>>> connection.queries
```

### Test Database Connection
```bash
python manage.py dbshell
```

### View Logs in Real-Time
```bash
# Local
tail -f logs/django_errors.log

# Sevalla
tail -f ~/logs/yourdomain.com/http/error.log
```

---

## Getting Help

If you're still experiencing issues:

1. **Check the logs** - Error messages usually point to the problem
2. **Run tests** - `python manage.py test` can reveal issues
3. **Verify configuration** - Double-check `.env` and settings.py
4. **Review documentation**:
   - [README.md](README.md) - Setup and overview
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API usage
   - [SEVALLA_QUICK_REFERENCE.md](SEVALLA_QUICK_REFERENCE.md) - Deployment
5. **Check Django documentation** - https://docs.djangoproject.com/
6. **Check DRF documentation** - https://www.django-rest-framework.org/

---

## Emergency Fixes

### Nuclear Option 1: Fresh Virtual Environment
```bash
# Deactivate current environment
deactivate

# Delete and recreate
rm -rf env/
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
```

### Nuclear Option 2: Reset Database
```bash
# WARNING: This deletes all data!
python manage.py flush
python manage.py migrate
```

### Nuclear Option 3: Start Over (Last Resort)
```bash
# Backup your .env file first!
cp .env .env.backup

# Delete everything except source code
rm -rf env/ __pycache__/ */migrations/*
rm db.sqlite3

# Run setup again
# Windows: .\setup.bat
# Unix/Mac: ./setup.sh
```

---

## Prevention

To avoid issues:
- ✅ Always activate virtual environment before working
- ✅ Keep dependencies updated: `pip install --upgrade -r requirements.txt`
- ✅ Run migrations after model changes
- ✅ Test locally before deploying to Sevalla
- ✅ Keep backups of .env and database
- ✅ Use version control (Git) for code
- ✅ Monitor logs regularly
