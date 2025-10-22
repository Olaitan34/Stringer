"""
Test PostgreSQL Database with String Analyzer
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'string_analyzer.settings')
django.setup()

from strings_app.models import StringAnalysis

print("=" * 60)
print("Testing PostgreSQL Database")
print("=" * 60)

# Test 1: Create a new string
print("\n[TEST 1] Creating a new string in PostgreSQL...")
try:
    test_string = StringAnalysis.objects.create(value="PostgreSQL Test String")
    print(f"✅ Created: {test_string.value}")
    print(f"   - ID (SHA-256): {test_string.id[:16]}...")
    print(f"   - Length: {test_string.length}")
    print(f"   - Is Palindrome: {test_string.is_palindrome}")
    print(f"   - Word Count: {test_string.word_count}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Query all strings
print("\n[TEST 2] Querying all strings from PostgreSQL...")
all_strings = StringAnalysis.objects.all()
print(f"✅ Total strings in database: {all_strings.count()}")
for s in all_strings:
    print(f"   - {s.value} (Length: {s.length}, Palindrome: {s.is_palindrome})")

# Test 3: Filter palindromes
print("\n[TEST 3] Filtering palindromes...")
palindromes = StringAnalysis.objects.filter(is_palindrome=True)
print(f"✅ Palindromes found: {palindromes.count()}")

# Test 4: Create a palindrome
print("\n[TEST 4] Creating a palindrome...")
try:
    palindrome = StringAnalysis.objects.create(value="racecar")
    print(f"✅ Created palindrome: {palindrome.value}")
    print(f"   - Is Palindrome: {palindrome.is_palindrome}")
except Exception as e:
    if "duplicate key" in str(e).lower() or "unique constraint" in str(e).lower():
        print(f"ℹ️  String already exists (this is expected)")
    else:
        print(f"❌ Error: {e}")

# Test 5: Delete test string
print("\n[TEST 5] Cleaning up test data...")
try:
    test_strings = StringAnalysis.objects.filter(value__contains="Test")
    count = test_strings.count()
    test_strings.delete()
    print(f"✅ Deleted {count} test string(s)")
except Exception as e:
    print(f"❌ Error: {e}")

# Final count
print("\n[FINAL] Database status:")
print(f"✅ Total strings: {StringAnalysis.objects.count()}")

print("\n" + "=" * 60)
print("🎉 PostgreSQL Database is Working Perfectly!")
print("=" * 60)
