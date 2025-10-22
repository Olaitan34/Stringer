from django.contrib import admin
from .models import StringAnalysis


@admin.register(StringAnalysis)
class StringAnalysisAdmin(admin.ModelAdmin):
    """
    Admin interface for StringAnalysis model.
    """
    list_display = ['value_preview', 'length', 'is_palindrome', 'word_count', 'created_at']
    list_filter = ['is_palindrome', 'created_at']
    search_fields = ['value', 'sha256_hash']
    readonly_fields = [
        'id', 'sha256_hash', 'length', 'is_palindrome', 
        'unique_characters', 'word_count', 'character_frequency_map', 'created_at'
    ]
    
    def value_preview(self, obj):
        """Show a preview of the value in the admin list."""
        return obj.value[:50] + ('...' if len(obj.value) > 50 else '')
    
    value_preview.short_description = 'String Value'
