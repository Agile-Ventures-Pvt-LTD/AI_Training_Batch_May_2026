"""
Backend utilities module

Phase 3 Additions:
- H-2: Standardized error responses
- H-7: Database error handling
- H-9: Timezone-aware date/time utilities
- Logging utilities for observability
"""

from backend.utils.api_responses import (
    APIResponse,
    ResponseStatus,
    create_error_response,
    create_success_response,
    create_partial_response,
)

from backend.utils.safe_api import (
    safe_extract,
    safe_api_call,
    validate_api_response,
    safe_dict_merge,
    APIResponseValidator,
    handle_api_error,
)

from backend.utils.datetime_utils import (
    DateTimeService,
)

from backend.utils.logging_utils import (
    StructuredLogger,
    get_correlation_id,
    set_correlation_id,
    log_performance,
    PerformanceMonitor,
)

__all__ = [
    # Phase 1: Response utilities
    'APIResponse',
    'ResponseStatus',
    'create_error_response',
    'create_success_response',
    'create_partial_response',

    # Phase 2: Safe API utilities
    'safe_extract',
    'safe_api_call',
    'validate_api_response',
    'safe_dict_merge',
    'APIResponseValidator',
    'handle_api_error',

    # Phase 3: Date/time utilities
    'DateTimeService',
    'get_period_boundaries',

    # Phase 3: Logging utilities
    'StructuredLogger',
    'get_correlation_id',
    'set_correlation_id',
    'log_performance',
    'PerformanceMonitor',
]
