# 🏗️ String Analyzer - Architecture & Flow Diagrams

## 📊 Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT (Browser/cURL/Postman)           │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/HTTPS Requests
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Sevalla Hosting                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Apache Web Server                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │         Passenger WSGI Server                   │  │  │
│  │  │  ┌──────────────────────────────────────────┐  │  │  │
│  │  │  │     Django Application                    │  │  │  │
│  │  │  │  ┌────────────────────────────────────┐  │  │  │  │
│  │  │  │  │  Django REST Framework             │  │  │  │  │
│  │  │  │  │  ┌──────────────────────────────┐  │  │  │  │  │
│  │  │  │  │  │    strings_app Views         │  │  │  │  │  │
│  │  │  │  │  │  - create_string()           │  │  │  │  │  │
│  │  │  │  │  │  - string_detail()           │  │  │  │  │  │
│  │  │  │  │  │  - list_strings()            │  │  │  │  │  │
│  │  │  │  │  │  - filter_natural_language() │  │  │  │  │  │
│  │  │  │  │  └──────────────┬───────────────┘  │  │  │  │  │
│  │  │  │  │                 │                   │  │  │  │  │
│  │  │  │  │  ┌──────────────▼───────────────┐  │  │  │  │  │
│  │  │  │  │  │    Serializers               │  │  │  │  │  │
│  │  │  │  │  │  - StringAnalysisSerializer  │  │  │  │  │  │
│  │  │  │  │  └──────────────┬───────────────┘  │  │  │  │  │
│  │  │  │  │                 │                   │  │  │  │  │
│  │  │  │  │  ┌──────────────▼───────────────┐  │  │  │  │  │
│  │  │  │  │  │    Models (ORM)              │  │  │  │  │  │
│  │  │  │  │  │  - StringAnalysis            │  │  │  │  │  │
│  │  │  │  │  └──────────────┬───────────────┘  │  │  │  │  │
│  │  │  │  │                 │                   │  │  │  │  │
│  │  │  │  │  ┌──────────────▼───────────────┐  │  │  │  │  │
│  │  │  │  │  │    Utility Functions         │  │  │  │  │  │
│  │  │  │  │  │  - analyze_string()          │  │  │  │  │  │
│  │  │  │  │  │  - compute_sha256()          │  │  │  │  │  │
│  │  │  │  │  └──────────────────────────────┘  │  │  │  │  │
│  │  │  │  └────────────────────────────────────┘  │  │  │  │
│  │  │  └──────────────────────────────────────────┘  │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ SQL Queries
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                  PostgreSQL Database                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Table: string_analysis                               │  │
│  │  - id (VARCHAR 64, PRIMARY KEY)                       │  │
│  │  - value (TEXT, UNIQUE, INDEXED)                      │  │
│  │  - length (INTEGER, INDEXED)                          │  │
│  │  - is_palindrome (BOOLEAN, INDEXED)                   │  │
│  │  - word_count (INTEGER, INDEXED)                      │  │
│  │  - unique_characters (INTEGER)                        │  │
│  │  - sha256_hash (VARCHAR 64)                           │  │
│  │  - character_frequency_map (JSONB)                    │  │
│  │  - created_at (TIMESTAMP)                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow Diagrams

### 1. Create String Flow (POST /strings)

```
Client Request
    │
    ├─► POST /strings
    │   Body: {"value": "hello world"}
    │
    ▼
Django URL Router (urls.py)
    │
    ▼
create_string() View
    │
    ├─► Validate request data
    │   └─► Check "value" field exists
    │
    ├─► StringAnalysisSerializer
    │   ├─► Validate value is string
    │   └─► Check value is not empty
    │
    ├─► Check for duplicates
    │   └─► Query DB for existing value
    │       ├─► EXISTS → Return 409 Conflict
    │       └─► NOT EXISTS → Continue
    │
    ├─► analyze_string() utility
    │   ├─► Calculate length
    │   ├─► Check palindrome (case-insensitive)
    │   ├─► Count unique characters
    │   ├─► Count words
    │   ├─► Generate SHA-256 hash
    │   └─► Build character frequency map
    │
    ├─► Create StringAnalysis instance
    │   └─► Set id = sha256_hash
    │
    ├─► Save to database
    │   └─► INSERT INTO string_analysis...
    │
    ▼
Response: 201 Created
    └─► JSON with id, value, properties, created_at
```

### 2. Get String Flow (GET /strings/<value>)

```
Client Request
    │
    ├─► GET /strings/hello%20world
    │
    ▼
Django URL Router
    │
    ├─► URL decode: "hello%20world" → "hello world"
    │
    ▼
string_detail() View
    │
    ├─► Query database
    │   └─► SELECT * FROM string_analysis
    │       WHERE value = 'hello world'
    │
    ├─► Found?
    │   ├─► YES → Serialize and return 200 OK
    │   └─► NO → Return 404 Not Found
    │
    ▼
Response: 200 OK or 404 Not Found
```

### 3. List with Filters Flow (GET /strings/?is_palindrome=true&min_length=5)

```
Client Request
    │
    ├─► GET /strings/?is_palindrome=true&min_length=5
    │
    ▼
list_strings() View
    │
    ├─► Parse query parameters
    │   ├─► is_palindrome="true" → boolean True
    │   ├─► min_length="5" → integer 5
    │   ├─► Validate types
    │   │   └─► Invalid → Return 400 Bad Request
    │   └─► Build filters_applied dict
    │
    ├─► Build database query
    │   └─► SELECT * FROM string_analysis
    │       WHERE is_palindrome = true
    │       AND length >= 5
    │
    ├─► Execute query
    │   └─► Get matching records
    │
    ├─► Serialize results
    │
    ▼
Response: 200 OK
    └─► JSON: {data: [...], count: N, filters_applied: {...}}
```

### 4. Natural Language Query Flow

```
Client Request
    │
    ├─► GET /strings/filter-by-natural-language
    │   Query: "palindromic single word longer than 3"
    │
    ▼
filter_by_natural_language() View
    │
    ├─► parse_natural_language_query()
    │   ├─► Regex: "palindrom" → is_palindrome=true
    │   ├─► Regex: "single word" → word_count=1
    │   ├─► Regex: "longer than 3" → min_length=4
    │   └─► Return parsed_filters dict
    │
    ├─► Check for conflicts
    │   └─► min_length > max_length?
    │       └─► YES → Return 422 Unprocessable
    │
    ├─► Apply filters to queryset
    │   └─► Build WHERE clause from parsed_filters
    │
    ├─► Execute query
    │
    ▼
Response: 200 OK
    └─► JSON: {
            data: [...],
            count: N,
            interpreted_query: {
                original_query: "...",
                parsed_filters: {...}
            }
        }
```

### 5. Delete String Flow (DELETE /strings/<value>)

```
Client Request
    │
    ├─► DELETE /strings/hello%20world
    │
    ▼
string_detail() View (method=DELETE)
    │
    ├─► URL decode value
    │
    ├─► Query database
    │   └─► SELECT * FROM string_analysis
    │       WHERE value = 'hello world'
    │
    ├─► Found?
    │   ├─► YES → Delete record
    │   │   └─► DELETE FROM string_analysis
    │   │       WHERE id = 'hash...'
    │   └─► NO → Return 404 Not Found
    │
    ▼
Response: 204 No Content (empty body)
```

---

## 🗄️ Database Relationships

```
┌────────────────────────────────────────────────────────────┐
│                  StringAnalysis Table                      │
├────────────────────────────────────────────────────────────┤
│ PK  id (VARCHAR 64)          [SHA-256 hash]               │
│ UQ  value (TEXT)             [Indexed]                     │
│     length (INTEGER)         [Indexed]                     │
│     is_palindrome (BOOLEAN)  [Indexed]                     │
│     unique_characters (INT)                                │
│     word_count (INTEGER)     [Indexed]                     │
│     sha256_hash (VARCHAR 64)                               │
│     character_frequency_map (JSONB)                        │
│     created_at (TIMESTAMP)                                 │
└────────────────────────────────────────────────────────────┘

Indexes:
├─► PRIMARY KEY (id)
├─► UNIQUE INDEX (value)
├─► INDEX (is_palindrome)
├─► INDEX (length)
└─► INDEX (word_count)

Benefits:
✓ Fast lookups by hash (primary key)
✓ Fast lookups by value (unique index)
✓ Efficient filtering (indexed columns)
✓ Prevents duplicate strings (unique constraint)
```

---

## 📦 Module Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                    Django 4.2+                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Django REST Framework 3.14+                   │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │         strings_app                            │  │  │
│  │  │                                                 │  │  │
│  │  │  models.py ──► utils.py (analyze_string)       │  │  │
│  │  │      │                                          │  │  │
│  │  │      ▼                                          │  │  │
│  │  │  serializers.py                                │  │  │
│  │  │      │                                          │  │  │
│  │  │      ▼                                          │  │  │
│  │  │  views.py ──► utils.py (parse_nl_query)        │  │  │
│  │  │      │                                          │  │  │
│  │  │      ▼                                          │  │  │
│  │  │  urls.py                                        │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│ PostgreSQL  │    │ WhiteNoise   │    │ CORS Headers    │
│ (psycopg2)  │    │ (Static)     │    │ (django-cors)   │
└─────────────┘    └──────────────┘    └─────────────────┘
```

---

## 🔐 Security Flow

```
Client Request
    │
    ├─► HTTPS (SSL/TLS)
    │   └─► Encrypted connection
    │
    ▼
Apache/Passenger
    │
    ├─► CORS Check
    │   └─► Origin in ALLOWED_ORIGINS?
    │
    ├─► CSRF Protection
    │   └─► Token validation (for state-changing ops)
    │
    ▼
Django Middleware Stack
    │
    ├─► Security Middleware
    │   ├─► SECURE_SSL_REDIRECT
    │   ├─► SECURE_CONTENT_TYPE_NOSNIFF
    │   └─► X_FRAME_OPTIONS
    │
    ├─► CORS Middleware
    │   └─► Add CORS headers
    │
    ├─► CSRF Middleware
    │   └─► Verify CSRF token
    │
    ▼
View Function
    │
    ├─► Input Validation
    │   ├─► Type checking
    │   ├─► Length validation
    │   └─► SQL injection prevention (ORM)
    │
    ▼
Database Query
    │
    ├─► Parameterized queries (ORM)
    │   └─► Prevents SQL injection
    │
    ▼
Response
    │
    ├─► Add security headers
    │   ├─► HSTS
    │   ├─► X-Content-Type-Options
    │   └─► X-Frame-Options
    │
    ▼
Client
```

---

## 🚀 Deployment Flow (Sevalla)

```
Developer Machine
    │
    ├─► Git commit and push
    │   └─► Push to GitHub
    │
    ▼
Sevalla Server (SSH)
    │
    ├─► Git pull / FTP upload
    │   └─► Update project files
    │
    ├─► Virtual Environment
    │   ├─► source venv/bin/activate
    │   └─► pip install -r requirements.txt
    │
    ├─► Environment Variables
    │   └─► Edit .env file
    │
    ├─► Database Migrations
    │   ├─► python manage.py makemigrations
    │   └─► python manage.py migrate
    │
    ├─► Collect Static Files
    │   └─► python manage.py collectstatic
    │
    ├─► Set Permissions
    │   └─► chmod 755 passenger_wsgi.py
    │
    ├─► Restart Application
    │   └─► touch tmp/restart.txt
    │
    ▼
Apache/Passenger
    │
    ├─► Read .htaccess
    │   └─► Configure Passenger
    │
    ├─► Load passenger_wsgi.py
    │   └─► Initialize Django
    │
    ▼
Application Live! 🎉
```

---

## 🧪 Testing Flow

```
Test Runner (python manage.py test)
    │
    ├─► Create Test Database
    │   └─► Clone production schema
    │
    ├─► Load Test Data
    │   └─► setUp() methods
    │
    ├─► Run Tests
    │   ├─► Unit Tests
    │   │   ├─► test_analyze_string_basic()
    │   │   ├─► test_palindrome_detection()
    │   │   └─► test_compute_sha256()
    │   │
    │   ├─► Model Tests
    │   │   ├─► test_create_string_analysis()
    │   │   └─► test_unique_constraint()
    │   │
    │   ├─► API Tests
    │   │   ├─► test_create_string_success()
    │   │   ├─► test_create_duplicate_409()
    │   │   ├─► test_get_string_success()
    │   │   ├─► test_list_with_filters()
    │   │   ├─► test_natural_language_query()
    │   │   └─► test_delete_string_success()
    │   │
    │   └─► Integration Tests
    │       └─► test_full_crud_workflow()
    │
    ├─► Clean Up
    │   └─► tearDown() methods
    │
    ├─► Drop Test Database
    │
    ▼
Test Results
    └─► Pass/Fail report
```

---

## 📊 Data Flow: String Analysis

```
Input String: "hello world"
    │
    ▼
analyze_string(value)
    │
    ├─► length = len(value)
    │   └─► Result: 11
    │
    ├─► is_palindrome
    │   ├─► cleaned = value.replace(' ', '').lower()
    │   │   └─► "helloworld"
    │   ├─► reversed = cleaned[::-1]
    │   │   └─► "dlrowolleh"
    │   └─► Result: False
    │
    ├─► unique_characters = len(set(value))
    │   └─► Result: 8 (h,e,l,o, ,w,r,d)
    │
    ├─► word_count = len(value.split())
    │   └─► Result: 2
    │
    ├─► sha256_hash
    │   ├─► hashlib.sha256(value.encode())
    │   └─► Result: "b94d27b9..."
    │
    ├─► character_frequency_map
    │   ├─► Count each character
    │   └─► Result: {"h": 1, "e": 1, "l": 3, ...}
    │
    ▼
Return properties dict
    │
    ▼
Save to Database
    │
    └─► id = sha256_hash (primary key)
```

---

## 🎯 Summary

This architecture provides:

✅ **Scalability** - Database indexes for efficient queries  
✅ **Security** - Multiple layers of validation and protection  
✅ **Maintainability** - Clear separation of concerns  
✅ **Testability** - Comprehensive test coverage  
✅ **Performance** - Optimized queries and caching-ready  
✅ **Reliability** - Error handling at every layer  
✅ **Deployment** - Production-ready Sevalla configuration  

All components work together to provide a robust, production-ready API service.
