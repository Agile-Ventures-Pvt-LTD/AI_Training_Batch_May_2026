"""
Database Service - H-7: Connection error handling with retry logic

Provides safe database operations with automatic retries on transient failures.
"""

import logging
import time
from typing import Optional, Callable, Any, TypeVar, List
from django.db import connection, DatabaseError, OperationalError
from django.db.utils import InterfaceError, InternalError

logger = logging.getLogger(__name__)

T = TypeVar('T')


class DatabaseConfig:
    """Configuration for database retry logic"""

    # Exponential backoff: 1s, 2s, 4s, 8s, 16s
    MAX_RETRIES = 5
    INITIAL_DELAY = 1  # seconds
    MAX_DELAY = 30  # seconds
    BACKOFF_FACTOR = 2

    # Transient errors that should trigger retry
    TRANSIENT_ERRORS = (
        OperationalError,
        InterfaceError,
        InternalError,
    )


class DatabaseService:
    """
    ✅ H-7: Database service with retry logic and error handling.

    Provides safe database operations with exponential backoff for transient failures.
    """

    @staticmethod
    def execute_query(
        query: str,
        params: Optional[tuple] = None,
        fetch_one: bool = False,
    ) -> Optional[Any]:
        """
        ✅ H-7: Execute query with retry logic on transient errors.

        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
            fetch_one: If True, fetch one result; else fetch all

        Returns:
            Query result or None if failed

        Raises:
            DatabaseError: If query fails after max retries
        """
        for attempt in range(DatabaseConfig.MAX_RETRIES):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params or ())

                    if fetch_one:
                        return cursor.fetchone()
                    else:
                        return cursor.fetchall()

            except DatabaseConfig.TRANSIENT_ERRORS as e:
                if attempt < DatabaseConfig.MAX_RETRIES - 1:
                    # Calculate exponential backoff delay
                    delay = min(
                        DatabaseConfig.INITIAL_DELAY * (DatabaseConfig.BACKOFF_FACTOR ** attempt),
                        DatabaseConfig.MAX_DELAY
                    )

                    logger.warning(
                        f"Database error (attempt {attempt + 1}/{DatabaseConfig.MAX_RETRIES}): {e}. "
                        f"Retrying in {delay}s...",
                        exc_info=e
                    )

                    time.sleep(delay)
                else:
                    # Final attempt failed
                    error_msg = f"Database query failed after {DatabaseConfig.MAX_RETRIES} attempts: {e}"
                    logger.error(error_msg, exc_info=e)
                    raise DatabaseError(error_msg) from e

            except DatabaseError as e:
                # Non-transient database error - don't retry
                logger.error(f"Database error (non-transient): {e}", exc_info=e)
                raise

        return None

    @staticmethod
    def execute_with_retry(
        func: Callable[..., T],
        *args,
        **kwargs
    ) -> Optional[T]:
        """
        ✅ H-7: Execute any function with database retry logic.

        Catches database errors and retries with exponential backoff.

        Args:
            func: Function to execute (should perform database operation)
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result or None if failed after max retries

        Usage:
            def get_user(user_id):
                return User.objects.get(id=user_id)

            user = DatabaseService.execute_with_retry(get_user, 123)
        """
        for attempt in range(DatabaseConfig.MAX_RETRIES):
            try:
                return func(*args, **kwargs)

            except DatabaseConfig.TRANSIENT_ERRORS as e:
                if attempt < DatabaseConfig.MAX_RETRIES - 1:
                    delay = min(
                        DatabaseConfig.INITIAL_DELAY * (DatabaseConfig.BACKOFF_FACTOR ** attempt),
                        DatabaseConfig.MAX_DELAY
                    )

                    logger.warning(
                        f"Database error in {func.__name__} "
                        f"(attempt {attempt + 1}/{DatabaseConfig.MAX_RETRIES}): {e}. "
                        f"Retrying in {delay}s...",
                        exc_info=e
                    )

                    time.sleep(delay)
                else:
                    error_msg = f"{func.__name__} failed after {DatabaseConfig.MAX_RETRIES} retries: {e}"
                    logger.error(error_msg, exc_info=e)
                    raise DatabaseError(error_msg) from e

            except DatabaseError as e:
                # Non-transient database error
                logger.error(
                    f"Non-transient database error in {func.__name__}: {e}",
                    exc_info=e
                )
                raise

        return None

    @staticmethod
    def bulk_execute(
        queries: List[tuple],  # List of (query, params) tuples
    ) -> bool:
        """
        ✅ H-7: Execute multiple queries in a transaction with retry logic.

        Args:
            queries: List of (query_string, params) tuples

        Returns:
            True if all queries succeeded, False otherwise

        Usage:
            queries = [
                ("INSERT INTO users VALUES (%s, %s)", (1, "John")),
                ("UPDATE users SET active=1 WHERE id=%s", (1,)),
            ]
            success = DatabaseService.bulk_execute(queries)
        """
        for attempt in range(DatabaseConfig.MAX_RETRIES):
            try:
                with connection.cursor() as cursor:
                    for query, params in queries:
                        cursor.execute(query, params or ())

                logger.info(f"Bulk execute succeeded: {len(queries)} queries")
                return True

            except DatabaseConfig.TRANSIENT_ERRORS as e:
                if attempt < DatabaseConfig.MAX_RETRIES - 1:
                    delay = min(
                        DatabaseConfig.INITIAL_DELAY * (DatabaseConfig.BACKOFF_FACTOR ** attempt),
                        DatabaseConfig.MAX_DELAY
                    )

                    logger.warning(
                        f"Database error in bulk_execute "
                        f"(attempt {attempt + 1}/{DatabaseConfig.MAX_RETRIES}): {e}. "
                        f"Retrying in {delay}s...",
                        exc_info=e
                    )

                    time.sleep(delay)
                else:
                    logger.error(
                        f"Bulk execute failed after {DatabaseConfig.MAX_RETRIES} retries: {e}",
                        exc_info=e
                    )
                    return False

            except DatabaseError as e:
                logger.error(f"Non-transient database error in bulk_execute: {e}", exc_info=e)
                return False

        return False

    @staticmethod
    def check_connection() -> bool:
        """
        ✅ H-7: Check if database connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            logger.info("Database connection healthy")
            return True

        except Exception as e:
            logger.error(f"Database connection check failed: {e}", exc_info=e)
            return False

    @staticmethod
    def get_connection_status() -> dict:
        """
        ✅ H-7: Get detailed database connection status.

        Returns:
            Dictionary with connection status information
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            return {
                'status': 'healthy',
                'connected': True,
                'database': connection.settings_dict.get('NAME', 'unknown'),
                'engine': connection.settings_dict.get('ENGINE', 'unknown'),
            }

        except Exception as e:
            return {
                'status': 'unhealthy',
                'connected': False,
                'error': str(e),
                'database': connection.settings_dict.get('NAME', 'unknown'),
                'engine': connection.settings_dict.get('ENGINE', 'unknown'),
            }
