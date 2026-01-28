"""
Logging configuration for After Effects Automation.

Usage:
    from ae_automation.logging_config import get_logger
    logger = get_logger(__name__)

Log level is controlled by the AE_LOG_LEVEL environment variable
(default: INFO). The CLI --verbose flag sets it to DEBUG.
"""
import logging
import os

_LOG_FORMAT = "%(levelname)s: %(message)s"
_DEBUG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"

_configured = False


def setup_logging(level=None):
    """
    Configure the root ae_automation logger.

    Args:
        level: logging level (e.g. logging.DEBUG). If None, reads
               AE_LOG_LEVEL env var, defaulting to INFO.
    """
    global _configured

    if level is None:
        env_level = os.environ.get("AE_LOG_LEVEL", "INFO").upper()
        level = getattr(logging, env_level, logging.INFO)

    fmt = _DEBUG_FORMAT if level <= logging.DEBUG else _LOG_FORMAT

    root_logger = logging.getLogger("ae_automation")
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates on re-setup
    root_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt))
    root_logger.addHandler(handler)

    _configured = True


def get_logger(name):
    """
    Return a logger under the ae_automation namespace.

    Lazily calls setup_logging() if it hasn't been called yet.
    """
    if not _configured:
        setup_logging()
    return logging.getLogger(name)
