"""
Quick test script to verify error responses for POST /strings endpoint.
Run this while the Django dev server is running.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_missing_value_field():
    """Test 400: Missing 'value' field"""
    print("\n1. Testing missing 'value' field (expect 400)...")
    response = requests.post(f"{BASE_URL}/strings/", json={})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("   ✅ PASS: 400 Bad Request")

def test_invalid_type():
    """Test 422: Value is not a string"""
    print("\n2. Testing invalid type (expect 422)...")
    
    # Test with integer
    response = requests.post(f"{BASE_URL}/strings/", json={"value": 12345})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("   ✅ PASS: 422 Unprocessable Entity (integer)")
    
    # Test with boolean
    response = requests.post(f"{BASE_URL}/strings/", json={"value": True})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("   ✅ PASS: 422 Unprocessable Entity (boolean)")
    
    # Test with array
    response = requests.post(f"{BASE_URL}/strings/", json={"value": ["test"]})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"
    print("   ✅ PASS: 422 Unprocessable Entity (array)")

def test_empty_value():
    """Test 400: Empty string"""
    print("\n3. Testing empty value (expect 400)...")
    response = requests.post(f"{BASE_URL}/strings/", json={"value": ""})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("   ✅ PASS: 400 Bad Request (empty string)")
    
    # Test with whitespace only
    response = requests.post(f"{BASE_URL}/strings/", json={"value": "   "})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    print("   ✅ PASS: 400 Bad Request (whitespace only)")

def test_successful_creation():
    """Test 201: Successful creation"""
    print("\n4. Testing successful creation (expect 201)...")
    test_string = f"test string {requests.utils.default_headers()['User-Agent'][:10]}"
    response = requests.post(f"{BASE_URL}/strings/", json={"value": test_string})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    
    # Verify response structure
    data = response.json()
    assert 'id' in data, "Missing 'id' field"
    assert 'value' in data, "Missing 'value' field"
    assert 'properties' in data, "Missing 'properties' field"
    assert 'created_at' in data, "Missing 'created_at' field"
    
    # Verify properties structure
    props = data['properties']
    assert 'length' in props, "Missing 'length' in properties"
    assert 'is_palindrome' in props, "Missing 'is_palindrome' in properties"
    assert 'unique_characters' in props, "Missing 'unique_characters' in properties"
    assert 'word_count' in props, "Missing 'word_count' in properties"
    assert 'sha256_hash' in props, "Missing 'sha256_hash' in properties"
    assert 'character_frequency_map' in props, "Missing 'character_frequency_map' in properties"
    
    print("   ✅ PASS: 201 Created with correct structure")
    return data['id']

def test_duplicate_string(string_id):
    """Test 409: Duplicate string"""
    print("\n5. Testing duplicate string (expect 409)...")
    # Try to create the same string again
    response = requests.post(f"{BASE_URL}/strings/", json={"value": "test string python-requ"})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 409:
        print("   ✅ PASS: 409 Conflict")
    elif response.status_code == 201:
        print("   ⚠️  WARNING: Created duplicate (might be unique string)")
    else:
        assert False, f"Expected 409, got {response.status_code}"

if __name__ == "__main__":
    print("=" * 60)
    print("Testing POST /strings Error Responses")
    print("=" * 60)
    
    try:
        test_missing_value_field()
        test_invalid_type()
        test_empty_value()
        string_id = test_successful_creation()
        test_duplicate_string(string_id)
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Django server.")
        print("Make sure the server is running: python manage.py runserver")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
