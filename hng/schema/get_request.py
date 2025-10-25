"""
get_request.py.

Pydantic schema for handling query parameters in GET requests.

This module defines the data validation model used to process and
validate query inputs passed to the string analysis API. The schema
ensures that all incoming query data conforms to the expected type
and structure before it reaches the service or database layer.

Classes
-------
GetRequest
    Schema for a simple query input containing an optional string value.
"""

from typing import Any

from pydantic import BaseModel, Field


class GetRequest(BaseModel):
    """
    Schema for handling GET request query parameters.

    Attributes
    ----------
    value : Optional[str]
        The input string value to be analyzed or filtered.
        Defaults to None if not provided.
    """

    value: Any = Field(..., description="String to analyze")
