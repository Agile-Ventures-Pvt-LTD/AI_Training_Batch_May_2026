"""
Standardized API Response Format - C-4: Proper error handling with status codes

All API responses follow this standardized format for consistency and client error handling.
"""

from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from datetime import datetime


class ResponseStatus(Enum):
    """Standard response status codes"""

    SUCCESS = 'success'  # Fresh, successful data
    PARTIAL = 'partial'  # Degraded service, using cache/fallback
    FAILED = 'failed'  # Complete failure, no data
    CACHED = 'cached'  # Cached/fallback data


@dataclass
class APIResponse:
    """
    Standardized API response with status tracking.

    Clients can use the status field to determine how to handle the response:
    - SUCCESS (200): Fresh data, all good
    - PARTIAL (206): Stale/cached data, service degraded
    - FAILED (503): No data available, service unavailable
    """

    status: ResponseStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    is_fallback: bool = False
    is_stale: bool = False
    timestamp: str = None
    cache_age_seconds: Optional[int] = None

    def __post_init__(self):
        """Initialize timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary"""
        response_dict = {
            'status': self.status.value if isinstance(self.status, ResponseStatus) else self.status,
            'data': self.data,
            'error': self.error,
            'error_code': self.error_code,
            'is_fallback': self.is_fallback,
            'is_stale': self.is_stale,
            'timestamp': self.timestamp,
        }

        if self.cache_age_seconds is not None:
            response_dict['cache_age_seconds'] = self.cache_age_seconds

        return response_dict


# ✅ C-4: Standardized error response format
ERROR_RESPONSE_SCHEMA = {
    'status': 'error',
    'error': 'Human readable error message',
    'error_code': 'MACHINE_READABLE_CODE',
    'details': {},  # Optional additional details
    'timestamp': 'ISO8601 timestamp',
}


def create_error_response(
    error_message: str,
    error_code: str,
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create standardized error response.

    Args:
        error_message: Human-readable error message
        error_code: Machine-readable error code
        status_code: HTTP status code
        details: Optional additional error details

    Returns:
        Standardized error response dictionary
    """
    return {
        'status': ResponseStatus.FAILED.value,
        'error': error_message,
        'error_code': error_code,
        'details': details or {},
        'timestamp': datetime.utcnow().isoformat(),
        'http_status': status_code,
    }


def create_success_response(
    data: Dict[str, Any],
    message: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create standardized success response.

    Args:
        data: Response data
        message: Optional success message

    Returns:
        Standardized success response dictionary
    """
    return {
        'status': ResponseStatus.SUCCESS.value,
        'data': data,
        'message': message,
        'timestamp': datetime.utcnow().isoformat(),
    }


def create_partial_response(
    data: Dict[str, Any],
    warning: str,
    cache_age_seconds: int,
) -> Dict[str, Any]:
    """
    Create standardized partial/degraded response.

    Args:
        data: Cached/fallback data
        warning: Warning message explaining degradation
        cache_age_seconds: Age of cached data

    Returns:
        Standardized partial response dictionary
    """
    return {
        'status': ResponseStatus.PARTIAL.value,
        'data': data,
        'warning': warning,
        'is_fallback': True,
        'is_stale': True,
        'cache_age_seconds': cache_age_seconds,
        'timestamp': datetime.utcnow().isoformat(),
    }
