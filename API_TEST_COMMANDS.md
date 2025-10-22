# API Testing Commands

Quick reference for testing the String Analyzer API endpoints.

## Base Configuration

- **Local Development**: `http://127.0.0.1:8000`
- **Production (Sevalla)**: `https://your-domain.com`

---

## 1. Create/Analyze String (POST /strings)

### PowerShell (Windows)

```powershell
# Success case
$body = @{
    value = "string to analyze"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

### Curl (Git Bash / Linux / Mac)

```bash
# Success case
curl -X POST http://127.0.0.1:8000/strings/ \
  -H "Content-Type: application/json" \
  -d '{"value": "string to analyze"}'
```

### Expected Response (201 Created)

```json
{
  "id": "abc123def456...",
  "value": "string to analyze",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123def456...",
    "character_frequency_map": {
      "s": 2,
      "t": 3,
      "r": 2,
      "i": 1,
      "n": 2,
      "g": 1,
      " ": 2,
      "o": 1,
      "a": 2,
      "l": 1,
      "y": 1,
      "z": 1,
      "e": 1
    }
  },
  "created_at": "2025-10-22T03:30:00Z"
}
```

---

## 2. Error Cases

### 409 Conflict (Duplicate String)

```powershell
# PowerShell - Try to create the same string twice
$body = @{
    value = "string to analyze"
} | ConvertTo-Json

# First call returns 201, second call returns 409
Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Expected Response (409 Conflict)**:
```json
{
  "error": "String already exists",
  "existing_id": "abc123def456..."
}
```

### 400 Bad Request (Missing 'value' field)

```powershell
# PowerShell
$body = @{
    text = "wrong field name"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Expected Response (400 Bad Request)**:
```json
{
  "error": "Missing 'value' field in request body"
}
```

### 422 Unprocessable Entity (Invalid Data Type)

```powershell
# PowerShell
$body = @{
    value = 12345  # Should be string, not number
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "error": "Invalid data type for 'value'. Expected string."
}
```

---

## 3. Get String by Value (GET /strings?value=...)

### PowerShell

```powershell
# Get string by value
Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/?value=string to analyze" `
    -Method GET
```

### Curl

```bash
curl "http://127.0.0.1:8000/strings/?value=string%20to%20analyze"
```

---

## 4. List All Strings (GET /strings)

### PowerShell

```powershell
# List all strings
Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/" -Method GET

# With filters
Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/?is_palindrome=true&min_length=5" `
    -Method GET
```

### Curl

```bash
# List all
curl http://127.0.0.1:8000/strings/

# With filters
curl "http://127.0.0.1:8000/strings/?is_palindrome=true&min_length=5"
```

---

## 5. Natural Language Query (GET /strings/filter-by-natural-language)

### PowerShell

```powershell
$query = "palindromes longer than 10 characters"
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/filter-by-natural-language/?query=$encodedQuery" `
    -Method GET
```

### Curl

```bash
curl "http://127.0.0.1:8000/strings/filter-by-natural-language/?query=palindromes%20longer%20than%2010%20characters"
```

---

## 6. Delete String (DELETE /strings?value=...)

### PowerShell

```powershell
# Delete by value
Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/?value=string to analyze" `
    -Method DELETE
```

### Curl

```bash
curl -X DELETE "http://127.0.0.1:8000/strings/?value=string%20to%20analyze"
```

**Expected Response (204 No Content)**: Empty body

---

## Running the Python Test Script

### Install dependencies

```powershell
pip install requests
```

### Run tests

```powershell
# Test local server
python test_api_endpoint.py

# Test production (edit BASE_URL in the script first)
python test_api_endpoint.py
```

---

## Quick Verification Script

Save this as `quick_test.ps1`:

```powershell
# Quick API Test
$baseUrl = "http://127.0.0.1:8000"

Write-Host "Testing String Analyzer API..." -ForegroundColor Cyan

# Test 1: Create string
Write-Host "`n1. Creating string..." -ForegroundColor Yellow
$body = @{ value = "test string $(Get-Date -Format 'HHmmss')" } | ConvertTo-Json
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/strings/" -Method POST -Body $body -ContentType "application/json"
    Write-Host "   ✅ Created: $($response.value)" -ForegroundColor Green
    Write-Host "   ID: $($response.id)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: List strings
Write-Host "`n2. Listing strings..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/strings/" -Method GET
    Write-Host "   ✅ Found $($response.results.count) strings" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n✅ Tests complete!" -ForegroundColor Cyan
```

Run with:
```powershell
powershell -ExecutionPolicy Bypass -File quick_test.ps1
```

---

## Testing Production on Sevalla

Replace `http://127.0.0.1:8000` with your production URL in all commands above.

**Example**:
```powershell
# Production test
$body = @{
    value = "production test"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://your-domain.com/strings/" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

## Troubleshooting

### Error: "Connection refused"
- **Local**: Make sure Django server is running (`python manage.py runserver`)
- **Production**: Check if your Sevalla app is active

### Error: "404 Not Found"
- Check the URL path (should end with `/strings/`)
- Verify URL routing in `urls.py`

### Error: "500 Internal Server Error"
- Check Django logs: `python manage.py runserver` output
- On Sevalla: Check error logs in cPanel

### PowerShell TLS Error
```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

---

## Complete Test Workflow

```powershell
# 1. Start server (if not running)
python manage.py runserver

# 2. Run comprehensive tests
python test_api_endpoint.py

# 3. Or test individual endpoints manually
$body = @{ value = "my test string" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/strings/" -Method POST -Body $body -ContentType "application/json"
```
