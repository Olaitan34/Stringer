"""
Test POST /strings endpoint to verify correct status codes.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_post_without_slash():
    """Test POST /strings (without trailing slash)"""
    print("\n1. Testing POST /strings (no trailing slash)...")
    
    test_value = f"test_no_slash_{requests.utils.default_headers()['User-Agent'][:5]}"
    response = requests.post(f"{BASE_URL}/strings", json={"value": test_value})
    
    print(f"   URL: {response.url}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("   ✅ PASS: 201 Created")
    else:
        print(f"   ❌ FAIL: Expected 201, got {response.status_code}")
    
    return response.status_code == 201

def test_post_with_slash():
    """Test POST /strings/ (with trailing slash)"""
    print("\n2. Testing POST /strings/ (with trailing slash)...")
    
    test_value = f"test_with_slash_{requests.utils.default_headers()['User-Agent'][:5]}"
    response = requests.post(f"{BASE_URL}/strings/", json={"value": test_value})
    
    print(f"   URL: {response.url}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("   ✅ PASS: 201 Created")
    else:
        print(f"   ❌ FAIL: Expected 201, got {response.status_code}")
    
    return response.status_code == 201

def test_duplicate():
    """Test duplicate string returns 409"""
    print("\n3. Testing duplicate string (409 Conflict)...")
    
    test_value = "duplicate_test_string"
    
    # Create first time
    response1 = requests.post(f"{BASE_URL}/strings", json={"value": test_value})
    print(f"   First POST: {response1.status_code}")
    
    # Try to create again
    response2 = requests.post(f"{BASE_URL}/strings", json={"value": test_value})
    print(f"   Second POST: {response2.status_code}")
    print(f"   Response: {response2.json()}")
    
    if response2.status_code == 409:
        print("   ✅ PASS: 409 Conflict")
        return True
    else:
        print(f"   ❌ FAIL: Expected 409, got {response2.status_code}")
        return False

def test_missing_value():
    """Test missing 'value' field returns 400"""
    print("\n4. Testing missing 'value' field (400 Bad Request)...")
    
    response = requests.post(f"{BASE_URL}/strings", json={})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 400:
        print("   ✅ PASS: 400 Bad Request")
        return True
    else:
        print(f"   ❌ FAIL: Expected 400, got {response.status_code}")
        return False

def test_invalid_type():
    """Test invalid data type returns 422"""
    print("\n5. Testing invalid data type (422 Unprocessable Entity)...")
    
    response = requests.post(f"{BASE_URL}/strings", json={"value": 12345})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code == 422:
        print("   ✅ PASS: 422 Unprocessable Entity")
        return True
    else:
        print(f"   ❌ FAIL: Expected 422, got {response.status_code}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing POST /strings Endpoint")
    print("=" * 60)
    
    try:
        results = []
        results.append(test_post_without_slash())
        results.append(test_post_with_slash())
        results.append(test_duplicate())
        results.append(test_missing_value())
        results.append(test_invalid_type())
        
        print("\n" + "=" * 60)
        passed = sum(results)
        total = len(results)
        print(f"RESULTS: {passed}/{total} tests passed")
        
        if passed == total:
            print("✅ ALL TESTS PASSED!")
        else:
            print(f"❌ {total - passed} test(s) failed")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to Django server.")
        print("Make sure the server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
