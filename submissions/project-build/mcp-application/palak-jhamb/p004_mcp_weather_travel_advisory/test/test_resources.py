
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.resources import get_advisory, get_checklist,get_schema
def test_required_resources_available():
    result = get_schema()
    result1 = get_checklist()
    result2 = get_advisory()
    assert result is not None
    assert result1 is not None
    assert result2 is not None


