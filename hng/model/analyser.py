"""
analyser.py.

Asynchronous SQLAlchemy model and database configuration for text analysis.

This module defines the `Analyser` model, which stores results of text
analyses such as length, word count, palindrome status, and character
frequency distribution. It also initializes the asynchronous SQLAlchemy
engine and sessionmaker used across the application.

Environment Variables
---------------------
DATABASE_URL : str
    The database connection URL
    (e.g., "postgresql+asyncpg://user:pass@localhost/db").

Exports
--------
Base : DeclarativeBase
    The declarative base class for all ORM models.
Analyser : Declarative model
    Represents analysis results for a given text entry.
engine : AsyncEngine
    SQLAlchemy asynchronous engine.
AsyncSessionLocal : async_sessionmaker
    Factory for creating `AsyncSession` objects.
create_db_and_tables() : Coroutine
    Initializes all database tables based on model metadata.

Example
-------
    >>> from hng.model.analyser import (
    ...     AsyncSessionLocal,
    ...     create_db_and_tables,
    ...     Analyser
    ...     )
    >>> async with AsyncSessionLocal() as session:
    ...     new_item = Analyser(
    ...         id="123",
    ...         sha256_hash="123",
    ...         name="example",
    ...         length=7,
    ...         word_count=1,
    ...         is_palindrome=False,
    ...         unique_characters=6,
    ...         character_frequency_map={
    ...             "e": 2, "x": 1, "a": 1, "m": 1, "p": 1, "l": 1
    ...             },
    ...     )
    ...     session.add(new_item)
    ...     await session.commit()
"""

import os

from dotenv import load_dotenv
from sqlalchemy import DateTime, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()
# Database Configuration
DATABASE_URL: str = os.environ.get("DATABASE_URL")


# Base Class
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Analyser Model
class Analyser(Base):
    """
    Represents the results of a text analysis operation.

    Stores metadata about a given text, including its name, length,
    word count, palindrome status, unique characters, and a character
    frequency map stored as JSONB.

    Parameters
    ----------
    Base : DeclarativeBase
        Inherited base class for SQLAlchemy ORM models.

    Attributes
    ----------
    id : Mapped[str]
        Primary key identifier for the analysis record.
    name : Mapped[str]
        Name or label of the analyzed text.
    length : Mapped[int]
        Total number of characters in the text.
    word_count : Mapped[int]
        Number of words in the text.
    is_palindrome : Mapped[bool]
        Whether the text is a palindrome.
    unique_characters : Mapped[int]
        Count of unique characters in the text.
    character_frequency_map : Mapped[dict[str, int]]
        Dictionary mapping each character to its frequency (stored as JSONB).
    created_at : Mapped[DateTime]
        Timestamp when the record was created.

    Table Constraints
    -----------------
    - UniqueConstraint: Ensures that each text `name` is unique.
    """

    __tablename__ = "analyser"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    sha256_hash: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    length: Mapped[int] = mapped_column(nullable=False)
    word_count: Mapped[int] = mapped_column(nullable=False)
    is_palindrome: Mapped[bool] = mapped_column(nullable=False)
    unique_characters: Mapped[int] = mapped_column(nullable=False)
    character_frequency_map: Mapped[dict[str, int]] = mapped_column(
        JSONB, nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )

    __table_args__ = (UniqueConstraint("value", name="uq_analyser_value"),)


# Async Engine and Session Factory
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Database Initialization
async def create_db_and_tables() -> None:
    """
    Create all database tables defined in the SQLAlchemy metadata.

    This coroutine initializes the database schema by running
    `Base.metadata.create_all` within an asynchronous connection.

    Returns
    -------
    None
        This function performs schema creation but does not return a value.

    Example
    -------
        >>> import asyncio
        >>> from hng.model.analyser import create_db_and_tables
        >>> asyncio.run(create_db_and_tables())
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
