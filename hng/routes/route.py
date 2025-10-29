"""
string_router.py.

This module defines API endpoints for creating, retrieving, and filtering
string analysis records. It provides operations to:

* Add new strings to the database with computed analytical properties.
* Retrieve details for a specific analyzed string.
* Filter existing records based on attributes such as palindrome status,
  string length, word count, or character inclusion.

Endpoints
---------
POST /strings/
    Create and store a new analyzed string.
GET /strings/{string_value}
    Retrieve the analysis details for a specific string.
GET /strings/
    Fetch multiple analyzed strings filtered by optional query parameters.

Raises
------
HTTPException
    - 400: When the request value is empty.
    - 404: When no data matches the request criteria.
    - 409: When the value already exists in the database.
    - 422: When invalid data types or constraints are provided.

Dependencies
------------
- `sessionDep` (AsyncSession): Injected dependency for database interaction.
- `Analyser` (SQLAlchemy Model): ORM model representing analyzed strings.
- `create_properties`: Utility function that computes string analysis properties.
- `get_sha256`: Utility to generate unique hash identifiers for strings.

Author
------
Your Name <you@example.com>
"""

import logging
from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlalchemy import select
from sqlmodel import and_
import httpx
import json

from hng.dependencies import sessionDep
from hng.model.analyser import Analyser
from hng.schema.get_request import GetRequest
from hng.schema.list_response import ListResponse
from hng.schema.properties_model import PropertiesModel
from hng.schema.string_response import StringResponse
from hng.utils import create_properties, get_sha256

NLP_API_URL = "https://nlp-funproj-string-analyser.onrender.com"
logger = logging.getLogger(__name__)

string_router = APIRouter(
    prefix="/strings",
    tags=["strings"],
)

# Default Error Messages
DOES_NOT_EXIST = "value does not exist"
DUPLICATE_VALUE = "String already exists in the system"
NOT_STRING = '"value" must be a string'
EMPTY_STRING = '"value" field is required'


@string_router.post(
    "/", response_model=StringResponse, status_code=status.HTTP_201_CREATED
)
async def create_string(req: Annotated[GetRequest, Body()], session: sessionDep) -> Any:
    """
    Create and store a new analyzed string record.

    This endpoint receives a string value, computes its analytical properties,
    and persists it to the database. Duplicate and invalid entries are rejected.

    Parameters
    ----------
    req : GetRequest
        Request body containing the string to analyze.
    session : AsyncSession
        Database session dependency.

    Returns
    -------
    StringResponse
        Object containing the analyzed string and its computed properties.

    Raises
    ------
    HTTPException
        - 400: If the string is empty.
        - 409: If the string already exists.
        - 422: If the value is not a string.
    """
    if not req.value:
        raise HTTPException(status_code=400, detail=EMPTY_STRING)
    if not isinstance(req.value, str):
        raise HTTPException(status_code=422, detail=NOT_STRING)

    value = req.value.strip()
    prop = create_properties(value.lower())

    # Prevent duplicate entries based on hash or raw value
    if await session.get(Analyser, prop.get("sha256_hash")):
        raise HTTPException(status_code=409, detail=DUPLICATE_VALUE)
    statement = select(Analyser).where(Analyser.value == req.value)
    data = await session.execute(statement)
    data_row = data.scalars().first()
    if data_row:
        raise HTTPException(status_code=409, detail=DUPLICATE_VALUE)

    db = Analyser(
        id=prop.get("sha256_hash"),
        sha256_hash=prop.get("sha256_hash"),
        value=value,
        length=prop.get("length"),
        word_count=prop.get("word_count"),
        is_palindrome=prop.get("is_palindrome"),
        unique_characters=prop.get("unique_characters"),
        character_frequency_map=prop.get("character_frequency_map"),
        created_at=datetime.now(UTC),
    )
    session.add(db)
    await session.commit()
    await session.refresh(db)

    return StringResponse(
        id=db.id,
        value=db.value,
        properties=PropertiesModel(**prop),
        created_at=db.created_at,
    )


@string_router.get(
    "/{string_value}", response_model=StringResponse, status_code=status.HTTP_200_OK
)
async def get_string(session: sessionDep, string_value: Annotated[str, Path()]):
    """
    Retrieve an analyzed string by its raw value.

    Parameters
    ----------
    session : AsyncSession
        Database session dependency.
    string_value : str
        The string to retrieve.

    Returns
    -------
    StringResponse
        An object containing the string's analysis results.

    Raises
    ------
    HTTPException
        - 404: If the string does not exist.
    """
    value = string_value.strip()
    id = get_sha256(value.lower())

    statement = select(Analyser).where(Analyser.id == id)
    data = await session.execute(statement)
    result = data.scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail=DOES_NOT_EXIST)

    return {
        "properties": PropertiesModel(**result.__dict__),
        "id": result.id,
        "value": result.value,
        "created_at": result.created_at,
    }


@string_router.get("/", response_model=ListResponse, status_code=status.HTTP_200_OK)
async def get_all_strings(
    session: sessionDep,
    is_palindrome: Annotated[bool | None, Query()] = None,
    min_length: Annotated[int | None, Query()] = None,
    max_length: Annotated[int | None, Query()] = None,
    word_count: Annotated[int | None, Query()] = None,
    contains_character: Annotated[str | None, Query()] = None,
):
    """
    Retrieve all analyzed strings matching optional filters.

    Query Parameters
    ----------------
    is_palindrome : bool, optional
        Filter by palindrome property.
    min_length : int, optional
        Minimum string length to include.
    max_length : int, optional
        Maximum string length to include.
    word_count : int, optional
        Filter by word count.
    contains_character : str, optional
        Filter strings that include the specified character.

    Returns
    -------
    ListResponse
        A paginated list of matching string records and applied filters.

    Raises
    ------
    HTTPException
        - 404: If no results are found.
        - 422: If filter constraints are invalid.
    """
    if max_length and min_length and max_length < min_length:
        raise HTTPException(
            status_code=422, detail="Max length must be greater than Min length"
        )

    params = {}
    condition = []

    if is_palindrome is not None:
        condition.append(Analyser.is_palindrome == is_palindrome)
        params["is_palindrome"] = is_palindrome
    if min_length is not None:
        condition.append(Analyser.length >= min_length)
        params["min_length"] = min_length
    if max_length is not None:
        condition.append(Analyser.length <= max_length)
        params["max_length"] = max_length
    if word_count is not None:
        condition.append(Analyser.word_count == word_count)
        params["word_count"] = word_count
    if contains_character:
        char = contains_character.strip().lower()
        condition.append(Analyser.character_frequency_map.has_key(char))
        params["contains_character"] = contains_character

    if not condition:
        raise HTTPException(status_code=404, detail=DOES_NOT_EXIST)

    statement = select(Analyser).where(and_(*condition))
    data = await session.execute(statement)
    result = data.scalars().all()

    if not result:
        raise HTTPException(status_code=404, detail=DOES_NOT_EXIST)

    data = [
        StringResponse(
            id=r.id,
            value=r.value,
            properties=PropertiesModel(**r.__dict__),
            created_at=r.created_at,
        )
        for r in result
    ]

    return ListResponse(data=data, count=len(data), filters_applied=params)


@string_router.get("/filter-by-natural-language", status_code=status.HTTP_200_OK)
async def filter_by_natural_language(
    session: sessionDep,
    query: str = Query(..., description="Natural language query to parse filters from"),
):
    """
    Parse a natural language query into structured filters using the remote NLP API,
    then retrieve matching strings from the database.

    Example:
    --------
    GET /strings/filter-by-natural-language?query=strings%20longer%20than%2010%20characters

    Returns:
    --------
    {
        "data": [...],
        "count": 5,
        "interpreted_query": {
            "original": "strings longer than 10 characters",
            "parsed_filters": {"min_length": 11}
        }
    }
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NLP_API_URL, params={"query": query})
            response.raise_for_status()
            logger.info("Successfully retrieved filters from NLP API.")
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to reach NLP API: {exc}",
            )
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"NLP API returned error: {exc.response.text}",
            )

    try:
        parsed_filters = response.json()
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid JSON returned from NLP API",
        )

    if not parsed_filters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to parse natural language query",
        )
    return await parsed_filters

    # Apply parsed filters to the database query
    params = {}
    condition = []

    is_palindrome = parsed_filters.get("is_palindrome")
    min_length = parsed_filters.get("min_length")
    max_length = parsed_filters.get("max_length")
    word_count = parsed_filters.get("word_count")
    contains_character = parsed_filters.get("contains_character")

    if is_palindrome is not None:
        condition.append(Analyser.is_palindrome == is_palindrome)
        params["is_palindrome"] = is_palindrome
    if min_length is not None:
        condition.append(Analyser.length >= min_length)
        params["min_length"] = min_length
    if max_length is not None:
        condition.append(Analyser.length <= max_length)
        params["max_length"] = max_length
    if word_count is not None:
        condition.append(Analyser.word_count == word_count)
        params["word_count"] = word_count
    if contains_character:
        char = contains_character.strip().lower()
        condition.append(Analyser.character_frequency_map.has_key(char))
        params["contains_character"] = contains_character

    if not condition:
        raise HTTPException(status_code=404, detail=DOES_NOT_EXIST)

    statement = select(Analyser).where(and_(*condition))
    data = await session.execute(statement)
    result = data.scalars().all()

    if not result:
        raise HTTPException(status_code=404, detail=DOES_NOT_EXIST)

    data = [
        StringResponse(
            id=r.id,
            value=r.value,
            properties=PropertiesModel(**r.__dict__),
            created_at=r.created_at,
        )
        for r in result
    ]

    return {
        "data": data,
        "count": len(data),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters,
        },
    }
