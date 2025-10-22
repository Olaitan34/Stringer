"""
Serializers for the strings_app application.
"""
from rest_framework import serializers
from .models import StringAnalysis


class StringAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for StringAnalysis model.
    
    Returns data in the format:
    {
        "id": "sha256_hash",
        "value": "the string",
        "properties": {
            "length": int,
            "is_palindrome": bool,
            "unique_characters": int,
            "word_count": int,
            "sha256_hash": "string",
            "character_frequency_map": {}
        },
        "created_at": "ISO8601 datetime"
    }
    """
    properties = serializers.SerializerMethodField()
    
    class Meta:
        model = StringAnalysis
        fields = ['id', 'value', 'properties', 'created_at']
        read_only_fields = ['id', 'properties', 'created_at']
    
    def get_properties(self, obj):
        """Return the properties dictionary."""
        return obj.properties
    
    def validate_value(self, value):
        """
        Validate that value is a string and not empty.
        """
        if not isinstance(value, str):
            raise serializers.ValidationError("Value must be a string.", code='invalid_type')
        
        if not value or value.strip() == '':
            raise serializers.ValidationError("Value cannot be empty.", code='empty_value')
        
        return value
    
    def create(self, validated_data):
        """
        Create a new StringAnalysis instance.
        
        Raises:
            serializers.ValidationError: If the string already exists (409 Conflict)
        """
        value = validated_data.get('value')
        
        # Check if string already exists
        if StringAnalysis.objects.filter(value=value).exists():
            raise serializers.ValidationError(
                {"error": "String already exists in the database."},
                code='conflict'
            )
        
        # Create and return the instance
        return StringAnalysis.objects.create(**validated_data)


class StringListSerializer(serializers.Serializer):
    """
    Serializer for listing strings with filters.
    
    Returns:
    {
        "data": [array of StringAnalysis objects],
        "count": int,
        "filters_applied": {}
    }
    """
    data = StringAnalysisSerializer(many=True)
    count = serializers.IntegerField()
    filters_applied = serializers.DictField()


class NaturalLanguageQuerySerializer(serializers.Serializer):
    """
    Serializer for natural language query results.
    
    Returns:
    {
        "data": [array of StringAnalysis objects],
        "count": int,
        "interpreted_query": {
            "original_query": "string",
            "parsed_filters": {}
        }
    }
    """
    data = StringAnalysisSerializer(many=True)
    count = serializers.IntegerField()
    interpreted_query = serializers.DictField()
