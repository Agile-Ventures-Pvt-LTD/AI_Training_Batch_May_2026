"""
Logging Utilities - Structured logging for observability

Provides structured logging with correlation IDs, performance metrics, and monitoring hooks.
"""

import logging
import time
import functools
from typing import Optional, Dict, Any
from datetime import datetime
from contextvars import ContextVar

# Context variable for correlation ID (tracks requests across services)
correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID for this context"""
    return correlation_id_var.get()


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID for request tracking"""
    correlation_id_var.set(correlation_id)


class StructuredLogger:
    """
    ✅ H-9+: Structured logging with correlation IDs and metrics.

    Provides consistent logging format for monitoring and debugging.
    """

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get logger for a module"""
        return logging.getLogger(name)

    @staticmethod
    def log_api_request(
        logger: logging.Logger,
        method: str,
        path: str,
        user_id: Optional[str] = None,
    ) -> None:
        """Log incoming API request"""
        correlation_id = get_correlation_id()
        logger.info(
            f"API request",
            extra={
                'correlation_id': correlation_id,
                'method': method,
                'path': path,
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def log_api_response(
        logger: logging.Logger,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        user_id: Optional[str] = None,
    ) -> None:
        """Log outgoing API response"""
        correlation_id = get_correlation_id()
        log_level = logging.INFO if 200 <= status_code < 400 else logging.WARNING

        logger.log(
            log_level,
            f"API response: {method} {path} {status_code}",
            extra={
                'correlation_id': correlation_id,
                'method': method,
                'path': path,
                'status_code': status_code,
                'duration_ms': f"{duration_ms:.1f}",
                'user_id': user_id,
                'timestamp': datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def log_database_query(
        logger: logging.Logger,
        query: str,
        duration_ms: float,
        rows_affected: int = 0,
    ) -> None:
        """Log database query with metrics"""
        correlation_id = get_correlation_id()
        logger.debug(
            f"Database query executed in {duration_ms:.1f}ms",
            extra={
                'correlation_id': correlation_id,
                'query': query[:100],  # Log first 100 chars only
                'duration_ms': f"{duration_ms:.1f}",
                'rows_affected': rows_affected,
            }
        )

    @staticmethod
    def log_external_api_call(
        logger: logging.Logger,
        api_name: str,
        endpoint: str,
        status_code: int,
        duration_ms: float,
    ) -> None:
        """Log external API call"""
        correlation_id = get_correlation_id()
        log_level = logging.INFO if 200 <= status_code < 400 else logging.WARNING

        logger.log(
            log_level,
            f"External API call: {api_name} {endpoint}",
            extra={
                'correlation_id': correlation_id,
                'api_name': api_name,
                'endpoint': endpoint,
                'status_code': status_code,
                'duration_ms': f"{duration_ms:.1f}",
            }
        )

    @staticmethod
    def log_error(
        logger: logging.Logger,
        error_code: str,
        message: str,
        exception: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log error with context"""
        correlation_id = get_correlation_id()
        extra = {
            'correlation_id': correlation_id,
            'error_code': error_code,
            'timestamp': datetime.utcnow().isoformat(),
        }

        if context:
            extra.update(context)

        if exception:
            logger.error(message, exc_info=exception, extra=extra)
        else:
            logger.error(message, extra=extra)

    @staticmethod
    def log_business_metric(
        logger: logging.Logger,
        metric_name: str,
        value: float,
        unit: str = '',
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log business metric for monitoring"""
        correlation_id = get_correlation_id()
        extra = {
            'correlation_id': correlation_id,
            'metric_name': metric_name,
            'value': value,
            'unit': unit,
        }

        if context:
            extra.update(context)

        logger.info(f"Metric: {metric_name} = {value}{unit}", extra=extra)


def log_performance(func):
    """
    ✅ Decorator to log function execution time and errors.

    Usage:
        @log_performance
        def calculate_kpis(data):
            return kpis
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000

            logger.info(
                f"{func.__name__} completed in {duration_ms:.1f}ms",
                extra={
                    'function': func.__name__,
                    'duration_ms': f"{duration_ms:.1f}",
                    'status': 'success',
                }
            )

            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000

            logger.error(
                f"{func.__name__} failed after {duration_ms:.1f}ms",
                exc_info=e,
                extra={
                    'function': func.__name__,
                    'duration_ms': f"{duration_ms:.1f}",
                    'status': 'failed',
                    'error_type': type(e).__name__,
                }
            )

            raise

    return wrapper


class PerformanceMonitor:
    """Context manager for performance monitoring"""

    def __init__(self, logger: logging.Logger, operation_name: str):
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000

        if exc_type is None:
            self.logger.info(
                f"Completed: {self.operation_name} ({duration_ms:.1f}ms)"
            )
        else:
            self.logger.error(
                f"Failed: {self.operation_name} ({duration_ms:.1f}ms)",
                exc_info=(exc_type, exc_val, exc_tb)
            )

        return False


# Example usage:
"""
✅ H-9+: Logging usage patterns

# Log API request/response
logger = StructuredLogger.get_logger(__name__)
StructuredLogger.log_api_request(logger, 'POST', '/api/kpis', user_id='user_123')
StructuredLogger.log_api_response(logger, 'POST', '/api/kpis', 200, 45.2, user_id='user_123')

# Log with decorator
@log_performance
def process_data(data):
    return transformed_data

# Log with context manager
with PerformanceMonitor(logger, "KPI Calculation"):
    kpis = calculate_kpis(data)

# Log business metrics
StructuredLogger.log_business_metric(
    logger,
    'revenue',
    50000.0,
    unit='USD',
    context={'merchant_id': 'merchant_123'}
)

# Log errors
try:
    result = risky_operation()
except Exception as e:
    StructuredLogger.log_error(
        logger,
        'CALCULATION_ERROR',
        'Failed to calculate KPIs',
        exception=e,
        context={'merchant_id': 'merchant_123', 'period': 'monthly'}
    )
"""
