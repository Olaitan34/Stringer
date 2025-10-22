# Quick API Test Script
# Run this to test the API endpoints

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("String Analyzer API - Quick Test")
print("=" * 60)

# Test 1: Create a string
print("\n[TEST 1] Creating a new string analysis...")
response = requests.post(
    f"{BASE_URL}/strings",
    json={"value": "racecar"}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 201:
    data = response.json()
    print(f"✅ Success! Created string: {data['value']}")
    print(f"   - Is palindrome: {data['properties']['is_palindrome']}")
    print(f"   - Length: {data['properties']['length']}")
    print(f"   - SHA-256: {data['id'][:16]}...")
else:
    print(f"❌ Failed: {response.text}")

# Test 2: Get the string
print("\n[TEST 2] Retrieving the string...")
response = requests.get(f"{BASE_URL}/strings/racecar")
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("✅ Success! Retrieved string")
else:
    print(f"❌ Failed: {response.text}")

# Test 3: Create another string
print("\n[TEST 3] Creating another string...")
response = requests.post(
    f"{BASE_URL}/strings",
    json={"value": "hello world"}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 201:
    data = response.json()
    print(f"✅ Success! Created string: {data['value']}")
    print(f"   - Word count: {data['properties']['word_count']}")
    print(f"   - Character frequency: {json.dumps(data['properties']['character_frequency_map'], indent=2)}")
else:
    print(f"❌ Failed: {response.text}")

# Test 4: List all strings
print("\n[TEST 4] Listing all strings...")
response = requests.get(f"{BASE_URL}/strings/")
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success! Found {data['count']} strings")
    for item in data['data']:
        print(f"   - {item['value']}")
else:
    print(f"❌ Failed: {response.text}")

# Test 5: Filter by palindrome
print("\n[TEST 5] Filtering palindromes...")
response = requests.get(f"{BASE_URL}/strings/?is_palindrome=true")
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success! Found {data['count']} palindromes")
    print(f"   Filters applied: {data['filters_applied']}")
else:
    print(f"❌ Failed: {response.text}")

# Test 6: Natural language query
print("\n[TEST 6] Natural language query: 'palindrome'...")
response = requests.get(
    f"{BASE_URL}/strings/filter-by-natural-language",
    params={"query": "palindrome"}
)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✅ Success! Found {data['count']} results")
    print(f"   Parsed filters: {data['interpreted_query']['parsed_filters']}")
else:
    print(f"❌ Failed: {response.text}")

# Test 7: Delete a string
print("\n[TEST 7] Deleting a string...")
response = requests.delete(f"{BASE_URL}/strings/hello%20world")
print(f"Status Code: {response.status_code}")
if response.status_code == 204:
    print("✅ Success! String deleted")
else:
    print(f"❌ Failed: {response.text}")

# Test 8: Verify deletion
print("\n[TEST 8] Verifying deletion...")
response = requests.get(f"{BASE_URL}/strings/hello%20world")
print(f"Status Code: {response.status_code}")
if response.status_code == 404:
    print("✅ Success! String not found (as expected)")
else:
    print(f"❌ Failed: String still exists")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
print("\nYour API is working correctly! 🎉")
print("Server is running at: http://127.0.0.1:8000")
print("\nNext steps:")
print("1. Test with Postman: Import postman_collection.json")
print("2. Read API docs: API_DOCUMENTATION.md")
print("3. Deploy to Sevalla: Follow SEVALLA_QUICK_REFERENCE.md")
print("=" * 60)
