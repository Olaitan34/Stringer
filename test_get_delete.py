"""
Test GET and DELETE /strings/{value} endpoints.
"""
import requests
import json
from urllib.parse import quote

BASE_URL = "http://127.0.0.1:8000"

def create_test_string(value):
    """Helper to create a test string"""
    response = requests.post(f"{BASE_URL}/strings", json={"value": value})
    return response

def test_get_existing_string():
    """Test GET /strings/{value} for existing string"""
    print("\n1. Testing GET /strings/{value} for existing string...")
    
    # Create a test string
    test_value = "test get existing"
    create_response = create_test_string(test_value)
    print(f"   Created string: {create_response.status_code}")
    
    if create_response.status_code not in [201, 409]:
        print(f"   ⚠️  Failed to create test string: {create_response.status_code}")
        return False
    
    # Try to GET it
    encoded_value = quote(test_value, safe='')
    response = requests.get(f"{BASE_URL}/strings/{encoded_value}")
    
    print(f"   URL: {response.url}")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Retrieved: {data.get('value', 'N/A')}")
        print("   ✅ PASS: 200 OK")
        return True
    else:
        print(f"   Response: {response.text[:200]}")
        print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
        return False

def test_get_nonexistent_string():
    """Test GET /strings/{value} for non-existent string"""
    print("\n2. Testing GET /strings/{value} for non-existent string...")
    
    test_value = "this_string_should_not_exist_12345"
    encoded_value = quote(test_value, safe='')
    response = requests.get(f"{BASE_URL}/strings/{encoded_value}")
    
    print(f"   URL: {response.url}")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 404:
        print(f"   Response: {response.json()}")
        print("   ✅ PASS: 404 Not Found")
        return True
    else:
        print(f"   ❌ FAIL: Expected 404, got {response.status_code}")
        return False

def test_delete_existing_string():
    """Test DELETE /strings/{value} for existing string"""
    print("\n3. Testing DELETE /strings/{value} for existing string...")
    
    # Create a test string
    test_value = "test delete existing"
    create_response = create_test_string(test_value)
    print(f"   Created string: {create_response.status_code}")
    
    if create_response.status_code not in [201, 409]:
        print(f"   ⚠️  Failed to create test string: {create_response.status_code}")
        return False
    
    # Try to DELETE it
    encoded_value = quote(test_value, safe='')
    response = requests.delete(f"{BASE_URL}/strings/{encoded_value}")
    
    print(f"   URL: {response.url}")
    print(f"   Status: {response.status_code}")
    print(f"   Content Length: {len(response.content)}")
    
    if response.status_code == 204:
        if len(response.content) == 0:
            print("   ✅ PASS: 204 No Content (empty body)")
            return True
        else:
            print(f"   ⚠️  WARNING: Body should be empty but got: {response.content}")
            return True
    else:
        print(f"   Response: {response.text[:200] if response.text else 'empty'}")
        print(f"   ❌ FAIL: Expected 204, got {response.status_code}")
        return False

def test_delete_nonexistent_string():
    """Test DELETE /strings/{value} for non-existent string"""
    print("\n4. Testing DELETE /strings/{value} for non-existent string...")
    
    test_value = "this_string_should_not_exist_for_delete_67890"
    encoded_value = quote(test_value, safe='')
    response = requests.delete(f"{BASE_URL}/strings/{encoded_value}")
    
    print(f"   URL: {response.url}")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 404:
        print(f"   Response: {response.json()}")
        print("   ✅ PASS: 404 Not Found")
        return True
    else:
        print(f"   ❌ FAIL: Expected 404, got {response.status_code}")
        return False

def test_get_with_special_characters():
    """Test GET with special characters in string value"""
    print("\n5. Testing GET with special characters...")
    
    # Create a string with special characters
    test_value = "hello world! @#$%"
    create_response = create_test_string(test_value)
    print(f"   Created string: {create_response.status_code}")
    
    if create_response.status_code not in [201, 409]:
        print(f"   ⚠️  Failed to create test string: {create_response.status_code}")
        return False
    
    # Try to GET it with URL encoding
    encoded_value = quote(test_value, safe='')
    print(f"   Encoded: {encoded_value}")
    response = requests.get(f"{BASE_URL}/strings/{encoded_value}")
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('value') == test_value:
            print(f"   Retrieved correct value: {data['value']}")
            print("   ✅ PASS: 200 OK with special chars")
            return True
        else:
            print(f"   ⚠️  Value mismatch: expected '{test_value}', got '{data.get('value')}'")
            return False
    else:
        print(f"   ❌ FAIL: Expected 200, got {response.status_code}")
        return False

def test_verify_deletion():
    """Test that deleted string is really gone"""
    print("\n6. Testing that deleted string is really gone...")
    
    # Create a string
    test_value = "test verify deletion"
    create_response = create_test_string(test_value)
    print(f"   Created string: {create_response.status_code}")
    
    # Delete it
    encoded_value = quote(test_value, safe='')
    delete_response = requests.delete(f"{BASE_URL}/strings/{encoded_value}")
    print(f"   Deleted string: {delete_response.status_code}")
    
    # Try to GET it (should be 404)
    get_response = requests.get(f"{BASE_URL}/strings/{encoded_value}")
    print(f"   GET after DELETE: {get_response.status_code}")
    
    if get_response.status_code == 404:
        print("   ✅ PASS: String was actually deleted")
        return True
    else:
        print(f"   ❌ FAIL: String still exists after deletion")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Testing GET and DELETE /strings/{value} Endpoints")
    print("=" * 60)
    
    try:
        results = []
        results.append(test_get_existing_string())
        results.append(test_get_nonexistent_string())
        results.append(test_delete_existing_string())
        results.append(test_delete_nonexistent_string())
        results.append(test_get_with_special_characters())
        results.append(test_verify_deletion())
        
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
