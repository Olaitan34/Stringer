"""
Views for the strings_app application.
Implements all 5 API endpoints with proper validation and error handling.
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
import re

from .models import StringAnalysis
from .serializers import (
    StringAnalysisSerializer,
    StringListSerializer,
    NaturalLanguageQuerySerializer
)


@api_view(['POST'])
def create_string(request):
    """
    POST /strings
    
    Create a new string analysis.
    
    Request Body:
        {
            "value": "string to analyze"
        }
    
    Responses:
        201 Created: String created successfully
        400 Bad Request: Missing 'value' field or empty value
        409 Conflict: String already exists
        422 Unprocessable Entity: Invalid value type (not a string)
    """
    # Validate that value exists
    if 'value' not in request.data:
        return Response(
            {"error": "The 'value' field is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if value is a string type (422 Unprocessable Entity)
    value = request.data.get('value')
    if not isinstance(value, str):
        return Response(
            {"error": "Value must be a string."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    # Check if value is empty (400 Bad Request)
    if not value or value.strip() == '':
        return Response(
            {"error": "Value cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = StringAnalysisSerializer(data=request.data)
    
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        # Check for conflict (string already exists) - 409
        error_detail = str(e.detail)
        if 'conflict' in error_detail.lower() or 'already exists' in error_detail.lower():
            return Response(
                {"error": "String already exists in the database."},
                status=status.HTTP_409_CONFLICT
            )
        
        # Any other validation error - 400
        return Response(
            {"error": str(e.detail)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Unexpected errors - 400
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'DELETE'])
def string_detail(request, string_value):
    """
    GET /strings/<string:string_value> - Retrieve a string analysis
    DELETE /strings/<string:string_value> - Delete a string analysis
    
    Retrieve or delete a string analysis by its actual string value (not hash).
    URL encoding is handled automatically.
    
    Responses:
        GET:
            200 OK: String found
            404 Not Found: String not found
        DELETE:
            204 No Content: String deleted successfully (empty body)
            404 Not Found: String not found
    """
    # URL decode the string value
    decoded_value = unquote(string_value)
    
    if request.method == 'GET':
        # Retrieve the string analysis or return 404
        try:
            string_analysis = StringAnalysis.objects.get(value=decoded_value)
            serializer = StringAnalysisSerializer(string_analysis)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StringAnalysis.DoesNotExist:
            return Response(
                {"error": "String not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    elif request.method == 'DELETE':
        # Try to find and delete the string analysis
        try:
            string_analysis = StringAnalysis.objects.get(value=decoded_value)
            string_analysis.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StringAnalysis.DoesNotExist:
            return Response(
                {"error": "String not found."},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
def list_strings(request):
    """
    GET /strings
    
    List all strings with optional query parameters for filtering:
    - is_palindrome: boolean (convert "true"/"false" string to bool)
    - min_length: integer (filter length >= min_length)
    - max_length: integer (filter length <= max_length)
    - word_count: integer (exact match)
    - contains_character: single character (check if char in value)
    
    Returns:
        {
            "data": [array of objects],
            "count": int,
            "filters_applied": {}
        }
    
    Responses:
        200 OK: Success
        400 Bad Request: Invalid query parameters
    """
    queryset = StringAnalysis.objects.all()
    filters_applied = {}
    
    # Parse and apply filters
    try:
        # is_palindrome filter
        if 'is_palindrome' in request.query_params:
            is_palindrome_str = request.query_params.get('is_palindrome').lower()
            if is_palindrome_str not in ['true', 'false']:
                return Response(
                    {"error": "is_palindrome must be 'true' or 'false'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            is_palindrome = is_palindrome_str == 'true'
            queryset = queryset.filter(is_palindrome=is_palindrome)
            filters_applied['is_palindrome'] = is_palindrome
        
        # min_length filter
        if 'min_length' in request.query_params:
            try:
                min_length = int(request.query_params.get('min_length'))
                queryset = queryset.filter(length__gte=min_length)
                filters_applied['min_length'] = min_length
            except ValueError:
                return Response(
                    {"error": "min_length must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # max_length filter
        if 'max_length' in request.query_params:
            try:
                max_length = int(request.query_params.get('max_length'))
                queryset = queryset.filter(length__lte=max_length)
                filters_applied['max_length'] = max_length
            except ValueError:
                return Response(
                    {"error": "max_length must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # word_count filter
        if 'word_count' in request.query_params:
            try:
                word_count = int(request.query_params.get('word_count'))
                queryset = queryset.filter(word_count=word_count)
                filters_applied['word_count'] = word_count
            except ValueError:
                return Response(
                    {"error": "word_count must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # contains_character filter
        if 'contains_character' in request.query_params:
            contains_char = request.query_params.get('contains_character')
            if len(contains_char) != 1:
                return Response(
                    {"error": "contains_character must be a single character."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(value__contains=contains_char)
            filters_applied['contains_character'] = contains_char
        
    except Exception as e:
        return Response(
            {"error": f"Invalid query parameters: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Serialize and return results
    serializer = StringAnalysisSerializer(queryset, many=True)
    response_data = {
        'data': serializer.data,
        'count': queryset.count(),
        'filters_applied': filters_applied
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


def parse_natural_language_query(query_string):
    """
    Parse natural language query to extract filters.
    
    Supports:
    - "palindrome/palindromic" → is_palindrome=true
    - "single word" → word_count=1
    - "longer than X characters" → min_length=X+1
    - "shorter than X" → max_length=X-1
    - "contains letter X" / "containing X" → contains_character=X
    - "first vowel" → contains_character=a
    
    Returns:
        Dictionary of parsed filters
    """
    filters = {}
    query_lower = query_string.lower()
    
    # Check for palindrome
    if 'palindrome' in query_lower or 'palindromic' in query_lower:
        filters['is_palindrome'] = True
    
    # Check for single word
    if 'single word' in query_lower:
        filters['word_count'] = 1
    
    # Check for "longer than X characters"
    longer_match = re.search(r'longer than (\d+)', query_lower)
    if longer_match:
        x = int(longer_match.group(1))
        filters['min_length'] = x + 1
    
    # Check for "shorter than X"
    shorter_match = re.search(r'shorter than (\d+)', query_lower)
    if shorter_match:
        x = int(shorter_match.group(1))
        filters['max_length'] = x - 1
    
    # Check for "contains letter X" or "containing X"
    contains_match = re.search(r'contain(?:s|ing)\s+(?:letter\s+)?([a-z])', query_lower)
    if contains_match:
        filters['contains_character'] = contains_match.group(1)
    
    # Check for "first vowel"
    if 'first vowel' in query_lower:
        filters['contains_character'] = 'a'
    
    return filters


@api_view(['GET'])
def filter_by_natural_language(request):
    """
    GET /strings/filter-by-natural-language
    
    Query parameter: query (the natural language string)
    
    Parse natural language to extract filters and return matching strings.
    
    Returns:
        {
            "data": [array of objects],
            "count": int,
            "interpreted_query": {
                "original_query": "string",
                "parsed_filters": {}
            }
        }
    
    Responses:
        200 OK: Success
        400 Bad Request: Unparseable query
        422 Unprocessable Entity: Conflicting filters
    """
    query_string = request.query_params.get('query', '')
    
    if not query_string:
        return Response(
            {"error": "The 'query' parameter is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Parse the natural language query
    try:
        parsed_filters = parse_natural_language_query(query_string)
    except Exception as e:
        return Response(
            {"error": f"Unable to parse query: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check for conflicting filters (min_length > max_length)
    if 'min_length' in parsed_filters and 'max_length' in parsed_filters:
        if parsed_filters['min_length'] > parsed_filters['max_length']:
            return Response(
                {
                    "error": "Conflicting filters: min_length cannot be greater than max_length.",
                    "parsed_filters": parsed_filters
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    
    # Apply filters to queryset
    queryset = StringAnalysis.objects.all()
    
    if 'is_palindrome' in parsed_filters:
        queryset = queryset.filter(is_palindrome=parsed_filters['is_palindrome'])
    
    if 'min_length' in parsed_filters:
        queryset = queryset.filter(length__gte=parsed_filters['min_length'])
    
    if 'max_length' in parsed_filters:
        queryset = queryset.filter(length__lte=parsed_filters['max_length'])
    
    if 'word_count' in parsed_filters:
        queryset = queryset.filter(word_count=parsed_filters['word_count'])
    
    if 'contains_character' in parsed_filters:
        queryset = queryset.filter(value__contains=parsed_filters['contains_character'])
    
    # Serialize and return results
    serializer = StringAnalysisSerializer(queryset, many=True)
    response_data = {
        'data': serializer.data,
        'count': queryset.count(),
        'interpreted_query': {
            'original_query': query_string,
            'parsed_filters': parsed_filters
        }
    }
    
    return Response(response_data, status=status.HTTP_200_OK)

