import pytest
from src.resources import get_resource

def test_required_resources_available():
    """All 3 required resources are exposed cleanly"""
    required_urls = [
        "resource://travel/checklist",
        "resource://travel/advisory-rules",
        "resource://weather/normalized-forecast-schema"
    ]
    for url in required_urls:
        content = get_resource(url)
        assert content is not None
