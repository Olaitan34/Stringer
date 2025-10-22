# 🎯 String Analyzer Service - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup (Choose Your Platform)

**Windows:**
```powershell
.\setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual:**
```bash
python -m venv env
source env/bin/activate  # Windows: .\env\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python manage.py migrate
python manage.py runserver
```

### Step 2: Configure Database

Edit `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/string_analyzer_db
SECRET_KEY=your-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 3: Test the API

```bash
# Create a string
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "hello world"}'

# Get the string
curl http://localhost:8000/strings/hello%20world

# List all strings
curl http://localhost:8000/strings/
```

---

## 📚 Documentation Quick Links

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [README.md](README.md) | Full setup & overview | First-time setup |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference | Using the API |
| [SEVALLA_QUICK_REFERENCE.md](SEVALLA_QUICK_REFERENCE.md) | Deployment commands | Deploying to Sevalla |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Problem solving | When issues occur |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview | Understanding structure |

---

## 🎯 API Endpoints Cheat Sheet

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/strings` | Create new string analysis |
| GET | `/strings/<value>` | Get specific string |
| GET | `/strings/` | List all (with filters) |
| GET | `/strings/filter-by-natural-language` | Natural language search |
| DELETE | `/strings/<value>` | Delete string |

---

## 🔍 Quick Examples

### Create & Analyze
```bash
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```
Returns: SHA-256 hash, palindrome status, character frequency, etc.

### Filter Palindromes
```bash
curl "http://localhost:8000/strings/?is_palindrome=true"
```

### Natural Language Query
```bash
curl "http://localhost:8000/strings/filter-by-natural-language?query=palindromic%20single%20word"
```

### Delete String
```bash
curl -X DELETE http://localhost:8000/strings/racecar
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test strings_app.tests.CreateStringAPITestCase
```

---

## 🌐 Sevalla Deployment (10 Steps)

1. **Create PostgreSQL database** in cPanel
2. **Upload files** via Git or FTP
3. **Create virtual environment**:
   ```bash
   python3.9 -m venv ~/virtualenv/string_analyzer/3.9
   ```
4. **Install dependencies**:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   pip install -r requirements.txt
   ```
5. **Create .env** with production settings
6. **Update passenger_wsgi.py** with your username
7. **Update .htaccess** with your username
8. **Run migrations**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
9. **Set permissions**:
   ```bash
   chmod 755 passenger_wsgi.py
   ```
10. **Restart application**:
    ```bash
    touch ~/string_analyzer/tmp/restart.txt
    ```

See [SEVALLA_QUICK_REFERENCE.md](SEVALLA_QUICK_REFERENCE.md) for details.

---

## 🔧 Common Commands

### Development
```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

### Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (WARNING: deletes data!)
python manage.py flush
```

### Sevalla
```bash
# Restart application
touch ~/string_analyzer/tmp/restart.txt

# Check logs
tail -f ~/logs/yourdomain.com/http/error.log

# Update code
cd ~/string_analyzer
git pull origin main
touch tmp/restart.txt
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Activate virtual environment |
| Database connection failed | Check .env DATABASE_URL |
| 404 on all endpoints | Verify server is running |
| 500 error on Sevalla | Check error logs |
| Tests failing | Ensure test database permissions |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

---

## 📦 Files Overview

### Core Files
- `manage.py` - Django management command
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create from .env.example)

### Configuration
- `string_analyzer/settings.py` - Django settings (Sevalla-ready)
- `string_analyzer/urls.py` - URL routing
- `passenger_wsgi.py` - Sevalla WSGI entry point
- `.htaccess` - Apache/Passenger config

### Application
- `strings_app/models.py` - StringAnalysis model
- `strings_app/views.py` - API endpoints
- `strings_app/serializers.py` - DRF serializers
- `strings_app/utils.py` - String analysis functions
- `strings_app/tests.py` - Test suite

### Documentation
- `README.md` - Main documentation
- `API_DOCUMENTATION.md` - API reference
- `SEVALLA_QUICK_REFERENCE.md` - Deployment guide
- `TROUBLESHOOTING.md` - Problem solving

### Tools
- `setup.bat` / `setup.sh` - Local setup scripts
- `deploy_sevalla.sh` - Deployment automation
- `postman_collection.json` - Postman API tests

---

## 💡 Tips

1. **Always activate virtual environment** before working:
   ```bash
   source env/bin/activate  # or .\env\Scripts\activate
   ```

2. **Test locally before deploying**:
   ```bash
   python manage.py test
   python manage.py runserver
   ```

3. **Use Postman collection** for API testing - import `postman_collection.json`

4. **Check logs when debugging**:
   - Local: `logs/django_errors.log`
   - Sevalla: `~/logs/yourdomain.com/http/error.log`

5. **Keep .env secure** - never commit to Git

---

## 🎯 Next Steps

### For Development
1. ✅ Run setup script
2. ✅ Configure .env
3. ✅ Run migrations
4. ✅ Start server
5. ✅ Test API endpoints

### For Deployment
1. ✅ Create Sevalla PostgreSQL database
2. ✅ Upload project files
3. ✅ Set up virtual environment
4. ✅ Configure .env on server
5. ✅ Run migrations
6. ✅ Test production API

---

## 📞 Need Help?

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review [README.md](README.md)
3. See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
4. Check Django docs: https://docs.djangoproject.com/
5. Open issue on GitHub

---

## ✨ You're Ready!

This project is **complete and production-ready**. Everything you need is included:

- ✅ All API endpoints working
- ✅ Complete test suite
- ✅ Sevalla deployment configs
- ✅ Comprehensive documentation
- ✅ Setup automation scripts
- ✅ Troubleshooting guides

**Start building!** 🚀
