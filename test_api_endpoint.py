"""
Test script for String Analyzer API
Tests the POST /strings endpoint with various scenarios
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"  # Change to your production URL when testing live
API_ENDPOINT = f"{BASE_URL}/strings/"

def print_separator():
    print("\n" + "="*80 + "\n")

def test_create_string_success():
    """Test successful string creation"""
    print("TEST 1: Create String - Success Case")
    print("-" * 40)
    
    payload = {
        "value": "string to analyze"
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("\n✅ TEST PASSED: String created successfully")
            data = response.json()
            
            # Validate response structure
            assert "id" in data, "Missing 'id' field"
            assert "value" in data, "Missing 'value' field"
            assert "properties" in data, "Missing 'properties' field"
            assert "created_at" in data, "Missing 'created_at' field"
            
            # Validate properties
            props = data["properties"]
            assert props["length"] == 17, f"Expected length 17, got {props['length']}"
            assert props["is_palindrome"] == False, "Expected is_palindrome to be False"
            assert props["word_count"] == 3, f"Expected word_count 3, got {props['word_count']}"
            assert "sha256_hash" in props, "Missing sha256_hash"
            assert "character_frequency_map" in props, "Missing character_frequency_map"
            
            print("✅ All response fields validated")
            return data["id"]
        else:
            print(f"\n❌ TEST FAILED: Expected 201, got {response.status_code}")
            return None
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")
        return None

def test_create_duplicate_string(sha256_id):
    """Test duplicate string creation (409 Conflict)"""
    print("TEST 2: Create Duplicate String - 409 Conflict")
    print("-" * 40)
    
    payload = {
        "value": "string to analyze"
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 409:
            print("\n✅ TEST PASSED: Correctly returned 409 Conflict")
        else:
            print(f"\n❌ TEST FAILED: Expected 409, got {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")

def test_missing_value_field():
    """Test missing 'value' field (400 Bad Request)"""
    print("TEST 3: Missing 'value' Field - 400 Bad Request")
    print("-" * 40)
    
    payload = {
        "text": "wrong field name"
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 400:
            print("\n✅ TEST PASSED: Correctly returned 400 Bad Request")
        else:
            print(f"\n❌ TEST FAILED: Expected 400, got {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")

def test_invalid_data_type():
    """Test invalid data type for 'value' (422 Unprocessable Entity)"""
    print("TEST 4: Invalid Data Type - 422 Unprocessable Entity")
    print("-" * 40)
    
    payload = {
        "value": 12345  # Should be string, not integer
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 422:
            print("\n✅ TEST PASSED: Correctly returned 422 Unprocessable Entity")
        else:
            print(f"\n❌ TEST FAILED: Expected 422, got {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")

def test_empty_string():
    """Test creating an empty string"""
    print("TEST 5: Empty String")
    print("-" * 40)
    
    payload = {
        "value": ""
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("\n✅ TEST PASSED: Empty string created successfully")
            data = response.json()
            assert data["properties"]["length"] == 0, "Expected length 0"
            assert data["properties"]["word_count"] == 0, "Expected word_count 0"
        else:
            print(f"\n⚠️  Status: {response.status_code} (may be expected)")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")

def test_palindrome_string():
    """Test creating a palindrome string"""
    print("TEST 6: Palindrome String")
    print("-" * 40)
    
    payload = {
        "value": "A man a plan a canal Panama"
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            data = response.json()
            if data["properties"]["is_palindrome"]:
                print("\n✅ TEST PASSED: Palindrome correctly detected")
            else:
                print("\n❌ TEST FAILED: Palindrome not detected")
        else:
            print(f"\n⚠️  Status: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")

def test_special_characters():
    """Test string with special characters"""
    print("TEST 7: Special Characters")
    print("-" * 40)
    
    payload = {
        "value": "Hello! @World# 123 $%^&*()"
    }
    
    print(f"Request URL: {API_ENDPOINT}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 201:
            print("\n✅ TEST PASSED: Special characters handled correctly")
        else:
            print(f"\n⚠️  Status: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ TEST FAILED with exception: {str(e)}")

def cleanup_test_strings():
    """Clean up test strings (optional)"""
    print("CLEANUP: Removing test strings")
    print("-" * 40)
    
    test_values = [
        "string to analyze",
        "",
        "A man a plan a canal Panama",
        "Hello! @World# 123 $%^&*()"
    ]
    
    for value in test_values:
        try:
            response = requests.delete(f"{API_ENDPOINT}?value={value}")
            if response.status_code == 204:
                print(f"✅ Deleted: '{value}'")
            elif response.status_code == 404:
                print(f"⚠️  Not found: '{value}'")
            else:
                print(f"❌ Error deleting '{value}': {response.status_code}")
        except Exception as e:
            print(f"❌ Exception deleting '{value}': {str(e)}")

def main():
    """Run all tests"""
    print("="*80)
    print("STRING ANALYZER API - ENDPOINT TESTING")
    print("="*80)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Testing endpoint: {API_ENDPOINT}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print_separator()
    
    # Test 1: Success case
    sha256_id = test_create_string_success()
    print_separator()
    
    # Test 2: Duplicate (only if Test 1 succeeded)
    if sha256_id:
        test_create_duplicate_string(sha256_id)
        print_separator()
    
    # Test 3: Missing field
    test_missing_value_field()
    print_separator()
    
    # Test 4: Invalid data type
    test_invalid_data_type()
    print_separator()
    
    # Test 5: Empty string
    test_empty_string()
    print_separator()
    
    # Test 6: Palindrome
    test_palindrome_string()
    print_separator()
    
    # Test 7: Special characters
    test_special_characters()
    print_separator()
    
    # Optional cleanup
    print("\nWould you like to clean up test data? (This will delete test strings)")
    print("Skipping cleanup - run cleanup_test_strings() manually if needed")
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
