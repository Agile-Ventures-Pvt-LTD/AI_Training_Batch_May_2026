"""
✅ M-6: Centralized configuration loader with validation

This module provides a single point for loading and validating configuration
from environment variables with sensible defaults and type conversion.

All hardcoded values should be loaded through this module to enable
environment-specific configuration without code changes.

Example:
    from backend.config.settings_loader import ConfigLoader

    MAX_RETRIES = ConfigLoader.get_int('DB_MAX_RETRIES', 5)
    TIMEOUT = ConfigLoader.get_int('API_TIMEOUT_SECONDS', 60)
    DEBUG = ConfigLoader.get_bool('DEBUG_MODE', False)
    MODELS = ConfigLoader.get_list('MODEL_CASCADE', ['model1', 'model2'])
"""

import os
import logging
from typing import Any, List, Optional

logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Centralized configuration loader with type conversion and validation.

    Provides methods to load configuration from environment variables
    with sensible defaults and automatic type conversion.

    Features:
    - Type-safe configuration loading
    - Sensible defaults for all values
    - Logging of configuration changes
    - Validation of critical values
    """

    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        """
        Get string configuration value.

        Args:
            key: Environment variable name
            default: Default value if not set

        Returns:
            Configuration value or default

        Example:
            >>> model = ConfigLoader.get_str('GEMINI_MODEL', 'gemini-2.5-flash')
        """
        value = os.getenv(key, default)
        if value != default and os.getenv(key):
            logger.debug(f"Loaded config: {key}={value[:20]}...")
        return value

    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        """
        Get integer configuration value.

        Args:
            key: Environment variable name
            default: Default value if not set

        Returns:
            Configuration value as integer or default

        Raises:
            ValueError: If value cannot be converted to int

        Example:
            >>> max_retries = ConfigLoader.get_int('DB_MAX_RETRIES', 5)
        """
        value = os.getenv(key)
        if value is None:
            return default

        try:
            result = int(value)
            logger.debug(f"Loaded config: {key}={result}")
            return result
        except ValueError:
            logger.error(f"Invalid integer config {key}={value}, using default {default}")
            return default

    @staticmethod
    def get_float(key: str, default: float = 0.0) -> float:
        """
        Get float configuration value.

        Args:
            key: Environment variable name
            default: Default value if not set

        Returns:
            Configuration value as float or default

        Raises:
            ValueError: If value cannot be converted to float

        Example:
            >>> multiplier = ConfigLoader.get_float('ROI_MULTIPLIER', 0.7)
        """
        value = os.getenv(key)
        if value is None:
            return default

        try:
            result = float(value)
            logger.debug(f"Loaded config: {key}={result}")
            return result
        except ValueError:
            logger.error(f"Invalid float config {key}={value}, using default {default}")
            return default

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """
        Get boolean configuration value.

        Recognizes: true, false, yes, no, 1, 0, on, off (case-insensitive)

        Args:
            key: Environment variable name
            default: Default value if not set

        Returns:
            Configuration value as boolean or default

        Example:
            >>> debug = ConfigLoader.get_bool('DEBUG_MODE', False)
            >>> enable_gemini = ConfigLoader.get_bool('ENABLE_GEMINI', True)
        """
        value = os.getenv(key)
        if value is None:
            return default

        value_lower = value.lower().strip()

        if value_lower in ('true', '1', 'yes', 'on', 'enabled'):
            logger.debug(f"Loaded config: {key}=True")
            return True
        elif value_lower in ('false', '0', 'no', 'off', 'disabled'):
            logger.debug(f"Loaded config: {key}=False")
            return False
        else:
            logger.warning(f"Invalid boolean config {key}={value}, using default {default}")
            return default

    @staticmethod
    def get_list(key: str, default: Optional[List[str]] = None) -> List[str]:
        """
        Get comma-separated list configuration value.

        Splits on commas and strips whitespace from each element.

        Args:
            key: Environment variable name
            default: Default list if not set

        Returns:
            Configuration value as list or default

        Example:
            >>> models = ConfigLoader.get_list(
            ...     'GEMINI_MODELS',
            ...     ['model1', 'model2', 'model3']
            ... )
        """
        if default is None:
            default = []

        value = os.getenv(key)
        if value is None:
            return default

        try:
            result = [v.strip() for v in value.split(',') if v.strip()]
            logger.debug(f"Loaded config: {key}={result}")
            return result if result else default
        except Exception as e:
            logger.error(f"Error parsing list config {key}={value}: {e}")
            return default

    @staticmethod
    def get_required(key: str) -> str:
        """
        Get required configuration value that must be set.

        Args:
            key: Environment variable name

        Returns:
            Configuration value

        Raises:
            ValueError: If key is not set

        Example:
            >>> api_key = ConfigLoader.get_required('GEMINI_API_KEY')
        """
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required configuration '{key}' not set")

        logger.debug(f"Loaded config: {key}=<set>")
        return value

    @staticmethod
    def validate_int_range(key: str, default: int, min_val: int, max_val: int) -> int:
        """
        Get and validate integer is within range.

        Args:
            key: Environment variable name
            default: Default value if not set
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Configuration value if valid, otherwise default

        Example:
            >>> workers = ConfigLoader.validate_int_range(
            ...     'WORKER_THREADS', 4, 1, 32
            ... )
        """
        value = ConfigLoader.get_int(key, default)

        if not (min_val <= value <= max_val):
            logger.warning(
                f"Config {key}={value} outside range [{min_val}, {max_val}], "
                f"using default {default}"
            )
            return default

        return value

    @staticmethod
    def validate_float_range(
        key: str, default: float, min_val: float, max_val: float
    ) -> float:
        """
        Get and validate float is within range.

        Args:
            key: Environment variable name
            default: Default value if not set
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Configuration value if valid, otherwise default

        Example:
            >>> margin = ConfigLoader.validate_float_range(
            ...     'PROFIT_MARGIN', 0.2, 0.0, 1.0
            ... )
        """
        value = ConfigLoader.get_float(key, default)

        if not (min_val <= value <= max_val):
            logger.warning(
                f"Config {key}={value} outside range [{min_val}, {max_val}], "
                f"using default {default}"
            )
            return default

        return value

    @staticmethod
    def print_loaded_config():
        """
        Print all loaded configuration for debugging.

        Useful for verifying configuration in logs during startup.
        Hides sensitive values like API keys.

        Example:
            >>> ConfigLoader.print_loaded_config()
        """
        logger.info("=" * 50)
        logger.info("Loaded Configuration:")
        logger.info("=" * 50)

        # List of all known config keys
        config_keys = [
            'ENVIRONMENT', 'DEBUG', 'LOG_LEVEL',
            'DB_MAX_RETRIES', 'DB_INITIAL_DELAY_MS', 'DB_MAX_DELAY_MS',
            'MAX_UPLOAD_SIZE_BYTES',
            'GEMINI_MODEL', 'GEMINI_API_TIMEOUT_SECONDS',
            'CACHE_TTL_SECONDS', 'SESSION_TIMEOUT_SECONDS',
            'ENABLE_GEMINI', 'ENABLE_FALLBACK',
        ]

        for key in config_keys:
            value = os.getenv(key)
            if value:
                # Hide sensitive values
                if any(x in key for x in ['KEY', 'SECRET', 'PASSWORD']):
                    display_value = '<set>'
                else:
                    display_value = value
                logger.info(f"  {key}={display_value}")

        logger.info("=" * 50)


# ✅ M-6: Configuration constants using ConfigLoader
# These are now externalized and can be changed via environment variables

# Database Configuration
DB_MAX_RETRIES = ConfigLoader.get_int('DB_MAX_RETRIES', 5)
DB_INITIAL_DELAY_MS = ConfigLoader.get_int('DB_INITIAL_DELAY_MS', 1000)
DB_MAX_DELAY_MS = ConfigLoader.get_int('DB_MAX_DELAY_MS', 30000)
DB_BACKOFF_FACTOR = ConfigLoader.get_float('DB_BACKOFF_FACTOR', 2.0)

# File Upload Configuration
MAX_UPLOAD_SIZE_BYTES = ConfigLoader.get_int('MAX_UPLOAD_SIZE_BYTES', 104857600)  # 100MB
ALLOWED_FILE_TYPES = ConfigLoader.get_list('ALLOWED_FILE_TYPES', ['xlsx', 'xls', 'xlsm'])

# Gemini API Configuration
GEMINI_MODEL = ConfigLoader.get_str('GEMINI_MODEL', 'gemini-2.5-flash')
GEMINI_MODELS = ConfigLoader.get_list(
    'GEMINI_MODELS',
    ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
)
GEMINI_API_TIMEOUT_SECONDS = ConfigLoader.get_int('GEMINI_API_TIMEOUT_SECONDS', 60)
GEMINI_MAX_TOKENS = ConfigLoader.get_int('GEMINI_MAX_TOKENS', 1024)

# Cache & Session Configuration
CACHE_TTL_SECONDS = ConfigLoader.get_int('CACHE_TTL_SECONDS', 3600)  # 1 hour
SESSION_TIMEOUT_SECONDS = ConfigLoader.get_int('SESSION_TIMEOUT_SECONDS', 86400)  # 1 day
TOKEN_EXPIRY_BUFFER_SECONDS = ConfigLoader.get_int('TOKEN_EXPIRY_BUFFER_SECONDS', 300)  # 5 min

# Feature Flags
ENABLE_GEMINI = ConfigLoader.get_bool('ENABLE_GEMINI', True)
ENABLE_FALLBACK = ConfigLoader.get_bool('ENABLE_FALLBACK', True)
ENABLE_CACHING = ConfigLoader.get_bool('ENABLE_CACHING', True)
DEBUG_MODE = ConfigLoader.get_bool('DEBUG_MODE', False)

# Logging Configuration
LOG_LEVEL = ConfigLoader.get_str('LOG_LEVEL', 'INFO')
CORRELATION_ID_ENABLED = ConfigLoader.get_bool('CORRELATION_ID_ENABLED', True)
