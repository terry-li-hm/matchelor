import logging
import sys
from typing import Any

import structlog


def configure_logging() -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
            if sys.stdout.isatty()
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    return structlog.get_logger(name)


def log_api_request(endpoint: str, method: str, **kwargs: Any) -> dict[str, Any]:
    return {
        "event": "api_request",
        "endpoint": endpoint,
        "method": method,
        **kwargs,
    }


def log_llm_call(model: str, latency_ms: int, **kwargs: Any) -> dict[str, Any]:
    return {
        "event": "llm_call",
        "model": model,
        "latency_ms": latency_ms,
        **kwargs,
    }


def log_classification_result(
    intent: str, confidence: float, **kwargs: Any
) -> dict[str, Any]:
    return {
        "event": "classification_result",
        "intent": intent,
        "confidence": confidence,
        **kwargs,
    }
