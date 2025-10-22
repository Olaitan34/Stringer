# String Analyzer API - Complete Documentation

## Base URL
- **Local Development**: `http://localhost:8000`
- **Production (Sevalla)**: `https://yourdomain.com`

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/strings` | Create a new string analysis |
| GET | `/strings/<value>` | Get string analysis by value |
| GET | `/strings/` | List all strings (with optional filters) |
| GET | `/strings/filter-by-natural-language` | Filter using natural language |
| DELETE | `/strings/<value>` | Delete a string analysis |

---

## 1. Create String Analysis

**Endpoint**: `POST /strings`

**Description**: Analyzes a string and stores the results in the database.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "value": "string to analyze"
}
```

**Success Response** (201 Created):
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

**Error Responses**:

- **400 Bad Request** - Missing or empty value
```json
{
  "error": "The 'value' field is required."
}
```

- **409 Conflict** - String already exists
```json
{
  "error": "String already exists in the database."
}
```

- **422 Unprocessable Entity** - Invalid value type
```json
{
  "error": "Value must be a string."
}
```

**Examples**:

```bash
# cURL
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'

# Python
import requests
response = requests.post(
    "http://localhost:8000/strings",
    json={"value": "racecar"}
)

# JavaScript
fetch('http://localhost:8000/strings', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({value: 'racecar'})
})
```

---

## 2. Get String by Value

**Endpoint**: `GET /strings/<string_value>`

**Description**: Retrieves a string analysis by its actual value (not hash).

**URL Parameters**:
- `string_value` (required) - The string value (URL-encoded for special characters)

**Success Response** (200 OK):
```json
{
  "id": "hash...",
  "value": "hello world",
  "properties": { ... },
  "created_at": "2025-10-21T10:30:00.123456Z"
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "String not found."
}
```

**Examples**:

```bash
# Simple string
curl http://localhost:8000/strings/hello

# String with spaces (URL-encoded)
curl http://localhost:8000/strings/hello%20world

# String with special characters
curl http://localhost:8000/strings/hello%40world%21
```

---

## 3. List Strings with Filters

**Endpoint**: `GET /strings/`

**Description**: Lists all strings with optional filtering.

**Query Parameters** (all optional):

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `is_palindrome` | boolean | Filter by palindrome status | `true` or `false` |
| `min_length` | integer | Minimum string length | `5` |
| `max_length` | integer | Maximum string length | `10` |
| `word_count` | integer | Exact word count | `2` |
| `contains_character` | string | Single character to search for | `a` |

**Success Response** (200 OK):
```json
{
  "data": [
    {
      "id": "hash1...",
      "value": "racecar",
      "properties": { ... },
      "created_at": "2025-10-21T10:30:00Z"
    },
    {
      "id": "hash2...",
      "value": "noon",
      "properties": { ... },
      "created_at": "2025-10-21T10:31:00Z"
    }
  ],
  "count": 2,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 4
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "is_palindrome must be 'true' or 'false'."
}
```

**Examples**:

```bash
# Get all strings
curl http://localhost:8000/strings/

# Get all palindromes
curl "http://localhost:8000/strings/?is_palindrome=true"

# Get strings with 5-10 characters
curl "http://localhost:8000/strings/?min_length=5&max_length=10"

# Get single-word strings
curl "http://localhost:8000/strings/?word_count=1"

# Get strings containing 'a'
curl "http://localhost:8000/strings/?contains_character=a"

# Multiple filters
curl "http://localhost:8000/strings/?is_palindrome=true&word_count=1&min_length=4"
```

---

## 4. Natural Language Filter

**Endpoint**: `GET /strings/filter-by-natural-language`

**Description**: Filter strings using natural language queries.

**Query Parameters**:
- `query` (required) - Natural language query string

**Supported Phrases**:

| Phrase | Translates To | Example |
|--------|--------------|---------|
| "palindrome" or "palindromic" | `is_palindrome=true` | "palindrome" |
| "single word" | `word_count=1` | "single word" |
| "longer than X characters" | `min_length=X+1` | "longer than 5 characters" |
| "shorter than X" | `max_length=X-1` | "shorter than 10" |
| "contains letter X" | `contains_character=X` | "contains letter a" |
| "containing X" | `contains_character=X` | "containing z" |
| "first vowel" | `contains_character=a` | "first vowel" |

**Success Response** (200 OK):
```json
{
  "data": [ ... ],
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

**Error Responses**:

- **400 Bad Request** - Missing or unparseable query
```json
{
  "error": "The 'query' parameter is required."
}
```

- **422 Unprocessable Entity** - Conflicting filters
```json
{
  "error": "Conflicting filters: min_length cannot be greater than max_length.",
  "parsed_filters": {
    "min_length": 10,
    "max_length": 5
  }
}
```

**Examples**:

```bash
# Simple query
curl "http://localhost:8000/strings/filter-by-natural-language?query=palindrome"

# Complex query
curl "http://localhost:8000/strings/filter-by-natural-language?query=palindromic%20single%20word%20longer%20than%203%20characters"

# With character filter
curl "http://localhost:8000/strings/filter-by-natural-language?query=single%20word%20containing%20a"
```

---

## 5. Delete String

**Endpoint**: `DELETE /strings/<string_value>`

**Description**: Deletes a string analysis by its value.

**URL Parameters**:
- `string_value` (required) - The string value (URL-encoded)

**Success Response** (204 No Content):
- Empty body

**Error Response** (404 Not Found):
```json
{
  "error": "String not found."
}
```

**Examples**:

```bash
# Delete simple string
curl -X DELETE http://localhost:8000/strings/test

# Delete string with spaces
curl -X DELETE http://localhost:8000/strings/hello%20world

# Delete string with special characters
curl -X DELETE http://localhost:8000/strings/test%40example%21
```

---

## Response Field Descriptions

### String Analysis Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | SHA-256 hash of the string (primary key) |
| `value` | string | The original string |
| `properties` | object | Computed properties of the string |
| `created_at` | string | ISO 8601 timestamp of creation |

### Properties Object

| Field | Type | Description |
|-------|------|-------------|
| `length` | integer | Total character count including spaces |
| `is_palindrome` | boolean | Whether the string is a palindrome (case-insensitive, ignoring spaces) |
| `unique_characters` | integer | Count of unique characters |
| `word_count` | integer | Number of words (split by whitespace) |
| `sha256_hash` | string | SHA-256 hash of the string |
| `character_frequency_map` | object | Dictionary of each character and its frequency |

---

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET request |
| 201 | Created | String successfully created |
| 204 | No Content | String successfully deleted |
| 400 | Bad Request | Invalid request data or parameters |
| 404 | Not Found | String not found |
| 409 | Conflict | String already exists |
| 422 | Unprocessable Entity | Invalid data type or conflicting filters |

---

## Common Use Cases

### 1. Check if a string is a palindrome
```bash
# Create and check
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'

# The response will show "is_palindrome": true
```

### 2. Find all palindromes in database
```bash
curl "http://localhost:8000/strings/?is_palindrome=true"
```

### 3. Analyze character frequency
```bash
# Create string
curl -X POST http://localhost:8000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "hello"}'

# Response includes character_frequency_map: {"h": 1, "e": 1, "l": 2, "o": 1}
```

### 4. Find short single-word strings
```bash
curl "http://localhost:8000/strings/?word_count=1&max_length=5"
```

### 5. Complex natural language search
```bash
curl "http://localhost:8000/strings/filter-by-natural-language?query=palindromic%20single%20word%20shorter%20than%2010%20containing%20a"
```

---

## Error Handling Best Practices

1. **Always check HTTP status codes** before parsing response
2. **Handle 409 Conflict** by checking if string exists before creating
3. **URL-encode string values** when using in URLs
4. **Validate input** before sending to API
5. **Parse error messages** from response body for user-friendly feedback

---

## Rate Limiting (Production)

Currently, there is no rate limiting implemented. For production deployment, consider:
- Implementing `django-ratelimit`
- Setting limits per IP or user
- Recommended: 100 requests per minute per IP

---

## CORS Configuration

The API is configured with CORS headers. Update `CORS_ALLOWED_ORIGINS` in `.env` for your frontend domain:

```env
CORS_ALLOWED_ORIGINS=https://yourfrontend.com,https://www.yourfrontend.com
```

---

## Testing the API

### Using cURL
See examples above in each endpoint section.

### Using Postman
Import the `postman_collection.json` file included in the project.

### Using Python
```python
import requests

BASE_URL = "http://localhost:8000"

# Create
response = requests.post(f"{BASE_URL}/strings", json={"value": "test"})
print(response.json())

# Get
response = requests.get(f"{BASE_URL}/strings/test")
print(response.json())

# List with filters
response = requests.get(f"{BASE_URL}/strings/", params={"is_palindrome": "true"})
print(response.json())

# Delete
response = requests.delete(f"{BASE_URL}/strings/test")
print(response.status_code)  # Should be 204
```

---

## Need Help?

- Check the main [README.md](README.md) for setup instructions
- See [SEVALLA_QUICK_REFERENCE.md](SEVALLA_QUICK_REFERENCE.md) for deployment help
- Run tests: `python manage.py test`
- Check logs for errors (see logs/ directory)
