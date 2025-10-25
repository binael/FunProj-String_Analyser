"""
logger.py.

Custom JSON-based logging configuration module.

This module defines a `JsonFormatter` class for structured JSON logs and a
`setup_logger` function to configure both console and rotating file handlers.

The resulting logs are structured, easily parseable, and suitable for
modern monitoring or log aggregation systems such as ELK Stack, Datadog,
and CloudWatch.

Directory Structure
-------------------
- logs/
    - app.log  (auto-created with rotation enabled)

Usage
-----
    >>> from logging_config import setup_logger
    >>> logger = setup_logger()
    >>> logger.info("Application started.")
    >>> logger.error("Something went wrong!", exc_info=True)

Example Output
--------------
    {
        "timestamp": "2025-10-23T12:10:45",
        "level": "INFO",
        "logger": "root",
        "message": "Application started.",
        "pathname": "/app/main.py",
        "lineno": 42
    }

Classes
-------
JsonFormatter
    A custom logging formatter that serializes log records as JSON.

Functions
---------
setup_logger() -> logging.Logger
    Configures and returns a global logger with both console
    and rotating file handlers.
"""

import json
import logging
import os
from logging.handlers import RotatingFileHandler


# -------------------------------------------------------------------------
# Custom Formatter
# -------------------------------------------------------------------------
class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for logging records.

    Converts standard Python log records into structured JSON
    for consistent and machine-readable logging output.

    Parameters
    ----------
    logging : logging
        The Python logging module (used implicitly).

    Example
    -------
    >>> formatter = JsonFormatter()
    >>> record = logging.LogRecord(
    ...    "app", logging.INFO, __file__, 42, "Hello", None, None
    ...    )
    >>> print(formatter.format(record))
    {"timestamp": "2025-10-23T12:15:30", "level": "INFO", ...}
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as a JSON string.

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.

        Returns
        -------
        str
            JSON-encoded log information containing timestamp, level, message,
            logger name, and optional exception details.
        """
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
        }

        # Include exception information if available
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Add any custom attributes attached to the record
        for key, value in record.__dict__.items():
            if key not in (
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
            ):
                log_record[key] = value

        return json.dumps(log_record)


# -------------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------------
def setup_logger() -> logging.Logger:
    """
    Set up the root logger with both console and rotating file handlers.

    Creates a `logs` directory (if it does not exist) and configures
    a global logger instance using the custom `JsonFormatter`.

    The logger outputs to:
      - **Console** (stdout) for real-time logs.
      - **Rotating file** (`logs/app.log`) with up to 5 backup files,
        each capped at 500 KB.

    Returns
    -------
    logging.Logger
        A configured logger instance ready for application-wide use.

    Example
    -------
    >>> logger = setup_logger()
    >>> logger.info("Server started successfully.")
    >>> logger.warning("Memory usage high.")
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    json_formatter = JsonFormatter()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # Rotating file handler
    rotating_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=500 * 1024,  # 500 KB
        backupCount=5,
    )
    rotating_handler.setFormatter(json_formatter)
    logger.addHandler(rotating_handler)

    return logger
