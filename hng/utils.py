"""
utils.py.

Utility functions for analyzing string properties.

This module provides helper functions to compute:
- Word count
- Palindrome status
- Unique character count
- Character frequency map
- SHA-256 hash

These utilities are used by the string analysis service layer
and exposed through the API endpoints.
"""

import hashlib
import re
from typing import Any


def get_word_count(sentence: str) -> int:
    """
    Count the number of words in a sentence.

    Parameters
    ----------
    sentence : str
        The input string.

    Returns
    -------
    int
        The number of words found.

    Example
    -------
    >>> get_word_count("Hello world, again!")
    3
    """
    words = re.findall(r"\b\w+\b", sentence.lower())
    return len(words)


def get_is_palindrome(sentence: str) -> bool:
    """
    Check whether a string is a palindrome.

    Ignores case, spaces, and non-alphanumeric characters.

    Parameters
    ----------
    sentence : str
        The input string.

    Returns
    -------
    bool
        True if the string is a palindrome, False otherwise.

    Example
    -------
    >>> get_is_palindrome("Madam, I'm Adam")
    True
    """
    normalized = sentence.lower()
    return normalized == normalized[::-1]


def get_unique_characters(sentence: str) -> int:
    """
    Count the number of unique characters in the string.

    Parameters
    ----------
    sentence : str
        The input string.

    Returns
    -------
    int
        Count of distinct characters (case-insensitive).

    Example
    -------
    >>> get_unique_characters("Hello")
    4
    """
    return len(set(sentence.lower()))


def get_character_frequency_map(sentence: str) -> dict[str, int]:
    """
    Build a frequency map of characters in the string.

    Parameters
    ----------
    sentence : str
        The input string.

    Returns
    -------
    Dict[str, int]
        A mapping of each lowercase character to its count.

    Example
    -------
    >>> get_character_frequency_map("aabB")
    {'a': 2, 'b': 2}
    """
    freq: dict[str, int] = {}
    for char in sentence.lower():
        if char.strip():
            freq[char] = freq.get(char, 0) + 1
    return freq


def get_sha256(sentence: str) -> str:
    """
    Generate a SHA-256 hash of the input string.

    Parameters
    ----------
    sentence : str
        The input string.

    Returns
    -------
    str
        A 64-character hexadecimal SHA-256 hash.

    Example
    -------
    >>> get_sha256("Hello")
    '185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969'
    """
    return hashlib.sha256(sentence.lower().encode("utf-8")).hexdigest()


def create_properties(sentence: str) -> dict[str, Any]:
    """
    Compute and return all string analysis properties.

    Parameters
    ----------
    sentence : str
        The input string to analyze.

    Returns
    -------
    Dict[str, Any]
        A dictionary of computed properties:
        {
            "length": int,
            "is_palindrome": bool,
            "unique_characters": int,
            "word_count": int,
            "sha256_hash": str,
            "character_frequency_map": dict
        }

    Example
    -------
    >>> create_properties("Level up")
    {
        'length': 8,
        'is_palindrome': False,
        'unique_characters': 6,
        'word_count': 2,
        'sha256_hash': '...',
        'character_frequency_map': {'l': 2, 'e': 2, 'v': 1, 'u': 1, 'p': 1}
    }
    """
    return {
        "length": len(sentence),
        "is_palindrome": get_is_palindrome(sentence),
        "unique_characters": get_unique_characters(sentence),
        "word_count": get_word_count(sentence),
        "sha256_hash": get_sha256(sentence),
        "character_frequency_map": get_character_frequency_map(sentence),
    }
