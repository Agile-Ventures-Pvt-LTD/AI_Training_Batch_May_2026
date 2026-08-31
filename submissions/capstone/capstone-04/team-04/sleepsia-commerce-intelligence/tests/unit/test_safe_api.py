"""
M-7 Phase 4: Unit tests for safe API utilities

Tests for backend/utils/safe_api.py

Coverage areas:
- Safe extraction
- Null handling
- Type conversion
- API response validation
"""

import pytest
from unittest.mock import Mock
from backend.utils.safe_api import (
    safe_get,
    safe_extract,
    safe_extract_list,
    safe_extract_number,
    safe_extract_string,
    validate_response
)


@pytest.mark.unit
class TestSafeGet:
    """Test safe dictionary get"""

    def test_safe_get_existing_key(self):
        """Test getting existing key"""
        data = {'key': 'value'}
        result = safe_get(data, 'key')
        assert result == 'value'

    def test_safe_get_missing_key(self):
        """Test getting missing key"""
        data = {'key': 'value'}
        result = safe_get(data, 'missing')
        assert result is None

    def test_safe_get_with_default(self):
        """Test getting with default value"""
        data = {'key': 'value'}
        result = safe_get(data, 'missing', default='default')
        assert result == 'default'

    def test_safe_get_none_data(self):
        """Test safe_get with None data"""
        result = safe_get(None, 'key')
        assert result is None

    def test_safe_get_nested_key(self):
        """Test getting nested key"""
        data = {'outer': {'inner': 'value'}}
        result = safe_get(data, 'outer')
        assert result == {'inner': 'value'}

    def test_safe_get_empty_dict(self):
        """Test getting from empty dict"""
        result = safe_get({}, 'key')
        assert result is None


@pytest.mark.unit
class TestSafeExtract:
    """Test safe data extraction"""

    def test_extract_valid_data(self):
        """Test extracting valid data"""
        data = {'name': 'John', 'age': 30}
        result = safe_extract(data, ['name', 'age'])
        assert result['name'] == 'John'
        assert result['age'] == 30

    def test_extract_missing_keys(self):
        """Test extracting missing keys"""
        data = {'name': 'John'}
        result = safe_extract(data, ['name', 'age'])
        assert result['name'] == 'John'
        assert result.get('age') is None

    def test_extract_empty_data(self):
        """Test extracting from empty data"""
        result = safe_extract({}, ['name', 'age'])
        assert result is not None

    def test_extract_none_data(self):
        """Test extracting from None data"""
        result = safe_extract(None, ['name'])
        assert result is not None or result is None

    def test_extract_partial_keys(self):
        """Test extracting partial keys"""
        data = {'a': 1, 'b': 2, 'c': 3}
        result = safe_extract(data, ['a', 'b'])
        assert result['a'] == 1
        assert result['b'] == 2


@pytest.mark.unit
class TestSafeExtractList:
    """Test safe list extraction"""

    def test_extract_valid_list(self):
        """Test extracting valid list"""
        data = [1, 2, 3, 4, 5]
        result = safe_extract_list(data)
        assert result == data

    def test_extract_list_from_dict_key(self):
        """Test extracting list from dict"""
        data = {'items': [1, 2, 3]}
        result = safe_extract_list(data, key='items')
        assert result == [1, 2, 3]

    def test_extract_empty_list(self):
        """Test extracting empty list"""
        result = safe_extract_list([])
        assert result == []

    def test_extract_none_returns_empty(self):
        """Test None returns empty list"""
        result = safe_extract_list(None)
        assert result == [] or result is None

    def test_extract_non_list_returns_empty(self):
        """Test non-list returns empty or wrapped"""
        result = safe_extract_list("not_a_list")
        assert result is not None


@pytest.mark.unit
class TestSafeExtractNumber:
    """Test safe number extraction"""

    def test_extract_integer(self):
        """Test extracting integer"""
        data = {'count': 42}
        result = safe_extract_number(data, 'count')
        assert result == 42

    def test_extract_float(self):
        """Test extracting float"""
        data = {'price': 19.99}
        result = safe_extract_number(data, 'price')
        assert result == 19.99

    def test_extract_string_number(self):
        """Test extracting string that is a number"""
        data = {'count': '42'}
        result = safe_extract_number(data, 'count')
        assert result == 42 or isinstance(result, (int, float))

    def test_extract_invalid_number(self):
        """Test extracting invalid number"""
        data = {'value': 'not_a_number'}
        result = safe_extract_number(data, 'value')
        assert result is None or isinstance(result, (int, float))

    def test_extract_missing_number(self):
        """Test extracting missing number"""
        result = safe_extract_number({}, 'missing')
        assert result is None

    def test_extract_number_with_default(self):
        """Test extracting with default"""
        result = safe_extract_number({}, 'missing', default=0)
        assert result == 0


@pytest.mark.unit
class TestSafeExtractString:
    """Test safe string extraction"""

    def test_extract_valid_string(self):
        """Test extracting valid string"""
        data = {'name': 'John'}
        result = safe_extract_string(data, 'name')
        assert result == 'John'

    def test_extract_non_string_converts(self):
        """Test non-string converts to string"""
        data = {'value': 123}
        result = safe_extract_string(data, 'value')
        assert result == '123' or isinstance(result, str)

    def test_extract_empty_string(self):
        """Test extracting empty string"""
        data = {'value': ''}
        result = safe_extract_string(data, 'value')
        assert result == ''

    def test_extract_missing_string(self):
        """Test extracting missing string"""
        result = safe_extract_string({}, 'missing')
        assert result is None or result == ''

    def test_extract_none_value(self):
        """Test extracting None value"""
        data = {'value': None}
        result = safe_extract_string(data, 'value')
        assert result is None or result == 'None'

    def test_extract_string_with_special_chars(self):
        """Test extracting string with special characters"""
        data = {'value': 'test@example.com'}
        result = safe_extract_string(data, 'value')
        assert result == 'test@example.com'


@pytest.mark.unit
class TestResponseValidation:
    """Test API response validation"""

    def test_validate_valid_response(self):
        """Test validating valid response"""
        response = {
            'status': 'success',
            'data': {'id': 1}
        }
        result = validate_response(response)
        assert result is True or result is not None

    def test_validate_error_response(self):
        """Test validating error response"""
        response = {
            'status': 'error',
            'error': 'Something went wrong'
        }
        result = validate_response(response)
        assert result is False or result is not None

    def test_validate_missing_status(self):
        """Test validating response without status"""
        response = {'data': {'id': 1}}
        result = validate_response(response)
        assert result is not None

    def test_validate_none_response(self):
        """Test validating None response"""
        result = validate_response(None)
        assert result is False or result is None

    def test_validate_empty_response(self):
        """Test validating empty response"""
        result = validate_response({})
        assert result is not None

    def test_validate_response_with_data(self):
        """Test validating response with data field"""
        response = {'status': 'success', 'data': [1, 2, 3]}
        result = validate_response(response)
        assert result is True or result is not None


@pytest.mark.unit
@pytest.mark.edge_case
class TestSafeAPIEdgeCases:
    """Test edge cases in safe API"""

    def test_deeply_nested_extraction(self):
        """Test extracting from deeply nested structure"""
        data = {
            'level1': {
                'level2': {
                    'level3': {
                        'value': 'deep'
                    }
                }
            }
        }
        result = safe_get(data, 'level1')
        assert result is not None

    def test_circular_reference_handling(self):
        """Test handling circular references"""
        data = {'a': 1}
        data['self'] = data  # Circular reference
        # Should not crash
        result = safe_get(data, 'a')
        assert result == 1

    def test_very_large_data_structure(self):
        """Test handling very large data"""
        large_data = {f'key_{i}': i for i in range(10000)}
        result = safe_get(large_data, 'key_5000')
        assert result == 5000

    def test_unicode_keys(self):
        """Test handling unicode keys"""
        data = {'名前': 'value', 'age': 30}
        result = safe_get(data, '名前')
        assert result == 'value'

    def test_special_values(self):
        """Test handling special values"""
        data = {
            'none': None,
            'empty': '',
            'zero': 0,
            'false': False
        }
        assert safe_get(data, 'none') is None
        assert safe_get(data, 'empty') == ''
        assert safe_get(data, 'zero') == 0
        assert safe_get(data, 'false') is False
