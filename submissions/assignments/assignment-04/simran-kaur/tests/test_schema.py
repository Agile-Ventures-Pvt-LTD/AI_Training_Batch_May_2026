
from src.db.schema_description import (
    extract_schema
)


def test_schema_extraction():

    schema = extract_schema()

    assert len(schema) > 0

    assert "TABLE:" in schema
    print("\nExtracted Schema:\n")
    print(schema)

# run ```pytest tests/test_schema.py``` to execute
#run ```pytest tests/test_schema.py -v -s``` to execute with verbose output and print statements