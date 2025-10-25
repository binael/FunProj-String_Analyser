"""
dependencies.py.

This module provides a FastAPI dependency for managing asynchronous
SQLAlchemy sessions. It ensures that each request has a dedicated
database session that is properly created and closed.

Exports
-------
get_db_session() : Dependency generator that yields an AsyncSession.
sessionDep       : Type alias for dependency injection using `Depends`.

Example
-------
    from fastapi import APIRouter, Depends
    from sqlalchemy.ext.asyncio import AsyncSession
    from .db_session import sessionDep

    router = APIRouter()

    @router.get("/users")
    async def list_users(db: sessionDep):
        result = await db.execute("SELECT * FROM users;")
        return result.fetchall()
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from hng.model.analyser import AsyncSessionLocal


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous SQLAlchemy database session for request handling.

    This FastAPI dependency ensures each request receives its own
    database session within an async context manager. The session
    is automatically closed after the request is completed.

    Yields
    ------
    AsyncSession
        An active SQLAlchemy asynchronous session for performing
        database operations.

    Example
    -------
    >>> async for session in get_db_session():
    ...     result = await session.execute("SELECT 1")
    ...     print(result.scalar())
    """
    async with AsyncSessionLocal() as session:
        yield session


# Dependency annotation for injecting AsyncSession into route handlers
sessionDep = Annotated[AsyncSession, Depends(get_db_session)]
