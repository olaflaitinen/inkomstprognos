"""Structured logging configuration using structlog."""

from __future__ import annotations

import os
import sys

import structlog


def _is_ci() -> bool:
    return os.environ.get("CI", "").lower() in ("true", "1", "yes")


def configure_logging() -> None:
    """Configure structlog with JSON renderer in CI and console renderer locally.

    Examples:
        >>> configure_logging()
    """
    processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.TimeStamper(fmt="iso"),
    ]
    if _is_ci() or not sys.stderr.isatty():
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(0),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a named structured logger.

    Args:
        name: Logger name, typically the module name.

    Returns:
        A bound structlog logger instance.

    Raises:
        ValueError: If name is empty.

    Examples:
        >>> log = get_logger("test")
    """
    if not name:
        msg = "Logger name must be non-empty"
        raise ValueError(msg)
    configure_logging()
    return structlog.get_logger(name)  # type: ignore[no-any-return]
