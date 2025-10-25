"""
app.py.

Application entry point for the HNG FastAPI service.

This module initializes logging, creates the FastAPI application
instance, registers API routers, and launches the Uvicorn ASGI server.

Usage
-----
Run the application locally:

    $ python app.py

Or use Uvicorn directly (recommended for production):

    $ uvicorn hng.app:app --host 0.0.0.0 --port 8000 --reload

Environment Variables
---------------------
- DATABASE_URL : str
    Database connection URL for SQLAlchemy.
- LOG_LEVEL : str
    Optional. Logging level (e.g., INFO, DEBUG, ERROR).

Example
-------
    >>> from hng import create_app
    >>> from hng.logger import setup_logger
    >>> app = create_app()
    >>> logger = setup_logger()
    >>> logger.info("HNG API started successfully.")
"""

import uvicorn

from hng import create_app
from hng.logger import setup_logger
from hng.routes.route import string_router

# Initialize Logging and Application
logger = setup_logger()
app = create_app()

# Register routers
app.include_router(string_router)


# Application Entrypoint
if __name__ == "__app__":
    logger.info("HNG API started successfully.")
    uvicorn.run(
        "hng.app:app",  # better than passing the app object directly
        host="127.0.0.1",
        port=8000,
        reload=True,  # better flag for dev than 'debug'
        log_level="info",
    )
