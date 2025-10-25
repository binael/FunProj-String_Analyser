"""
properties_model.py.

Pydantic schema for representing computed string analysis properties.

This module defines the structure of the response object returned by
the API after analyzing a string. It includes computed metadata such as
word count, palindrome status, unique character count, and frequency map.

These models help ensure consistent validation, serialization, and
OpenAPI schema generation for all string analysis responses.

Classes
-------
PropertiesModel
    Schema representing computed properties of a string.
"""

from pydantic import BaseModel, Field


class PropertiesModel(BaseModel):
    """
    Schema representing computed string analysis properties.

    This model is used for both database responses and API outputs
    when returning analyzed string results.
    """

    length: int = Field(..., description="Total number of characters in the string.")
    is_palindrome: bool = Field(..., description="True if the string is a palindrome.")
    unique_characters: int = Field(..., description="Count of distinct characters.")
    word_count: int = Field(..., description="Number of words in the string.")
    sha256_hash: str = Field(..., description="SHA-256 hash of the lowercase string.")
    character_frequency_map: dict[str, int] = Field(
        ..., description="Mapping of each character to its frequency count."
    )
