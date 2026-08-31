"""
Backend types module - H-1: Type hints and definitions

Provides type aliases and definitions for type-safe API development.
"""

from backend.types.api_types import (
    APITypes,
    DatasetType,
    KPIResultsType,
    FilterParamsType,
    AgentResultType,
    ApiResponseType,
    SuccessResponseType,
    ErrorResponseType,
    PaginatedResponseType,
    MaybeDataset,
    MaybeKPIs,
    MaybeAgent,
)

__all__ = [
    'APITypes',
    'DatasetType',
    'KPIResultsType',
    'FilterParamsType',
    'AgentResultType',
    'ApiResponseType',
    'SuccessResponseType',
    'ErrorResponseType',
    'PaginatedResponseType',
    'MaybeDataset',
    'MaybeKPIs',
    'MaybeAgent',
]
