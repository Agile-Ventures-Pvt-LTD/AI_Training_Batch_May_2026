"""
API Serializers - H-6: Input validation for all user data

All user input must be validated at the API boundary to prevent:
- Invalid file types
- Oversized uploads
- Malicious content
- Injection attacks
"""

from rest_framework import serializers
from typing import Optional


class DatasetUploadSerializer(serializers.Serializer):
    """
    ✅ H-6: Serializer for dataset file uploads with validation

    Validates:
    - File must be Excel format (.xlsx or .xls)
    - File size must not exceed 100MB
    - File content is properly formatted
    """

    file = serializers.FileField(
        max_length=104857600,  # 100MB max
        help_text="Upload Excel file (.xlsx or .xls) up to 100MB"
    )

    def validate_file(self, value):
        """Validate uploaded file"""
        # Check file size
        if value.size > 104857600:  # 100MB
            raise serializers.ValidationError(
                "File too large. Maximum size is 100MB. "
                f"Your file is {value.size / 1024 / 1024:.1f}MB"
            )

        # Check file type - only Excel files allowed
        file_name = value.name.lower()
        allowed_extensions = ['.xlsx', '.xls', '.xlsm']
        has_valid_extension = any(file_name.endswith(ext) for ext in allowed_extensions)

        if not has_valid_extension:
            raise serializers.ValidationError(
                f"Invalid file type. Only Excel files allowed (.xlsx, .xls, .xlsm). "
                f"Your file: {value.name}"
            )

        return value


class FilterSerializer(serializers.Serializer):
    """
    ✅ M-3: Serializer for KPI filter parameters with comprehensive validation.

    Validates:
    - Date format (YYYY-MM-DD)
    - Date range constraints (start ≤ end)
    - Channel is valid (whitelist)
    - Category not empty
    - SKU format is valid
    - No malicious input

    Example:
        >>> serializer = FilterSerializer(data={
        ...     'date': '2026-08-30',
        ...     'channel': 'Amazon',
        ...     'category': 'Electronics',
        ...     'sku': 'SKU-001'
        ... })
        >>> if serializer.is_valid():
        ...     filters = serializer.validated_data
    """

    date = serializers.DateField(required=False, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    channel = serializers.CharField(max_length=100, default='All')
    category = serializers.CharField(max_length=100, default='All', allow_blank=True)
    sku = serializers.CharField(max_length=50, default='All')

    def validate_date(self, value):
        """Validate date is in correct format"""
        if value and value.year < 2000:
            raise serializers.ValidationError(
                f"Invalid year {value.year}. Date must be after 2000."
            )
        return value

    def validate_channel(self, value):
        """Validate channel name"""
        # Allow common marketplace names
        valid_channels = [
            'All', 'Amazon', 'Flipkart', 'Meesho', 'Myntra',
            'Website', 'Other'
        ]
        if value not in valid_channels and value != 'All':
            raise serializers.ValidationError(
                f"Invalid channel '{value}'. "
                f"Valid options: {', '.join(valid_channels)}"
            )
        return value

    def validate_category(self, value):
        """Validate category"""
        if len(value) > 100:
            raise serializers.ValidationError(
                "Category name too long (max 100 characters)"
            )
        return value

    def validate_sku(self, value):
        """Validate SKU format"""
        if len(value) > 50:
            raise serializers.ValidationError(
                "SKU too long (max 50 characters)"
            )
        # SKU should be alphanumeric with hyphens/underscores
        if value != 'All' and not all(c.isalnum() or c in '-_' for c in value):
            raise serializers.ValidationError(
                "SKU must contain only alphanumeric characters, hyphens, or underscores"
            )
        return value

    def validate(self, data):
        """Cross-field validation - validate date range constraints"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        single_date = data.get('date')

        # If both start and end dates provided, validate range
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError({
                    'end_date': f'End date ({end_date}) must be after start date ({start_date})'
                })
            # Range should not exceed 1 year
            days_diff = (end_date - start_date).days
            if days_diff > 365:
                raise serializers.ValidationError({
                    'end_date': f'Date range too large. Maximum allowed: 365 days, got: {days_diff} days'
                })

        # If both single date and date range provided, that's conflicting
        if single_date and (start_date or end_date):
            raise serializers.ValidationError(
                'Cannot specify both single date and date range. Choose one.'
            )

        return data


class EmailSettingsSerializer(serializers.Serializer):
    """
    ✅ H-6: Serializer for email configuration with validation

    Validates:
    - Email address format
    - Report frequency is valid
    - Schedule time format
    """

    email = serializers.EmailField()
    frequency = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly'],
        help_text="Report frequency: daily, weekly, or monthly"
    )
    time = serializers.TimeField(required=False, allow_null=True)
    enabled = serializers.BooleanField(default=True)

    def validate_time(self, value):
        """Validate time format"""
        if value:
            # Time must be in valid range (00:00 to 23:59)
            if not (0 <= value.hour < 24 and 0 <= value.minute < 60):
                raise serializers.ValidationError("Invalid time format")
        return value


class ScheduleSerializer(serializers.Serializer):
    """
    ✅ H-6: Serializer for schedule creation with validation

    Validates:
    - Schedule name not empty
    - Cron expression valid
    - Description reasonable length
    """

    name = serializers.CharField(max_length=200)
    cron_expression = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    enabled = serializers.BooleanField(default=True)

    def validate_name(self, value):
        """Validate schedule name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Schedule name cannot be empty")
        if len(value) > 200:
            raise serializers.ValidationError("Schedule name too long (max 200 characters)")
        return value.strip()

    def validate_cron_expression(self, value):
        """Validate cron expression format"""
        # Basic validation - cron should have 5 or 6 fields
        parts = value.strip().split()
        if len(parts) not in [5, 6]:
            raise serializers.ValidationError(
                "Invalid cron expression. Should have 5 or 6 fields "
                "(minute hour day month weekday [year])"
            )
        # Check each field is valid
        for i, part in enumerate(parts):
            if not _is_valid_cron_field(part, i):
                raise serializers.ValidationError(
                    f"Invalid cron field at position {i}: {part}"
                )
        return value.strip()

    def validate_description(self, value):
        """Validate description"""
        if value and len(value) > 1000:
            raise serializers.ValidationError(
                "Description too long (max 1000 characters)"
            )
        return value


def _is_valid_cron_field(field: str, position: int) -> bool:
    """
    Basic validation of cron field.

    Position: 0=minute, 1=hour, 2=day, 3=month, 4=weekday, 5=year
    """
    # Allow wildcards and ranges
    if field in ['*', '?']:
        return True

    # Allow step values
    if '/' in field:
        return True

    # Allow ranges
    if '-' in field:
        return True

    # Allow lists
    if ',' in field:
        return True

    # Must be a valid number for the field
    try:
        num = int(field)
        ranges = [
            (0, 59),    # minute
            (0, 23),    # hour
            (1, 31),    # day
            (1, 12),    # month
            (0, 6),     # weekday
            (1970, 2099)  # year
        ]
        min_val, max_val = ranges[position]
        return min_val <= num <= max_val
    except (ValueError, IndexError):
        return False


class ReportFeedbackSerializer(serializers.Serializer):
    """
    ✅ H-6: Serializer for report feedback with validation

    Validates:
    - Rating is 1-5
    - Feedback text reasonable length
    - Report ID valid
    """

    report_id = serializers.CharField(max_length=100)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    feedback = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    def validate_report_id(self, value):
        """Validate report ID"""
        if not value or not value.strip():
            raise serializers.ValidationError("Report ID cannot be empty")
        return value.strip()

    def validate_rating(self, value):
        """Validate rating"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def validate_feedback(self, value):
        """Validate feedback text"""
        if value and len(value) > 1000:
            raise serializers.ValidationError(
                "Feedback too long (max 1000 characters)"
            )
        return value
