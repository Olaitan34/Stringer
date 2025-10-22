"""
Utility functions for string analysis.
"""
import hashlib
from typing import Dict, Any


def analyze_string(value: str) -> Dict[str, Any]:
    """
    Analyze a string and compute all its properties.
    
    Args:
        value: The string to analyze
        
    Returns:
        Dictionary containing all computed properties:
        - length: len(string)
        - is_palindrome: Check if string is a palindrome (case-insensitive, ignoring spaces)
        - unique_characters: Count of unique characters
        - word_count: Number of words (split by whitespace)
        - sha256_hash: SHA-256 hash of the string
        - character_frequency_map: Dictionary with character frequencies
    """
    # Length
    length = len(value)
    
    # Palindrome check (case-insensitive, ignoring spaces)
    cleaned_value = value.replace(' ', '').lower()
    is_palindrome = cleaned_value == cleaned_value[::-1]
    
    # Unique characters
    unique_characters = len(set(value))
    
    # Word count
    word_count = len(value.split())
    
    # SHA-256 hash
    sha256_hash = hashlib.sha256(value.encode()).hexdigest()
    
    # Character frequency map (includes ALL characters: letters, spaces, punctuation)
    character_frequency_map = {}
    for char in value:
        character_frequency_map[char] = character_frequency_map.get(char, 0) + 1
    
    return {
        'length': length,
        'is_palindrome': is_palindrome,
        'unique_characters': unique_characters,
        'word_count': word_count,
        'sha256_hash': sha256_hash,
        'character_frequency_map': character_frequency_map,
    }


def compute_sha256(value: str) -> str:
    """
    Compute SHA-256 hash of a string.
    
    Args:
        value: The string to hash
        
    Returns:
        The SHA-256 hash as a hexadecimal string
    """
    return hashlib.sha256(value.encode()).hexdigest()
