"""
hng package.

This is the root package for the HNG String Analysis application.

It provides the application factory pattern through `create_app()`, sets
up the FastAPI instance, configures middleware, and initializes the
database at startup.

Modules
-------
- model.analyser : Defines ORM models and database initialization logic.
- logger : Provides JSON-based structured logging.
- api : Contains route definitions and request handlers.

Usage
-----
    >>> from hng import create_app
    >>> app = create_app()

Run using:
    $ uvicorn hng.app:app --reload

Features
--------
- 🧠 String analysis (length, palindrome check, unique characters, word count)
- 🧮 Character frequency mapping (JSONB field)
- 🌐 Natural language-based filtering without AI models
- 🗄️ PostgreSQL async database backend
- ⚙️ Built-in CORS configuration for cross-origin support
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hng.model.analyser import create_db_and_tables


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    This function initializes the FastAPI app with metadata, middleware,
    and startup/shutdown events using the lifespan context manager.
    It also triggers asynchronous database table creation on startup.

    Returns
    -------
    FastAPI
        Configured FastAPI application instance.

    Example
    -------
        >>> from hng import create_app
        >>> app = create_app()
        >>> import uvicorn
        >>> uvicorn.run(app, host="0.0.0.0", port=8000)
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """
        Lifespan context manager for startup and shutdown tasks.

        Runs before the app starts serving requests and after it shuts down.

        Parameters
        ----------
        app : FastAPI
            The FastAPI application instance.

        Yields
        ------
        None
            Control back to the FastAPI event loop.
        """
        await create_db_and_tables()
        yield
        # Add cleanup or background shutdown tasks here if needed.

    app = FastAPI(
        title="HNG String Analysis API",
        description=(
            "### 🧠 Overview\n"
            "This RESTful API analyzes input strings and stores their "
            "computed properties in a PostgreSQL database.\n\n"
            "**For each string, it computes:**\n"
            "- **length** → Number of characters\n"
            "- **is_palindrome** → Whether it reads the same backward\n"
            "- **unique_characters** → Count of distinct characters\n"
            "- **word_count** → Number of words\n"
            "- **sha256_hash** → Unique SHA-256 identifier\n"
            "- **character_frequency_map** → Count of each character\n\n"
            "The API supports:\n"
            "- 🔹 Creating and analyzing strings\n"
            "- 🔹 Retrieving a specific analyzed string\n"
            "- 🔹 Filtering strings by properties\n"
            "- 🔹 Natural language filtering (without AI models)\n"
            "- 🔹 Deleting strings\n"
        ),
        version="1.0.0",
        contact={
            "name": "Binael Nchekwube",
            "url": "https://binael.tech",
            "email": "nbinael@yahoo.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        lifespan=lifespan,
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Consider restricting in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
