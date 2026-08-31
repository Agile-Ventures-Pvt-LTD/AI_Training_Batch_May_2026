"""
M-10: Custom error definitions and messages

Improved, user-friendly error messages with:
- Clear problem descriptions
- Actionable guidance
- Context information
- Logging integration
"""

import logging


logger = logging.getLogger(__name__)


class SleepsiaException(Exception):
    """Base exception for Sleepsia Commerce Intelligence"""

    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code or "UNKNOWN_ERROR"
        self.details = details or {}
        super().__init__(self.message)
        logger.error(f"[{self.error_code}] {self.message}", extra=self.details)

    def to_dict(self):
        """Convert to response dictionary"""
        return {
            "status": "error",
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }


# ============================================
# Data Validation Errors
# ============================================

class FileUploadError(SleepsiaException):
    """File upload validation error"""
    pass


class InvalidFileType(FileUploadError):
    """Invalid file type"""

    def __init__(self, filename: str, allowed_types: list):
        message = (
            f"Invalid file type for '{filename}'. "
            f"Allowed types: {', '.join(allowed_types)}. "
            f"Please upload a valid file."
        )
        super().__init__(message, "INVALID_FILE_TYPE", {
            "filename": filename,
            "allowed_types": allowed_types
        })


class FileTooLarge(FileUploadError):
    """File exceeds size limit"""

    def __init__(self, filename: str, size_bytes: int, max_size_bytes: int):
        size_mb = size_bytes / (1024 * 1024)
        max_mb = max_size_bytes / (1024 * 1024)
        message = (
            f"File '{filename}' is {size_mb:.1f} MB. "
            f"Maximum allowed size is {max_mb:.0f} MB. "
            f"Please upload a smaller file."
        )
        super().__init__(message, "FILE_TOO_LARGE", {
            "filename": filename,
            "size_mb": size_mb,
            "max_size_mb": max_mb
        })


class FileEmpty(FileUploadError):
    """File is empty"""

    def __init__(self, filename: str):
        message = f"File '{filename}' is empty. Please upload a file with data."
        super().__init__(message, "FILE_EMPTY", {"filename": filename})


class InvalidDateRange(SleepsiaException):
    """Invalid date range"""

    def __init__(self, start_date: str, end_date: str, max_days: int = 365):
        message = (
            f"Invalid date range: {start_date} to {end_date}. "
            f"Start date must be before end date, "
            f"and range cannot exceed {max_days} days. "
            f"Please correct the dates and try again."
        )
        super().__init__(message, "INVALID_DATE_RANGE", {
            "start_date": start_date,
            "end_date": end_date,
            "max_days": max_days
        })


class MissingRequiredField(SleepsiaException):
    """Required field is missing"""

    def __init__(self, field_name: str, context: str = ""):
        message = (
            f"Required field '{field_name}' is missing. "
            f"Please provide a value for '{field_name}' and try again."
        )
        if context:
            message += f" Context: {context}"
        super().__init__(message, "MISSING_REQUIRED_FIELD", {
            "field_name": field_name,
            "context": context
        })


# ============================================
# Database Errors
# ============================================

class DatabaseError(SleepsiaException):
    """Database operation error"""
    pass


class ConnectionError(DatabaseError):
    """Database connection failed"""

    def __init__(self, attempt: int = 1, max_attempts: int = 3):
        message = (
            f"Failed to connect to database (attempt {attempt}/{max_attempts}). "
            f"Please check your database configuration and try again. "
            f"If the problem persists, contact support."
        )
        super().__init__(message, "DB_CONNECTION_ERROR", {
            "attempt": attempt,
            "max_attempts": max_attempts
        })


class QueryTimeout(DatabaseError):
    """Query execution timeout"""

    def __init__(self, query_type: str, timeout_seconds: int):
        message = (
            f"Database query '{query_type}' exceeded {timeout_seconds}s timeout. "
            f"The query is too slow or the database is unresponsive. "
            f"Try simplifying your query or contact support."
        )
        super().__init__(message, "QUERY_TIMEOUT", {
            "query_type": query_type,
            "timeout_seconds": timeout_seconds
        })


class DuplicateEntry(DatabaseError):
    """Duplicate entry in database"""

    def __init__(self, field_name: str, value: str):
        message = (
            f"A record with '{field_name}' = '{value}' already exists. "
            f"Please use a unique value or update the existing record."
        )
        super().__init__(message, "DUPLICATE_ENTRY", {
            "field_name": field_name,
            "value": value
        })


# ============================================
# API Errors
# ============================================

class APIError(SleepsiaException):
    """External API error"""
    pass


class APITimeout(APIError):
    """API request timeout"""

    def __init__(self, api_name: str, timeout_seconds: int):
        message = (
            f"Request to {api_name} timed out after {timeout_seconds}s. "
            f"The service may be experiencing issues. "
            f"Please try again later."
        )
        super().__init__(message, "API_TIMEOUT", {
            "api_name": api_name,
            "timeout_seconds": timeout_seconds
        })


class RateLimitExceeded(APIError):
    """Rate limit exceeded"""

    def __init__(self, api_name: str, reset_seconds: int = None):
        message = (
            f"Rate limit exceeded for {api_name}. "
            f"Too many requests have been made. "
        )
        if reset_seconds:
            minutes = reset_seconds // 60
            message += f"Please wait {minutes} minute(s) and try again."
        else:
            message += "Please try again in a few moments."
        super().__init__(message, "RATE_LIMIT_EXCEEDED", {
            "api_name": api_name,
            "reset_seconds": reset_seconds
        })


class InvalidAPIKey(APIError):
    """Invalid API key"""

    def __init__(self, api_name: str):
        message = (
            f"Invalid or missing API key for {api_name}. "
            f"Please verify your API key configuration and try again."
        )
        super().__init__(message, "INVALID_API_KEY", {"api_name": api_name})


class APIUnauthorized(APIError):
    """API authorization failed"""

    def __init__(self, api_name: str, resource: str = ""):
        message = (
            f"Not authorized to access {api_name}"
        )
        if resource:
            message += f" resource '{resource}'"
        message += ". Please check your credentials and permissions."
        super().__init__(message, "API_UNAUTHORIZED", {
            "api_name": api_name,
            "resource": resource
        })


# ============================================
# Calculation and Processing Errors
# ============================================

class CalculationError(SleepsiaException):
    """Calculation or processing error"""
    pass


class InvalidInput(CalculationError):
    """Invalid input for calculation"""

    def __init__(self, operation: str, reason: str):
        message = (
            f"Cannot perform '{operation}': {reason}. "
            f"Please check your input data and try again."
        )
        super().__init__(message, "INVALID_INPUT", {
            "operation": operation,
            "reason": reason
        })


class NoDataError(CalculationError):
    """No data available for operation"""

    def __init__(self, data_type: str):
        message = (
            f"No {data_type} data available for analysis. "
            f"Please upload or provide {data_type} data first."
        )
        super().__init__(message, "NO_DATA", {"data_type": data_type})


class DivisionByZeroError(CalculationError):
    """Division by zero in calculation"""

    def __init__(self, metric: str):
        message = (
            f"Cannot calculate {metric} - insufficient data. "
            f"Please ensure you have enough data points for this metric."
        )
        super().__init__(message, "DIVISION_BY_ZERO", {"metric": metric})


# ============================================
# Session and Authentication Errors
# ============================================

class SessionError(SleepsiaException):
    """Session-related error"""
    pass


class SessionExpired(SessionError):
    """Session has expired"""

    def __init__(self):
        message = "Your session has expired. Please log in again."
        super().__init__(message, "SESSION_EXPIRED")


class InvalidSession(SessionError):
    """Invalid session ID"""

    def __init__(self, session_id: str):
        message = (
            f"Session '{session_id}' is invalid or has expired. "
            f"Please start a new session."
        )
        super().__init__(message, "INVALID_SESSION", {"session_id": session_id})


# ============================================
# Configuration Errors
# ============================================

class ConfigurationError(SleepsiaException):
    """Configuration-related error"""
    pass


class MissingConfigValue(ConfigurationError):
    """Required configuration value is missing"""

    def __init__(self, config_key: str):
        message = (
            f"Required configuration '{config_key}' is not set. "
            f"Please set the environment variable or configuration file value. "
            f"See documentation for setup instructions."
        )
        super().__init__(message, "MISSING_CONFIG", {"config_key": config_key})


class InvalidConfigValue(ConfigurationError):
    """Configuration value is invalid"""

    def __init__(self, config_key: str, expected: str, received: str):
        message = (
            f"Configuration '{config_key}' has invalid value. "
            f"Expected: {expected}, Got: {received}. "
            f"Please correct the configuration."
        )
        super().__init__(message, "INVALID_CONFIG", {
            "config_key": config_key,
            "expected": expected,
            "received": received
        })


# ============================================
# Generic Errors
# ============================================

class InternalServerError(SleepsiaException):
    """Internal server error"""

    def __init__(self, operation: str, error_id: str = None):
        message = (
            f"An internal error occurred during '{operation}'. "
            f"This has been logged and our team has been notified. "
            f"Please try again later or contact support."
        )
        if error_id:
            message += f" Error ID: {error_id}"
        super().__init__(message, "INTERNAL_ERROR", {
            "operation": operation,
            "error_id": error_id
        })


class NotImplementedError(SleepsiaException):
    """Feature not yet implemented"""

    def __init__(self, feature: str):
        message = (
            f"The '{feature}' feature is not yet implemented. "
            f"This feature is coming soon. "
            f"Please check back later or contact support for updates."
        )
        super().__init__(message, "NOT_IMPLEMENTED", {"feature": feature})
