"""
string_response.py.

Schema defining the response structure for analyzed strings.

This module contains the `StringResponse` model, which represents the
data returned by the API after analyzing and storing a string in the
database. It includes the string itself, computed properties, and
metadata such as creation timestamp.

Classes
-------
StringResponse
    Schema representing the full analyzed string response.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from hng.schema.properties_model import PropertiesModel


class StringResponse(BaseModel):
    """
    Schema representing the full response for a stored string analysis.

    This model combines the analyzed string, its computed properties,
    and metadata such as creation timestamp.

    Attributes
    ----------
    id : str
        The unique identifier (UUID or SHA-256 hash) of the analyzed string.

    value : str
        The original input string provided for analysis.

    properties : PropertiesModel
        Nested model containing computed string properties such as
        length, palindrome status, and character frequency map.

    created_at : datetime
        Timestamp of when the record was created in the database.
    """

    id: str = Field(..., description="Unique identifier of the analyzed string.")
    value: str = Field(..., description="Original string value analyzed.")
    properties: PropertiesModel = Field(
        ..., description="Computed analysis properties of the string."
    )
    created_at: datetime = Field(..., description="Creation timestamp of the record.")
