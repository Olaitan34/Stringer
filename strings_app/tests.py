"""
Comprehensive tests for the strings_app application.
Tests all endpoints, filters, error cases, and natural language parsing.
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import StringAnalysis
from .utils import analyze_string, compute_sha256
import json


class StringAnalysisUtilsTestCase(TestCase):
    """Test the utility functions for string analysis."""
    
    def test_analyze_string_basic(self):
        """Test basic string analysis."""
        result = analyze_string("hello")
        self.assertEqual(result['length'], 5)
        self.assertFalse(result['is_palindrome'])
        self.assertEqual(result['unique_characters'], 4)  # h, e, l, o
        self.assertEqual(result['word_count'], 1)
        self.assertEqual(len(result['sha256_hash']), 64)
        self.assertEqual(result['character_frequency_map']['h'], 1)
        self.assertEqual(result['character_frequency_map']['l'], 2)
    
    def test_analyze_string_palindrome(self):
        """Test palindrome detection."""
        result = analyze_string("racecar")
        self.assertTrue(result['is_palindrome'])
        
        result = analyze_string("A man a plan a canal Panama")
        self.assertTrue(result['is_palindrome'])
        
        result = analyze_string("hello")
        self.assertFalse(result['is_palindrome'])
    
    def test_analyze_string_with_spaces(self):
        """Test string with multiple words."""
        result = analyze_string("hello world")
        self.assertEqual(result['length'], 11)
        self.assertEqual(result['word_count'], 2)
        self.assertEqual(result['character_frequency_map'][' '], 1)
    
    def test_compute_sha256(self):
        """Test SHA-256 hash computation."""
        hash1 = compute_sha256("test")
        hash2 = compute_sha256("test")
        hash3 = compute_sha256("Test")
        
        self.assertEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)
        self.assertEqual(len(hash1), 64)


class StringAnalysisModelTestCase(TestCase):
    """Test the StringAnalysis model."""
    
    def test_create_string_analysis(self):
        """Test creating a StringAnalysis instance."""
        string_analysis = StringAnalysis(value="hello world")
        string_analysis.save()
        
        self.assertEqual(string_analysis.value, "hello world")
        self.assertEqual(string_analysis.length, 11)
        self.assertEqual(string_analysis.word_count, 2)
        self.assertIsNotNone(string_analysis.sha256_hash)
        self.assertEqual(string_analysis.id, string_analysis.sha256_hash)
        self.assertIsNotNone(string_analysis.created_at)
    
    def test_unique_constraint(self):
        """Test that duplicate strings cannot be created."""
        StringAnalysis.objects.create(value="test")
        
        with self.assertRaises(Exception):
            StringAnalysis.objects.create(value="test")
    
    def test_properties_method(self):
        """Test the properties method."""
        string_analysis = StringAnalysis.objects.create(value="test")
        props = string_analysis.properties
        
        self.assertIn('length', props)
        self.assertIn('is_palindrome', props)
        self.assertIn('unique_characters', props)
        self.assertIn('word_count', props)
        self.assertIn('sha256_hash', props)
        self.assertIn('character_frequency_map', props)


class CreateStringAPITestCase(TestCase):
    """Test POST /strings endpoint."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_create_string_success(self):
        """Test successful string creation."""
        response = self.client.post(
            '/strings',
            {'value': 'hello world'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertIn('value', response.data)
        self.assertIn('properties', response.data)
        self.assertIn('created_at', response.data)
        self.assertEqual(response.data['value'], 'hello world')
    
    def test_create_string_missing_value(self):
        """Test creating string without value field."""
        response = self.client.post('/strings', {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_create_string_empty_value(self):
        """Test creating string with empty value."""
        response = self.client.post(
            '/strings',
            {'value': ''},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_string_duplicate(self):
        """Test creating duplicate string (409 Conflict)."""
        self.client.post('/strings', {'value': 'test'}, format='json')
        response = self.client.post('/strings', {'value': 'test'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('error', response.data)
    
    def test_create_string_invalid_type(self):
        """Test creating string with invalid type."""
        response = self.client.post(
            '/strings',
            {'value': 123},
            format='json'
        )
        
        # DRF might convert this to string, but our validation should catch it
        # The actual behavior depends on how DRF handles type coercion
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ])


class GetStringByValueAPITestCase(TestCase):
    """Test GET /strings/<string_value> endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.string_analysis = StringAnalysis.objects.create(value="hello world")
    
    def test_get_string_success(self):
        """Test successful string retrieval."""
        response = self.client.get('/strings/hello world')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 'hello world')
        self.assertIn('properties', response.data)
    
    def test_get_string_url_encoded(self):
        """Test retrieving string with special characters (URL encoded)."""
        StringAnalysis.objects.create(value="hello@world!")
        response = self.client.get('/strings/hello%40world%21')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 'hello@world!')
    
    def test_get_string_not_found(self):
        """Test retrieving non-existent string."""
        response = self.client.get('/strings/nonexistent')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)


class ListStringsAPITestCase(TestCase):
    """Test GET /strings endpoint with filters."""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test strings
        StringAnalysis.objects.create(value="racecar")  # palindrome, 7 chars, 1 word
        StringAnalysis.objects.create(value="hello world")  # not palindrome, 11 chars, 2 words
        StringAnalysis.objects.create(value="noon")  # palindrome, 4 chars, 1 word
        StringAnalysis.objects.create(value="test")  # not palindrome, 4 chars, 1 word
    
    def test_list_all_strings(self):
        """Test listing all strings without filters."""
        response = self.client.get('/strings/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('count', response.data)
        self.assertIn('filters_applied', response.data)
        self.assertEqual(response.data['count'], 4)
    
    def test_filter_by_palindrome(self):
        """Test filtering by is_palindrome."""
        response = self.client.get('/strings/?is_palindrome=true')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['filters_applied']['is_palindrome'], True)
    
    def test_filter_by_min_length(self):
        """Test filtering by min_length."""
        response = self.client.get('/strings/?min_length=5')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 2)
        self.assertEqual(response.data['filters_applied']['min_length'], 5)
    
    def test_filter_by_max_length(self):
        """Test filtering by max_length."""
        response = self.client.get('/strings/?max_length=5')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['filters_applied']['max_length'], 5)
    
    def test_filter_by_word_count(self):
        """Test filtering by word_count."""
        response = self.client.get('/strings/?word_count=1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(response.data['filters_applied']['word_count'], 1)
    
    def test_filter_by_contains_character(self):
        """Test filtering by contains_character."""
        response = self.client.get('/strings/?contains_character=o')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
        self.assertEqual(response.data['filters_applied']['contains_character'], 'o')
    
    def test_filter_multiple_criteria(self):
        """Test filtering with multiple criteria."""
        response = self.client.get('/strings/?is_palindrome=true&word_count=1')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_filter_invalid_palindrome_value(self):
        """Test invalid is_palindrome value."""
        response = self.client.get('/strings/?is_palindrome=maybe')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_invalid_min_length(self):
        """Test invalid min_length value."""
        response = self.client.get('/strings/?min_length=abc')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_invalid_contains_character(self):
        """Test invalid contains_character value (more than 1 char)."""
        response = self.client.get('/strings/?contains_character=ab')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NaturalLanguageFilterAPITestCase(TestCase):
    """Test GET /strings/filter-by-natural-language endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        
        # Create test strings
        StringAnalysis.objects.create(value="racecar")
        StringAnalysis.objects.create(value="hello")
        StringAnalysis.objects.create(value="noon")
        StringAnalysis.objects.create(value="a")
    
    def test_natural_language_palindrome(self):
        """Test parsing 'palindrome' query."""
        response = self.client.get('/strings/filter-by-natural-language?query=palindrome')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('interpreted_query', response.data)
        self.assertEqual(response.data['interpreted_query']['original_query'], 'palindrome')
        self.assertIn('is_palindrome', response.data['interpreted_query']['parsed_filters'])
    
    def test_natural_language_single_word(self):
        """Test parsing 'single word' query."""
        response = self.client.get('/strings/filter-by-natural-language?query=single word')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['interpreted_query']['parsed_filters']['word_count'], 1
        )
    
    def test_natural_language_longer_than(self):
        """Test parsing 'longer than X characters' query."""
        response = self.client.get(
            '/strings/filter-by-natural-language?query=longer than 3 characters'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['interpreted_query']['parsed_filters']['min_length'], 4
        )
    
    def test_natural_language_shorter_than(self):
        """Test parsing 'shorter than X' query."""
        response = self.client.get(
            '/strings/filter-by-natural-language?query=shorter than 5'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['interpreted_query']['parsed_filters']['max_length'], 4
        )
    
    def test_natural_language_contains_letter(self):
        """Test parsing 'contains letter X' query."""
        response = self.client.get(
            '/strings/filter-by-natural-language?query=contains letter a'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['interpreted_query']['parsed_filters']['contains_character'], 'a'
        )
    
    def test_natural_language_first_vowel(self):
        """Test parsing 'first vowel' query."""
        response = self.client.get(
            '/strings/filter-by-natural-language?query=first vowel'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['interpreted_query']['parsed_filters']['contains_character'], 'a'
        )
    
    def test_natural_language_complex_query(self):
        """Test parsing complex query with multiple filters."""
        response = self.client.get(
            '/strings/filter-by-natural-language?query=palindromic single word'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        filters = response.data['interpreted_query']['parsed_filters']
        self.assertIn('is_palindrome', filters)
        self.assertIn('word_count', filters)
    
    def test_natural_language_missing_query(self):
        """Test missing query parameter."""
        response = self.client.get('/strings/filter-by-natural-language')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_natural_language_conflicting_filters(self):
        """Test conflicting filters (min_length > max_length)."""
        response = self.client.get(
            '/strings/filter-by-natural-language?query=longer than 10 and shorter than 5'
        )
        
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class DeleteStringByValueAPITestCase(TestCase):
    """Test DELETE /strings/<string_value> endpoint."""
    
    def setUp(self):
        self.client = APIClient()
        self.string_analysis = StringAnalysis.objects.create(value="delete me")
    
    def test_delete_string_success(self):
        """Test successful string deletion."""
        response = self.client.delete('/strings/delete me')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.content), 0)  # Empty body
        
        # Verify it's deleted
        self.assertFalse(StringAnalysis.objects.filter(value="delete me").exists())
    
    def test_delete_string_not_found(self):
        """Test deleting non-existent string."""
        response = self.client.delete('/strings/nonexistent')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_string_url_encoded(self):
        """Test deleting string with special characters (URL encoded)."""
        StringAnalysis.objects.create(value="delete@me!")
        response = self.client.delete('/strings/delete%40me%21')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class IntegrationTestCase(TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow."""
        # Create
        response = self.client.post(
            '/strings',
            {'value': 'integration test'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Read
        response = self.client.get('/strings/integration test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # List
        response = self.client.get('/strings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
        
        # Delete
        response = self.client.delete('/strings/integration test')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify deletion
        response = self.client.get('/strings/integration test')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
