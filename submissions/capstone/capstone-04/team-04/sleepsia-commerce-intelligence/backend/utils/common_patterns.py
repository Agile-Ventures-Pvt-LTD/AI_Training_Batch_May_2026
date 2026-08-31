"""
M-8: Common pattern extraction and utilities

Extracted duplicate code patterns from across the codebase
to reduce duplication and improve maintainability.
"""

from functools import wraps
import logging
import json
from typing import Any, Callable, Dict, List, Optional


logger = logging.getLogger(__name__)


# ============================================
# Pattern 1: Safe Data Extraction
# ============================================

def safe_get_nested(data: Dict, keys: List[str], default: Any = None) -> Any:
    """
    Safely extract nested dictionary values.

    Replaces pattern repeated in:
    - gemini_service.py
    - safe_api.py
    - dataset_service.py

    Usage:
        value = safe_get_nested(response, ['data', 'results', 0, 'value'])
    """
    if data is None:
        return default

    current = data
    for key in keys:
        try:
            if isinstance(current, dict):
                current = current.get(key, default)
            elif isinstance(current, (list, tuple)):
                current = current[int(key)] if isinstance(key, (int, str)) and str(key).isdigit() else default
            else:
                return default

            if current is None:
                return default
        except (KeyError, IndexError, TypeError, ValueError):
            return default

    return current


# ============================================
# Pattern 2: API Error Handling
# ============================================

def handle_api_error(func: Callable) -> Callable:
    """
    Decorator for consistent API error handling.

    Replaces pattern repeated in:
    - gemini_service.py
    - database_service.py
    - kpi_engine.py

    Usage:
        @handle_api_error
        def my_api_call():
            return client.do_something()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutError as e:
            logger.error(f"Timeout in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper


# ============================================
# Pattern 3: Retry Logic with Backoff
# ============================================

def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0
) -> Callable:
    """
    Decorator for retry logic with exponential backoff.

    Replaces pattern repeated in:
    - database_service.py
    - gemini_service.py
    - safe_api.py

    Usage:
        @retry_with_backoff(max_attempts=5)
        def unstable_operation():
            return do_something()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time

            attempt = 0
            delay = initial_delay

            while attempt < max_attempts:
                try:
                    logger.debug(f"Attempt {attempt + 1}/{max_attempts} for {func.__name__}")
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {str(e)}")
                        raise

                    delay = min(delay * backoff_factor, max_delay)
                    logger.warning(
                        f"Attempt {attempt} failed, retrying in {delay}s: {str(e)}"
                    )
                    time.sleep(delay)

            return None

        return wrapper

    return decorator


# ============================================
# Pattern 4: Input Validation
# ============================================

def validate_required_fields(required_fields: List[str]) -> Callable:
    """
    Decorator for validating required fields.

    Replaces pattern repeated in:
    - serializers.py
    - api/views.py
    - dataset_service.py

    Usage:
        @validate_required_fields(['name', 'email'])
        def create_user(data):
            return do_something(data)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = args[0] if args else kwargs.get('data', {})

            if not isinstance(data, dict):
                raise TypeError(f"Expected dict, got {type(data)}")

            missing_fields = [
                field for field in required_fields
                if field not in data or data[field] is None
            ]

            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ============================================
# Pattern 5: Response Formatting
# ============================================

def format_response(
    status: str = "success",
    include_timestamp: bool = True,
    include_correlation_id: bool = True
) -> Callable:
    """
    Decorator for consistent response formatting.

    Replaces pattern repeated in:
    - api/views.py
    - kpi_engine.py
    - gemini_service.py

    Usage:
        @format_response(status="success")
        def get_kpis():
            return {"revenue": 5000}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from datetime import datetime
            import uuid

            try:
                result = func(*args, **kwargs)

                response = {
                    "status": status,
                    "data": result
                }

                if include_timestamp:
                    response["timestamp"] = datetime.utcnow().isoformat()

                if include_correlation_id:
                    response["correlation_id"] = str(uuid.uuid4())

                return response

            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                return {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat() if include_timestamp else None
                }

        return wrapper

    return decorator


# ============================================
# Pattern 6: Logging with Context
# ============================================

def log_operation(operation_name: str, log_level: int = logging.INFO) -> Callable:
    """
    Decorator for logging operations with timing.

    Replaces pattern repeated in:
    - kpi_engine.py
    - database_service.py
    - gemini_service.py

    Usage:
        @log_operation("calculate_kpis")
        def calculate_kpis(data):
            return compute(data)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time

            start_time = time.time()
            logger.log(log_level, f"Starting {operation_name}")

            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.log(
                    log_level,
                    f"Completed {operation_name} in {duration:.2f}s"
                )
                return result

            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Failed {operation_name} after {duration:.2f}s: {str(e)}"
                )
                raise

        return wrapper

    return decorator


# ============================================
# Pattern 7: JSON Parsing with Validation
# ============================================

def safe_json_parse(data: str, default: Dict = None) -> Dict:
    """
    Safely parse JSON with fallback.

    Replaces pattern repeated in:
    - gemini_service.py
    - api/views.py
    - safe_api.py

    Usage:
        result = safe_json_parse(response_text, default={})
    """
    if default is None:
        default = {}

    if not isinstance(data, str):
        logger.warning(f"Expected string, got {type(data)}")
        return default

    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse JSON: {str(e)}")
        return default
    except Exception as e:
        logger.error(f"Unexpected error parsing JSON: {str(e)}")
        return default


# ============================================
# Pattern 8: Cache Management
# ============================================

class CacheManager:
    """
    Central cache management utility.

    Replaces pattern repeated in:
    - database_service.py
    - kpi_engine.py
    - dataset_service.py
    """

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, tuple] = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key not in self.cache:
            return None

        value, timestamp = self.cache[key]
        import time
        if time.time() - timestamp > self.ttl_seconds:
            del self.cache[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        """Set cached value"""
        import time
        self.cache[key] = (value, time.time())

    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()

    def delete(self, key: str) -> None:
        """Delete specific cache entry"""
        if key in self.cache:
            del self.cache[key]


# ============================================
# Pattern 9: Data Transformation Pipeline
# ============================================

class Pipeline:
    """
    Data transformation pipeline.

    Replaces pattern repeated in:
    - kpi_engine.py
    - dataset_service.py
    - serializers.py

    Usage:
        pipeline = Pipeline(data)
        result = (pipeline
            .filter(lambda x: x['amount'] > 0)
            .map(lambda x: x['amount'])
            .sum())
    """

    def __init__(self, data: Any):
        self.data = data

    def filter(self, predicate: Callable) -> 'Pipeline':
        """Filter data"""
        if isinstance(self.data, list):
            self.data = [item for item in self.data if predicate(item)]
        return self

    def map(self, transformer: Callable) -> 'Pipeline':
        """Transform data"""
        if isinstance(self.data, list):
            self.data = [transformer(item) for item in self.data]
        return self

    def reduce(self, reducer: Callable, initial: Any = None) -> Any:
        """Reduce data"""
        if not isinstance(self.data, list):
            return self.data

        if initial is None and self.data:
            result = self.data[0]
            for item in self.data[1:]:
                result = reducer(result, item)
        else:
            result = initial
            for item in self.data:
                result = reducer(result, item)

        return result

    def sum(self) -> float:
        """Sum numeric data"""
        return self.reduce(lambda a, b: a + b, 0)

    def result(self) -> Any:
        """Get final result"""
        return self.data


# ============================================
# Pattern 10: Error Context
# ============================================

class ErrorContext:
    """
    Context for detailed error information.

    Replaces pattern repeated in:
    - error handling throughout
    - logging throughout
    """

    def __init__(self, operation: str, context_data: Dict = None):
        self.operation = operation
        self.context_data = context_data or {}
        self.errors: List[str] = []

    def add_error(self, error: str) -> None:
        """Add error message"""
        self.errors.append(error)
        logger.error(f"{self.operation}: {error}")

    def has_errors(self) -> bool:
        """Check if there are errors"""
        return len(self.errors) > 0

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "operation": self.operation,
            "errors": self.errors,
            "context": self.context_data
        }
