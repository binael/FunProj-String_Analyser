"""
nl_parser.py.

Schema defining the response structure for natural language query results.

This module contains the `NLParser` model, which represents the API
response when a natural language query is parsed and applied to filter
analyzed strings. It includes the filtered data, record count, and the
interpreted query in a structured format.

Classes
-------
NLParser
    Schema representing the result of a natural language filter query.
"""

from typing import Any

from pydantic import BaseModel, Field

from hng.schema.string_response import StringResponse


class NLParser(BaseModel):
    """
    Schema representing results of a natural language query interpretation.

    Attributes
    ----------
    data : List[StringResponse]
        A list of analyzed strings that match the interpreted natural
        language filter criteria.

    count : int
        Total number of records that matched the interpreted query.

    interpreted_query : Dict[str, Any]
        The structured form of the interpreted natural language input.
        This may include recognized conditions, filters, or properties.
    """

    data: list[StringResponse] = Field(
        ..., description="List of analyzed strings matching the query."
    )
    count: int = Field(..., description="Total number of matches found.")
    interpreted_query: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured interpretation of the natural language query.",
    )
