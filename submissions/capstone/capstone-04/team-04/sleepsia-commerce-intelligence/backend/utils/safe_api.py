"""
Safe API Call Utilities - H-4: Null checks and graceful error handling

Provides helpers to safely call external APIs and handle missing/null responses.
"""

import logging
from typing import Optional, Dict, Any, Callable

logger = logging.getLogger(__name__)


def safe_extract(data: Optional[Dict], *keys, default=None):
    """
    ✅ H-4: Safely extract nested values from dict, handling None/missing keys.

    Usage:
        safe_extract(response, 'data', 'content', 0, 'text')
        # Returns response['data']['content'][0]['text'] or default if any key missing

    Args:
        data: Dictionary to extract from (can be None)
        *keys: Keys/indices to traverse
        default: Default value if any key missing

    Returns:
        Extracted value or default
    """
    if data is None:
        return default

    current = data
    for key in keys:
        if current is None:
            return default

        try:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, list):
                try:
                    current = current[int(key)]
                except (ValueError, IndexError):
                    return default
            else:
                return default
        except (KeyError, TypeError, AttributeError):
            return default

    return current if current is not None else default


def safe_api_call(
    func: Callable,
    *args,
    error_code: str = "API_CALL_FAILED",
    **kwargs
) -> tuple:
    """
    ✅ H-4: Execute API call safely with error handling.

    Returns:
        (success: bool, data: Any, error_message: str or None)

    Usage:
        success, data, error = safe_api_call(
            api.get_data,
            user_id=123,
            error_code="GET_USER_FAILED"
        )
        if not success:
            logger.error(error)
            return None
    """
    try:
        result = func(*args, **kwargs)

        # Validate result is not None
        if result is None:
            return False, None, f"{error_code}: API returned None"

        return True, result, None

    except Exception as e:
        error_msg = f"{error_code}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, None, error_msg


def validate_api_response(
    response: Optional[Dict],
    required_fields: list,
    response_name: str = "API Response"
) -> tuple:
    """
    ✅ H-4: Validate API response contains required fields.

    Returns:
        (is_valid: bool, missing_fields: list or None)

    Usage:
        is_valid, missing = validate_api_response(
            gemini_response,
            ['content', 'usage'],
            'Gemini API Response'
        )
        if not is_valid:
            logger.error(f"Missing fields: {missing}")
    """
    if response is None:
        return False, ["None (no response)"]

    if not isinstance(response, dict):
        return False, ["Response is not a dictionary"]

    missing = [f for f in required_fields if f not in response or response[f] is None]

    if missing:
        return False, missing

    return True, None


def safe_dict_merge(*dicts: Optional[Dict]) -> Dict:
    """
    ✅ H-4: Safely merge multiple dictionaries, ignoring None values.

    Returns:
        Merged dictionary with None values filtered out

    Usage:
        result = safe_dict_merge(
            {'a': 1},
            None,
            {'b': 2, 'c': None},
            {'d': 4}
        )
        # Returns {'a': 1, 'b': 2, 'd': 4}
    """
    result = {}
    for d in dicts:
        if d and isinstance(d, dict):
            for key, value in d.items():
                if value is not None:
                    result[key] = value
    return result


class APIResponseValidator:
    """
    ✅ H-4: Validator class for external API responses.

    Provides structured validation for common API patterns.
    """

    @staticmethod
    def validate_gemini_response(response: Optional[Dict]) -> tuple:
        """
        Validate Gemini/Claude API response format.

        Returns:
            (is_valid: bool, extracted_text: str or None, error: str or None)
        """
        if response is None:
            return False, None, "Gemini response is None"

        # Check structure
        is_valid, missing = validate_api_response(
            response,
            ['content'],
            'Gemini Response'
        )

        if not is_valid:
            return False, None, f"Missing required fields: {missing}"

        # Extract content safely
        content = safe_extract(response, 'content', default=None)

        if not content or not isinstance(content, list) or len(content) == 0:
            return False, None, "Response content is empty or not a list"

        text = safe_extract(content, 0, 'text', default=None)

        if not text:
            return False, None, "No text content in response"

        return True, text, None

    @staticmethod
    def validate_marketplace_response(response: Optional[Dict]) -> tuple:
        """
        Validate marketplace API response.

        Returns:
            (is_valid: bool, data: Dict or None, error: str or None)
        """
        if response is None:
            return False, None, "Marketplace response is None"

        # Check for common error indicators
        if response.get('error'):
            error_msg = safe_extract(response, 'error', 'message', default=response.get('error'))
            return False, None, f"Marketplace API error: {error_msg}"

        # Validate expected structure
        if response.get('status') not in ['success', 'ok', 200]:
            return False, None, f"Marketplace API status: {response.get('status')}"

        data = safe_extract(response, 'data', default=response)

        if not data:
            return False, None, "Marketplace response contains no data"

        return True, data, None

    @staticmethod
    def validate_database_query(result: Optional[Any]) -> tuple:
        """
        Validate database query result.

        Returns:
            (is_valid: bool, data: Any or None, error: str or None)
        """
        if result is None:
            return False, None, "Database query returned None"

        # Result can be list, dict, or other type
        return True, result, None


def handle_api_error(
    error: Exception,
    context: str = "API call",
    fallback_data: Any = None
) -> tuple:
    """
    ✅ H-4: Handle API errors with logging and fallback.

    Returns:
        (success: bool, data: Any, error_message: str)

    Usage:
        try:
            data = api.fetch()
        except Exception as e:
            success, fallback, error = handle_api_error(
                e,
                context="Fetch user data",
                fallback_data={}
            )
    """
    error_msg = f"{context} failed: {str(error)}"
    logger.error(error_msg, exc_info=True)

    if fallback_data is not None:
        return False, fallback_data, error_msg

    return False, None, error_msg
