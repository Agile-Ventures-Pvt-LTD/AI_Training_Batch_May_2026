"""
Date/Time Utilities - Timezone-aware date/time handling

All timestamps use UTC internally; conversion to user timezone only for display.
"""

import logging
from datetime import datetime, date, timedelta, timezone

logger = logging.getLogger(__name__)

UTC = timezone.utc


class DateTimeService:
    """Timezone-aware date/time service."""

    @staticmethod
    def now_utc() -> datetime:
        """Get current UTC time (timezone-aware)."""
        return datetime.now(UTC)

    @staticmethod
    def parse_date(date_str: str) -> date:
        """Parse date string in YYYY-MM-DD format."""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError as e:
            logger.error(f"Failed to parse date '{date_str}': {e}")
            return None

    @staticmethod
    def format_date(dt: datetime, format_str: str = '%Y-%m-%d') -> str:
        """Format datetime to string."""
        return dt.strftime(format_str)

    @staticmethod
    def get_date_range(start_str: str, end_str: str):
        """Parse and validate date range."""
        start = DateTimeService.parse_date(start_str)
        end = DateTimeService.parse_date(end_str)

        if start is None or end is None:
            return None, None

        if start > end:
            logger.error(f"Invalid date range: start ({start}) > end ({end})")
            return None, None

        return start, end

    @staticmethod
    def days_between(start: date, end: date) -> int:
        """Calculate days between two dates."""
        delta = end - start
        return delta.days

    @staticmethod
    def is_business_day(date_obj: date) -> bool:
        """Check if date is a business day (Monday-Friday)."""
        return date_obj.weekday() < 5

    @staticmethod
    def add_business_days(date_obj: date, days: int) -> date:
        """Add business days to a date."""
        current = date_obj
        direction = 1 if days > 0 else -1

        for _ in range(abs(days)):
            current += timedelta(days=direction)
            while current.weekday() >= 5:  # Skip weekends
                current += timedelta(days=direction)

        return current

    @staticmethod
    def get_period_boundaries(period_type: str, date_obj: date = None):
        """Get start and end dates for a period."""
        if date_obj is None:
            date_obj = DateTimeService.now_utc().date()

        if period_type == 'daily':
            return date_obj, date_obj

        elif period_type == 'weekly':
            start = date_obj - timedelta(days=date_obj.weekday())
            end = start + timedelta(days=6)
            return start, end

        elif period_type == 'monthly':
            start = date(date_obj.year, date_obj.month, 1)
            if date_obj.month == 12:
                end = date(date_obj.year + 1, 1, 1) - timedelta(days=1)
            else:
                end = date(date_obj.year, date_obj.month + 1, 1) - timedelta(days=1)
            return start, end

        elif period_type == 'yearly':
            start = date(date_obj.year, 1, 1)
            end = date(date_obj.year, 12, 31)
            return start, end

        return date_obj, date_obj


# Utility functions
def get_utc_now():
    """Get current UTC time."""
    return datetime.now(UTC)


def to_utc(dt: datetime):
    """Convert datetime to UTC."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def from_utc(dt: datetime, tz_name: str = 'UTC'):
    """Convert from UTC (returns same datetime, just reference)."""
    return dt


def parse_date(date_str: str):
    """Parse date string."""
    return DateTimeService.parse_date(date_str)


def format_date(dt: datetime, format_str: str = '%Y-%m-%d') -> str:
    """Format date."""
    return DateTimeService.format_date(dt, format_str)


def get_period_start(dt: datetime, period: str):
    """Get period start."""
    d = dt.date()
    start, _ = DateTimeService.get_period_boundaries(period, d)
    return datetime.combine(start, datetime.min.time()).replace(tzinfo=UTC)


def get_period_end(dt: datetime, period: str):
    """Get period end."""
    d = dt.date()
    _, end = DateTimeService.get_period_boundaries(period, d)
    return datetime.combine(end, datetime.max.time()).replace(tzinfo=UTC)


def is_business_day(date_obj: date) -> bool:
    """Check if business day."""
    return DateTimeService.is_business_day(date_obj)


def add_business_days(date_obj: date, days: int) -> date:
    """Add business days."""
    return DateTimeService.add_business_days(date_obj, days)


def get_timezone(tz_name: str):
    """Get timezone object."""
    if tz_name == 'UTC':
        return UTC
    return UTC  # Default to UTC
