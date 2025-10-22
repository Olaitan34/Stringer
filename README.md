# String Analyzer Service - Django REST API

A powerful Django REST API service for analyzing strings with support for palindrome detection, character frequency analysis, and natural language query filtering. Optimized for deployment on Sevalla (cPanel-based hosting with Passenger WSGI).

## 🎯 Features

- **String Analysis**: Automatically compute length, palindrome status, unique characters, word count, SHA-256 hash, and character frequency map
- **RESTful API**: 5 comprehensive endpoints for CRUD operations and filtering
- **Natural Language Queries**: Filter strings using natural language (e.g., "palindromic single word")
- **PostgreSQL Database**: Production-ready with optimized indexes
- **Sevalla Deployment Ready**: Pre-configured for Passenger WSGI on cPanel hosting
- **Comprehensive Tests**: Full test coverage for all endpoints and edge cases

## 🛠 Tech Stack

- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL (Sevalla-compatible)
- **WSGI Server**: Gunicorn (local) / Passenger (Sevalla)
- **Static Files**: WhiteNoise
- **Environment**: python-decouple for configuration
- **CORS**: django-cors-headers

## 📋 API Endpoints

### 1. Create String Analysis
```http
POST /strings
Content-Type: application/json

{
  "value": "hello world"
}
```

**Response (201 Created):**
```json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 3,
      "o": 2,
      " ": 1,
      "w": 1,
      "r": 1,
      "d": 1
    }
  },
  "created_at": "2025-10-21T10:30:00.123456Z"
}
```

**Error Responses:**
- `400 Bad Request`: Missing or empty value
- `409 Conflict`: String already exists
- `422 Unprocessable Entity`: Invalid value type

### 2. Get String by Value
```http
GET /strings/hello%20world
```

**Response (200 OK):** Same format as POST response

**Error Responses:**
- `404 Not Found`: String not found

### 3. List Strings with Filters
```http
GET /strings/?is_palindrome=true&min_length=5&word_count=1
```

**Query Parameters:**
- `is_palindrome`: boolean ("true" or "false")
- `min_length`: integer (filter length >= value)
- `max_length`: integer (filter length <= value)
- `word_count`: integer (exact match)
- `contains_character`: single character

**Response (200 OK):**
```json
{
  "data": [/* array of string objects */],
  "count": 5,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "word_count": 1
  }
}
```

### 4. Natural Language Filter
```http
GET /strings/filter-by-natural-language?query=palindromic single word longer than 3 characters
```

**Supported Phrases:**
- "palindrome" / "palindromic" → `is_palindrome=true`
- "single word" → `word_count=1`
- "longer than X characters" → `min_length=X+1`
- "shorter than X" → `max_length=X-1`
- "contains letter X" → `contains_character=X`
- "first vowel" → `contains_character=a`

**Response (200 OK):**
```json
{
  "data": [/* array of string objects */],
  "count": 3,
  "interpreted_query": {
    "original_query": "palindromic single word longer than 3 characters",
    "parsed_filters": {
      "is_palindrome": true,
      "word_count": 1,
      "min_length": 4
    }
  }
}
```

### 5. Delete String
```http
DELETE /strings/hello%20world
```

**Response (204 No Content):** Empty body

**Error Responses:**
- `404 Not Found`: String not found

## 🚀 Local Setup Instructions

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Olaitan34/Stringer.git
   cd Stringer
   ```

2. **Create and activate virtual environment**
   
   **Windows:**
   ```powershell
   python -m venv env
   .\env\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   
   Create a PostgreSQL database:
   ```sql
   CREATE DATABASE string_analyzer_db;
   CREATE USER string_analyzer_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE string_analyzer_db TO string_analyzer_user;
   ```

5. **Configure environment variables**
   
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your settings:
   ```env
   SECRET_KEY=your-very-secret-key-here-change-this
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgresql://string_analyzer_user:your_password@localhost:5432/string_analyzer_db
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   ```

6. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```
   
   The API will be available at: `http://127.0.0.1:8000/`

## 🧪 Running Tests

Run the comprehensive test suite:

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test strings_app.tests.CreateStringAPITestCase

# Run with coverage (install coverage first: pip install coverage)
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## 🌐 Sevalla Deployment Guide

Sevalla is a cPanel-based hosting provider that uses **Passenger WSGI** to run Python applications. Follow these steps for deployment.

### Prerequisites

- Active Sevalla hosting account
- SSH access enabled
- PostgreSQL database access in cPanel
- FTP/SFTP client or Git access

### Step 1: Create PostgreSQL Database on Sevalla

1. Log in to your Sevalla cPanel
2. Navigate to **Databases** → **PostgreSQL Databases**
3. Create a new database (e.g., `username_string_analyzer`)
4. Create a database user with a strong password
5. Add the user to the database with ALL PRIVILEGES
6. Note down the connection details:
   - Database name: `username_string_analyzer`
   - Username: `username_dbuser`
   - Password: `your_password`
   - Host: `localhost` (or provided by Sevalla)
   - Port: `5432`

### Step 2: Upload Project Files

**Option A: Using Git (Recommended)**

1. SSH into your Sevalla server:
   ```bash
   ssh username@yourdomain.com
   ```

2. Navigate to your home directory:
   ```bash
   cd ~
   ```

3. Clone your repository:
   ```bash
   git clone https://github.com/Olaitan34/Stringer.git string_analyzer
   cd string_analyzer
   ```

**Option B: Using FTP/SFTP**

1. Connect to your Sevalla server via FTP/SFTP
2. Upload all project files to `/home/username/string_analyzer/`
3. Ensure all files are uploaded, including hidden files (`.env`, `.htaccess`)

### Step 3: Set Up Python Virtual Environment

1. SSH into your Sevalla server
2. Create a Python virtual environment:
   ```bash
   cd ~/string_analyzer
   python3.9 -m venv ~/virtualenv/string_analyzer/3.9
   ```

3. Activate the virtual environment:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   ```

4. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

5. Install project dependencies:
   ```bash
   cd ~/string_analyzer
   pip install -r requirements.txt
   ```

### Step 4: Configure Environment Variables

1. Create `.env` file in the project root:
   ```bash
   cd ~/string_analyzer
   nano .env
   ```

2. Add your production settings:
   ```env
   SECRET_KEY=your-very-secret-production-key-change-this-to-random-string
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   
   # PostgreSQL Database URL from Sevalla cPanel
   DATABASE_URL=postgresql://username_dbuser:your_password@localhost:5432/username_string_analyzer
   
   # CORS (if you have a frontend)
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   
   # Security Settings
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

3. Save and exit (Ctrl+X, then Y, then Enter)

### Step 5: Configure Passenger WSGI

1. Edit `passenger_wsgi.py` with your actual paths:
   ```bash
   nano ~/string_analyzer/passenger_wsgi.py
   ```

2. Update these lines (replace `username` with your actual Sevalla username):
   ```python
   INTERP = os.path.expanduser("~/virtualenv/string_analyzer/3.9/bin/python3")
   sys.path.insert(0, os.path.expanduser('~/string_analyzer'))
   ```

3. Verify the Python interpreter path:
   ```bash
   which python
   # Should output something like: /home/username/virtualenv/string_analyzer/3.9/bin/python3
   ```

### Step 6: Configure .htaccess

1. Edit `.htaccess` with your actual username:
   ```bash
   cd ~/public_html
   nano .htaccess
   ```

2. Add this configuration (replace `username` with your Sevalla username):
   ```apache
   PassengerPython /home/username/virtualenv/string_analyzer/3.9/bin/python3
   PassengerAppRoot /home/username/string_analyzer
   PassengerEnabled On
   PassengerStartupFile passenger_wsgi.py
   PassengerAppEnv production
   PassengerMinInstances 1
   PassengerMaxPoolSize 6
   PassengerFriendlyErrorPages off
   
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteRule ^(.*)$ /passenger_wsgi.py/$1 [QSA,L]
   ```

3. **Alternative**: Create a symlink from public_html to your app:
   ```bash
   cd ~/public_html
   ln -s ~/string_analyzer/passenger_wsgi.py passenger_wsgi.py
   ```

### Step 7: Run Database Migrations

1. SSH into your server and activate the virtual environment:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   cd ~/string_analyzer
   ```

2. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Create superuser (optional, for Django admin):
   ```bash
   python manage.py createsuperuser
   ```

### Step 8: Set Correct Permissions

```bash
cd ~/string_analyzer
chmod 755 passenger_wsgi.py
chmod -R 755 staticfiles/
chmod -R 755 logs/
```

### Step 9: Restart the Application

**Method 1: Touch restart.txt (Recommended)**
```bash
mkdir -p ~/string_analyzer/tmp
touch ~/string_analyzer/tmp/restart.txt
```

**Method 2: Via cPanel**
1. Log in to cPanel
2. Navigate to **Software** → **Setup Python App**
3. Find your application and click **Restart**

### Step 10: Test Your Deployment

1. Visit your domain: `https://yourdomain.com/strings/`
2. Test the API endpoints:
   ```bash
   # Create a string
   curl -X POST https://yourdomain.com/strings \
     -H "Content-Type: application/json" \
     -d '{"value": "hello world"}'
   
   # List strings
   curl https://yourdomain.com/strings/
   
   # Get specific string
   curl https://yourdomain.com/strings/hello%20world
   ```

## 🔧 Sevalla Troubleshooting Guide

### Issue 1: 500 Internal Server Error

**Possible Causes:**
- Incorrect Python interpreter path in `passenger_wsgi.py`
- Missing or incorrect `.env` file
- Database connection issues

**Solutions:**
1. Check error logs:
   ```bash
   tail -f ~/logs/yourdomain.com/http/error.log
   ```

2. Verify Python path:
   ```bash
   which python
   ```

3. Test database connection:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   cd ~/string_analyzer
   python manage.py dbshell
   ```

4. Check settings.py loads correctly:
   ```bash
   python manage.py check
   ```

### Issue 2: Passenger Not Starting

**Solutions:**
1. Verify `.htaccess` configuration
2. Check file permissions:
   ```bash
   chmod 755 ~/string_analyzer/passenger_wsgi.py
   ```

3. Restart Passenger:
   ```bash
   touch ~/string_analyzer/tmp/restart.txt
   ```

4. Check Passenger log:
   ```bash
   tail -f ~/passenger.log
   ```

### Issue 3: Database Connection Refused

**Solutions:**
1. Verify DATABASE_URL in `.env`:
   ```bash
   cat ~/string_analyzer/.env | grep DATABASE_URL
   ```

2. Test PostgreSQL connection:
   ```bash
   psql -h localhost -U username_dbuser -d username_string_analyzer
   ```

3. Check PostgreSQL is running:
   ```bash
   ps aux | grep postgres
   ```

### Issue 4: Static Files Not Loading

**Solutions:**
1. Run collectstatic again:
   ```bash
   source ~/virtualenv/string_analyzer/3.9/bin/activate
   cd ~/string_analyzer
   python manage.py collectstatic --noinput
   ```

2. Verify static files directory permissions:
   ```bash
   chmod -R 755 ~/string_analyzer/staticfiles/
   ```

3. Check WhiteNoise is installed:
   ```bash
   pip list | grep whitenoise
   ```

### Issue 5: Application Not Restarting

**Solutions:**
1. Use restart.txt:
   ```bash
   touch ~/string_analyzer/tmp/restart.txt
   ```

2. Restart via cPanel Python App Manager

3. If all else fails, restart the entire server (contact Sevalla support)

### Checking Error Logs

**Passenger Error Log:**
```bash
tail -100 ~/logs/yourdomain.com/http/error.log
```

**Django Application Log:**
```bash
tail -100 ~/string_analyzer/logs/django_errors.log
```

**PostgreSQL Log:**
```bash
tail -100 /var/log/postgresql/postgresql-*.log
```

## 📊 Database Schema

```sql
CREATE TABLE string_analysis (
    id VARCHAR(64) PRIMARY KEY,  -- SHA-256 hash
    value TEXT UNIQUE NOT NULL,
    length INTEGER NOT NULL,
    is_palindrome BOOLEAN NOT NULL DEFAULT FALSE,
    unique_characters INTEGER NOT NULL,
    word_count INTEGER NOT NULL,
    sha256_hash VARCHAR(64) NOT NULL,
    character_frequency_map JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE INDEX idx_string_analysis_value ON string_analysis(value);
CREATE INDEX idx_string_analysis_is_palindrome ON string_analysis(is_palindrome);
CREATE INDEX idx_string_analysis_length ON string_analysis(length);
CREATE INDEX idx_string_analysis_word_count ON string_analysis(word_count);
```

## 📝 Example API Usage

### Using cURL

```bash
# Create a new string
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'

# Get string by value
curl http://localhost:8000/strings/racecar

# List palindromes
curl "http://localhost:8000/strings/?is_palindrome=true"

# Natural language query
curl "http://localhost:8000/strings/filter-by-natural-language?query=palindromic%20single%20word"

# Delete string
curl -X DELETE http://localhost:8000/strings/racecar
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create string
response = requests.post(
    f"{BASE_URL}/strings",
    json={"value": "hello world"}
)
print(response.json())

# List strings with filters
response = requests.get(
    f"{BASE_URL}/strings/",
    params={
        "is_palindrome": "false",
        "min_length": 5,
        "word_count": 2
    }
)
print(response.json())

# Natural language query
response = requests.get(
    f"{BASE_URL}/strings/filter-by-natural-language",
    params={"query": "palindrome longer than 5 characters"}
)
print(response.json())
```

### Using JavaScript fetch

```javascript
// Create string
fetch('http://localhost:8000/strings', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ value: 'hello world' })
})
  .then(response => response.json())
  .then(data => console.log(data));

// List strings
fetch('http://localhost:8000/strings/?is_palindrome=true')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔒 Security Considerations

- Always use strong `SECRET_KEY` in production
- Enable HTTPS in production (Sevalla provides free SSL certificates)
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Regularly update dependencies: `pip install --upgrade -r requirements.txt`
- Implement rate limiting for production (consider django-ratelimit)
- Use PostgreSQL with strong passwords
- Restrict `ALLOWED_HOSTS` to your domain only

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Olaitan34**
- GitHub: [@Olaitan34](https://github.com/Olaitan34)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact Sevalla support for hosting-related issues
- Check Django documentation: https://docs.djangoproject.com/
- Check DRF documentation: https://www.django-rest-framework.org/

## 🎉 Acknowledgments

- Django and Django REST Framework teams
- Sevalla hosting platform
- PostgreSQL community
- All contributors and testers
