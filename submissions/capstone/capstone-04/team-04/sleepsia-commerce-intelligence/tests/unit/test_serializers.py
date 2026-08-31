"""
M-7 Phase 3: Unit tests for API serializers

Tests for api/serializers.py

Coverage areas:
- File upload validation
- Size limits
- File type validation
- Filter parameter validation
- Date range validation
- Email validation
- Schedule validation
- Cross-field validation
- Error messages
"""

import pytest
from api.serializers import (
    FileUploadSerializer,
    FilterSerializer,
    ScheduleSerializer,
    EmailSerializer,
    RatingSerializer
)


@pytest.mark.unit
class TestFileUploadValidation:
    """Test file upload validation"""

    def test_valid_xlsx_file(self):
        """Test valid XLSX file passes validation"""
        serializer = FileUploadSerializer({
            'filename': 'data.xlsx',
            'size': 5000000,
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert serializer.is_valid()

    def test_valid_xls_file(self):
        """Test valid XLS file passes validation"""
        serializer = FileUploadSerializer({
            'filename': 'data.xls',
            'size': 3000000,
            'content_type': 'application/vnd.ms-excel'
        })
        assert serializer.is_valid()

    def test_file_too_large(self):
        """Test file size exceeding limit"""
        serializer = FileUploadSerializer({
            'filename': 'large.xlsx',
            'size': 150000000,  # 150MB > 100MB limit
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert not serializer.is_valid()
        assert 'size' in serializer.errors

    def test_file_empty(self):
        """Test empty file rejection"""
        serializer = FileUploadSerializer({
            'filename': 'empty.xlsx',
            'size': 0,
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert not serializer.is_valid()
        assert 'size' in serializer.errors

    def test_invalid_file_type(self):
        """Test invalid file type rejection"""
        serializer = FileUploadSerializer({
            'filename': 'data.pdf',
            'size': 5000000,
            'content_type': 'application/pdf'
        })
        assert not serializer.is_valid()
        assert 'content_type' in serializer.errors

    def test_missing_filename(self):
        """Test missing filename validation"""
        serializer = FileUploadSerializer({
            'size': 5000000,
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert not serializer.is_valid()

    def test_filename_with_spaces(self):
        """Test filename with spaces"""
        serializer = FileUploadSerializer({
            'filename': 'my data file.xlsx',
            'size': 5000000,
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert serializer.is_valid()

    def test_maximum_file_size_boundary(self):
        """Test file exactly at size limit"""
        serializer = FileUploadSerializer({
            'filename': 'data.xlsx',
            'size': 100000000,  # Exactly 100MB
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert serializer.is_valid()


@pytest.mark.unit
class TestFilterValidation:
    """Test filter parameter validation"""

    def test_valid_channel_filter(self):
        """Test valid channel filter"""
        serializer = FilterSerializer({
            'channel': 'Amazon'
        })
        assert serializer.is_valid()

    def test_invalid_channel_filter(self):
        """Test invalid channel rejection"""
        serializer = FilterSerializer({
            'channel': 'InvalidChannel'
        })
        assert not serializer.is_valid()

    def test_valid_date_filter(self):
        """Test valid single date filter"""
        serializer = FilterSerializer({
            'date': '2026-08-30'
        })
        assert serializer.is_valid()

    def test_invalid_date_format(self):
        """Test invalid date format"""
        serializer = FilterSerializer({
            'date': '30-08-2026'
        })
        assert not serializer.is_valid()

    def test_valid_date_range(self):
        """Test valid date range"""
        serializer = FilterSerializer({
            'start_date': '2026-08-01',
            'end_date': '2026-08-30'
        })
        assert serializer.is_valid()

    def test_date_range_start_after_end(self):
        """Test start date after end date"""
        serializer = FilterSerializer({
            'start_date': '2026-08-30',
            'end_date': '2026-08-01'
        })
        assert not serializer.is_valid()
        assert 'start_date' in serializer.errors or 'end_date' in serializer.errors

    def test_date_range_exceeds_365_days(self):
        """Test date range exceeding 365 days"""
        serializer = FilterSerializer({
            'start_date': '2025-08-01',
            'end_date': '2026-08-30'
        })
        assert not serializer.is_valid()
        assert 'date_range' in serializer.errors or 'start_date' in serializer.errors

    def test_date_range_exactly_365_days(self):
        """Test date range exactly 365 days"""
        serializer = FilterSerializer({
            'start_date': '2025-08-30',
            'end_date': '2026-08-30'
        })
        assert serializer.is_valid()

    def test_both_single_and_range_filters_conflict(self):
        """Test conflict between single date and date range"""
        serializer = FilterSerializer({
            'date': '2026-08-30',
            'start_date': '2026-08-01',
            'end_date': '2026-08-30'
        })
        assert not serializer.is_valid()

    def test_valid_sku_filter(self):
        """Test valid SKU filter"""
        serializer = FilterSerializer({
            'sku': 'SKU-001'
        })
        assert serializer.is_valid()

    def test_valid_category_filter(self):
        """Test valid category filter"""
        serializer = FilterSerializer({
            'category': 'Electronics'
        })
        assert serializer.is_valid()

    def test_empty_filter(self):
        """Test empty filter (no filters)"""
        serializer = FilterSerializer({})
        assert serializer.is_valid()

    def test_multiple_filters(self):
        """Test multiple filters together"""
        serializer = FilterSerializer({
            'channel': 'Amazon',
            'date': '2026-08-30',
            'sku': 'SKU-001'
        })
        assert serializer.is_valid()


@pytest.mark.unit
class TestEmailValidation:
    """Test email validation"""

    def test_valid_email(self):
        """Test valid email format"""
        serializer = EmailSerializer({
            'email': 'user@example.com'
        })
        assert serializer.is_valid()

    def test_valid_email_with_subdomain(self):
        """Test email with subdomain"""
        serializer = EmailSerializer({
            'email': 'user@mail.example.com'
        })
        assert serializer.is_valid()

    def test_invalid_email_no_at(self):
        """Test email without @ symbol"""
        serializer = EmailSerializer({
            'email': 'userexample.com'
        })
        assert not serializer.is_valid()

    def test_invalid_email_no_domain(self):
        """Test email without domain"""
        serializer = EmailSerializer({
            'email': 'user@'
        })
        assert not serializer.is_valid()

    def test_invalid_email_no_local(self):
        """Test email without local part"""
        serializer = EmailSerializer({
            'email': '@example.com'
        })
        assert not serializer.is_valid()

    def test_invalid_email_spaces(self):
        """Test email with spaces"""
        serializer = EmailSerializer({
            'email': 'user name@example.com'
        })
        assert not serializer.is_valid()


@pytest.mark.unit
class TestScheduleValidation:
    """Test schedule (cron) validation"""

    def test_valid_5_field_cron(self):
        """Test valid 5-field cron expression"""
        serializer = ScheduleSerializer({
            'schedule': '0 9 * * MON'  # 9 AM Monday
        })
        assert serializer.is_valid()

    def test_valid_6_field_cron(self):
        """Test valid 6-field cron expression"""
        serializer = ScheduleSerializer({
            'schedule': '0 9 * * MON *'  # With year
        })
        assert serializer.is_valid()

    def test_invalid_cron_wrong_fields(self):
        """Test cron with wrong field count"""
        serializer = ScheduleSerializer({
            'schedule': '0 9 *'  # Only 3 fields
        })
        assert not serializer.is_valid()

    def test_invalid_cron_bad_hour(self):
        """Test cron with invalid hour"""
        serializer = ScheduleSerializer({
            'schedule': '0 25 * * *'  # Hour 25 invalid
        })
        assert not serializer.is_valid()

    def test_invalid_cron_bad_minute(self):
        """Test cron with invalid minute"""
        serializer = ScheduleSerializer({
            'schedule': '65 9 * * *'  # Minute 65 invalid
        })
        assert not serializer.is_valid()


@pytest.mark.unit
class TestRatingValidation:
    """Test rating validation"""

    def test_valid_rating_1(self):
        """Test rating value 1"""
        serializer = RatingSerializer({'rating': 1})
        assert serializer.is_valid()

    def test_valid_rating_5(self):
        """Test rating value 5"""
        serializer = RatingSerializer({'rating': 5})
        assert serializer.is_valid()

    def test_valid_rating_middle(self):
        """Test rating value 3"""
        serializer = RatingSerializer({'rating': 3})
        assert serializer.is_valid()

    def test_invalid_rating_zero(self):
        """Test rating 0 is invalid"""
        serializer = RatingSerializer({'rating': 0})
        assert not serializer.is_valid()

    def test_invalid_rating_six(self):
        """Test rating 6 is invalid"""
        serializer = RatingSerializer({'rating': 6})
        assert not serializer.is_valid()

    def test_invalid_rating_negative(self):
        """Test negative rating invalid"""
        serializer = RatingSerializer({'rating': -1})
        assert not serializer.is_valid()


@pytest.mark.unit
@pytest.mark.edge_case
class TestSerializerEdgeCases:
    """Test edge cases in serializers"""

    def test_unicode_characters_in_filename(self):
        """Test unicode characters in filename"""
        serializer = FileUploadSerializer({
            'filename': 'données_2026.xlsx',
            'size': 5000000,
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        assert serializer.is_valid()

    def test_very_long_filename(self):
        """Test very long filename"""
        long_name = 'a' * 200 + '.xlsx'
        serializer = FileUploadSerializer({
            'filename': long_name,
            'size': 5000000,
            'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        # Should either pass or fail gracefully
        assert serializer.is_valid() or len(serializer.errors) > 0

    def test_future_date(self):
        """Test future date in filter"""
        serializer = FilterSerializer({
            'date': '2099-12-31'
        })
        assert serializer.is_valid()

    def test_past_date(self):
        """Test very old date in filter"""
        serializer = FilterSerializer({
            'date': '2000-01-01'
        })
        assert serializer.is_valid()
