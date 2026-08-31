"""
Error Handling Middleware - H-2: Standardized error responses

Ensures all API errors follow the same response format for consistency.
Catches exceptions and returns proper error responses with status codes.
"""

import logging
import traceback
from typing import Dict, Any, Tuple
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class StandardErrorResponse:
    """
    ✅ H-2: Standardized error response format for all endpoints.

    All errors use this format:
    {
        "status": "error",
        "error": "Human readable message",
        "error_code": "MACHINE_READABLE_CODE",
        "details": {},
        "timestamp": "ISO8601"
    }
    """

    # Error codes for common scenarios
    ERROR_CODES = {
        # Validation errors
        'VALIDATION_ERROR': (400, 'Validation failed'),
        'INVALID_FILE_TYPE': (400, 'Invalid file type'),
        'FILE_TOO_LARGE': (413, 'File too large'),
        'INVALID_PARAMETER': (400, 'Invalid parameter'),

        # Authentication/Authorization
        'UNAUTHORIZED': (401, 'Authentication required'),
        'FORBIDDEN': (403, 'Access denied'),
        'INVALID_CREDENTIALS': (401, 'Invalid credentials'),

        # Resource errors
        'NOT_FOUND': (404, 'Resource not found'),
        'CONFLICT': (409, 'Resource conflict'),

        # Rate limiting
        'RATE_LIMITED': (429, 'Too many requests'),

        # Server errors
        'INTERNAL_ERROR': (500, 'Internal server error'),
        'SERVICE_UNAVAILABLE': (503, 'Service unavailable'),
        'DATABASE_ERROR': (503, 'Database error'),
        'API_ERROR': (503, 'External API error'),
        'TIMEOUT': (504, 'Request timeout'),

        # Business logic errors
        'DATASET_NOT_FOUND': (404, 'Dataset not found'),
        'INVALID_DATASET': (400, 'Invalid dataset format'),
        'CALCULATION_ERROR': (500, 'Calculation failed'),
    }

    @staticmethod
    def create(
        error_code: str,
        custom_message: str = None,
        details: Dict[str, Any] = None,
        exception: Exception = None
    ) -> Tuple[Dict[str, Any], int]:
        """
        ✅ H-2: Create standardized error response.

        Args:
            error_code: Machine-readable error code
            custom_message: Override default error message
            details: Additional error details
            exception: Exception object for logging

        Returns:
            (response_dict, http_status_code)

        Usage:
            error_dict, status_code = StandardErrorResponse.create(
                'INVALID_PARAMETER',
                custom_message='Date must be in YYYY-MM-DD format',
                details={'field': 'date', 'provided': '2024-13-01'}
            )
            return Response(error_dict, status=status_code)
        """
        from datetime import datetime

        # Get error info from registry
        if error_code not in StandardErrorResponse.ERROR_CODES:
            logger.warning(f"Unknown error code: {error_code}")
            http_status = 500
            default_message = 'Internal server error'
        else:
            http_status, default_message = StandardErrorResponse.ERROR_CODES[error_code]

        # Use custom message or default
        error_message = custom_message or default_message

        # Log exception if provided
        if exception:
            logger.error(
                f"Error {error_code}: {error_message}",
                exc_info=exception,
                extra={
                    'error_code': error_code,
                    'http_status': http_status,
                    'exception_type': type(exception).__name__,
                }
            )

        response = {
            'status': 'error',
            'error': error_message,
            'error_code': error_code,
            'timestamp': datetime.utcnow().isoformat(),
        }

        if details:
            response['details'] = details

        return response, http_status


class ErrorHandlerMiddleware:
    """
    ✅ H-2: Middleware to catch unhandled exceptions and return standardized errors.

    Wraps all responses to ensure consistency.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            error_dict, status_code = StandardErrorResponse.create(
                'VALIDATION_ERROR',
                custom_message=str(e),
                exception=e
            )
            return Response(error_dict, status=status_code)

        except Exception as e:
            logger.error(f"Unhandled exception: {e}", exc_info=True)
            error_dict, status_code = StandardErrorResponse.create(
                'INTERNAL_ERROR',
                custom_message='An unexpected error occurred',
                exception=e
            )
            return Response(error_dict, status=status_code)


def handle_serializer_errors(serializer_errors: Dict) -> Dict[str, Any]:
    """
    ✅ H-2: Convert DRF serializer errors to standard format.

    Args:
        serializer_errors: Errors from serializer.errors

    Returns:
        Standardized error response

    Usage:
        if not serializer.is_valid():
            error_response = handle_serializer_errors(serializer.errors)
            return Response(error_response, status=400)
    """
    from datetime import datetime

    # Extract first field error for main message
    first_field = next(iter(serializer_errors.keys()), 'unknown')
    first_error = serializer_errors[first_field]
    error_msg = first_error[0] if isinstance(first_error, list) else first_error

    return {
        'status': 'error',
        'error': f'Validation error in {first_field}: {error_msg}',
        'error_code': 'VALIDATION_ERROR',
        'details': {
            'field_errors': serializer_errors
        },
        'timestamp': datetime.utcnow().isoformat(),
    }


def handle_api_error(
    error_code: str,
    message: str = None,
    status_code: int = None,
    details: Dict = None,
    exception: Exception = None
) -> Response:
    """
    ✅ H-2: Convenience function to handle errors in view functions.

    Usage:
        try:
            dataset = parse_workbook(file_bytes)
        except Exception as e:
            return handle_api_error(
                'INVALID_DATASET',
                message='Failed to parse workbook',
                details={'file_size': len(file_bytes)},
                exception=e
            )
    """
    error_dict, http_status = StandardErrorResponse.create(
        error_code,
        custom_message=message,
        details=details,
        exception=exception
    )

    if status_code:
        http_status = status_code

    return Response(error_dict, status=http_status)
