# Sevalla Deployment Quick Reference

## Quick Commands

### Restart Application
```bash
touch ~/string_analyzer/tmp/restart.txt
```

### Check Logs
```bash
# Passenger error log
tail -f ~/logs/yourdomain.com/http/error.log

# Django error log
tail -f ~/string_analyzer/logs/django_errors.log
```

### Run Migrations
```bash
source ~/virtualenv/string_analyzer/3.9/bin/activate
cd ~/string_analyzer
python manage.py migrate
```

### Update Code from Git
```bash
cd ~/string_analyzer
git pull origin main
source ~/virtualenv/string_analyzer/3.9/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch ~/string_analyzer/tmp/restart.txt
```

## Important Paths (Replace 'username' with your actual username)

- **Project Root**: `~/string_analyzer`
- **Virtual Environment**: `~/virtualenv/string_analyzer/3.9`
- **Python Interpreter**: `~/virtualenv/string_analyzer/3.9/bin/python3`
- **Public HTML**: `~/public_html`
- **Logs**: `~/logs/yourdomain.com/http/`

## Environment Variables (.env file location)

```bash
~/string_analyzer/.env
```

## Database Connection String Format

```
DATABASE_URL=postgresql://username_dbuser:password@localhost:5432/username_dbname
```

## Testing the API After Deployment

```bash
# Health check (list all strings)
curl https://yourdomain.com/strings/

# Create test string
curl -X POST https://yourdomain.com/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "test"}'

# Get test string
curl https://yourdomain.com/strings/test

# Delete test string
curl -X DELETE https://yourdomain.com/strings/test
```

## Common Issues and Quick Fixes

### 500 Error
1. Check error logs
2. Verify DATABASE_URL in .env
3. Run: `python manage.py check`

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
chmod -R 755 ~/string_analyzer/staticfiles/
```

### Database Issues
```bash
# Test connection
psql -h localhost -U username_dbuser -d username_dbname

# Re-run migrations
python manage.py migrate --run-syncdb
```

### Application Won't Start
```bash
# Check passenger_wsgi.py Python path
which python

# Update passenger_wsgi.py if needed
nano ~/string_analyzer/passenger_wsgi.py

# Restart
touch ~/string_analyzer/tmp/restart.txt
```
