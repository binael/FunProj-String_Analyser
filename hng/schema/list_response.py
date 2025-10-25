"""
list_response.py.

Schema defining the response structure for a list of analyzed strings.

This module contains the `ListResponse` model, which represents the
paginated or filtered collection of analyzed strings returned by the
API. It includes the analyzed string data, total count, and a record
of applied filters (if any).

Classes
-------
ListResponse
    Schema representing a collection of analyzed string responses.
"""

from typing import Any

from pydantic import BaseModel, Field

from hng.schema.string_response import StringResponse


class ListResponse(BaseModel):
    """
    Schema representing a list of analyzed strings with metadata.

    Attributes
    ----------
    data : List[StringResponse]
        A list of analyzed string objects containing string values
        and their computed properties.

    count : int
        The total number of records returned in the current response.

    filters_applied : Dict[str, Any]
        Dictionary of filters applied during the query, useful for
        debugging or for clients to confirm filter criteria.
    """

    data: list[StringResponse] = Field(
        ..., description="List of analyzed string results."
    )
    count: int = Field(..., description="Total number of results returned.")
    filters_applied: dict[str, Any] = Field(
        default_factory=dict,
        description="Filters applied to the query (if any).",
    )
