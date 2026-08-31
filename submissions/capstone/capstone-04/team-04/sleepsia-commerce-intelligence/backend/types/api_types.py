"""
Type Hints and Definitions - H-1: Type safety across API

Defines common type aliases and type hints for better IDE support and type checking.
"""

from typing import Dict, Any, List, Optional, Tuple, Union
from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework.request import Request


# HTTP Request/Response Types
HttpRequestType = HttpRequest
DjangoJsonResponseType = JsonResponse
DRFResponseType = Response
DRFRequestType = Request

# Data Types
DatasetType = Dict[str, Any]
KPIResultsType = Dict[str, Any]
FilterParamsType = Dict[str, Any]
AgentResultType = Dict[str, Any]
ApiResponseType = Dict[str, Any]

# Common Response Types
SuccessResponseType = Dict[str, Union[bool, Dict[str, Any], str]]
ErrorResponseType = Dict[str, Union[bool, str, int]]
PaginatedResponseType = Dict[str, Union[int, str, List[Dict[str, Any]]]]

# Optional Types
MaybeDataset = Optional[DatasetType]
MaybeKPIs = Optional[KPIResultsType]
MaybeAgent = Optional[AgentResultType]


class APITypes:
    """
    ✅ H-1: Type definitions for common API patterns.

    Usage in functions:
        def process_dataset(data: APITypes.Dataset) -> APITypes.Result:
            pass
    """

    # Input types
    Dataset = DatasetType
    Filters = FilterParamsType
    Request = DRFRequestType

    # Output types
    Result = ApiResponseType
    Success = SuccessResponseType
    Error = ErrorResponseType
    KPIs = KPIResultsType
    AgentResult = AgentResultType

    # Optional versions
    OptionalDataset = MaybeDataset
    OptionalResult = Optional[ApiResponseType]
    OptionalKPIs = MaybeKPIs


# Function signature examples with type hints
"""
✅ H-1: Examples of proper type hints

# Simple function
def get_user_id(request: DRFRequestType) -> int:
    return int(request.user.id)

# Function with multiple returns
def parse_file(file_bytes: bytes) -> Tuple[bool, Optional[DatasetType], Optional[str]]:
    try:
        data = parse_workbook(file_bytes)
        return True, data, None
    except Exception as e:
        return False, None, str(e)

# Function with optional parameters
def calculate_kpis(
    data: DatasetType,
    filters: Optional[FilterParamsType] = None
) -> KPIResultsType:
    if filters is None:
        filters = {}
    return compute_kpis(data, filters)

# Function returning response
def api_endpoint(request: DRFRequestType) -> DRFResponseType:
    data = get_data()
    return Response({'data': data, 'success': True})

# Function with list return
def get_all_agents() -> List[Dict[str, Any]]:
    return [agent.to_dict() for agent in agents]

# Function with union type
def process_input(value: Union[str, int, float]) -> str:
    return str(value).upper()

# Async function with type hints
async def async_agent_execute(data: AgentResultType) -> Tuple[bool, AgentResultType]:
    try:
        result = await agent.execute(data)
        return True, result
    except Exception as e:
        return False, {}
"""
