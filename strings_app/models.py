"""
Models for the strings_app application.
"""
from django.db import models
from .utils import analyze_string, compute_sha256


class StringAnalysis(models.Model):
    """
    Model to store string analysis results.
    
    The sha256_hash is used as the primary key (id field).
    """
    # Use sha256_hash as primary key
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    
    # The original string value (unique)
    value = models.TextField(unique=True, db_index=True)
    
    # Computed properties
    length = models.IntegerField(db_index=True)
    is_palindrome = models.BooleanField(default=False, db_index=True)
    unique_characters = models.IntegerField()
    word_count = models.IntegerField(db_index=True)
    sha256_hash = models.CharField(max_length=64, editable=False)
    character_frequency_map = models.JSONField()
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'string_analysis'
        verbose_name = 'String Analysis'
        verbose_name_plural = 'String Analyses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['value']),
            models.Index(fields=['is_palindrome']),
            models.Index(fields=['length']),
            models.Index(fields=['word_count']),
        ]
    
    def save(self, *args, **kwargs):
        """
        Override save method to compute properties before saving.
        """
        # Compute all properties using the utility function
        properties = analyze_string(self.value)
        
        # Set the computed properties
        self.length = properties['length']
        self.is_palindrome = properties['is_palindrome']
        self.unique_characters = properties['unique_characters']
        self.word_count = properties['word_count']
        self.sha256_hash = properties['sha256_hash']
        self.character_frequency_map = properties['character_frequency_map']
        
        # Set the id (primary key) to the sha256_hash
        self.id = self.sha256_hash
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.value[:50]}{'...' if len(self.value) > 50 else ''}"
    
    @property
    def properties(self):
        """
        Return all computed properties as a dictionary.
        """
        return {
            'length': self.length,
            'is_palindrome': self.is_palindrome,
            'unique_characters': self.unique_characters,
            'word_count': self.word_count,
            'sha256_hash': self.sha256_hash,
            'character_frequency_map': self.character_frequency_map,
        }
