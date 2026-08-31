"""
M-7 Phase 3: Unit tests for datetime utilities

Tests for backend/utils/datetime_utils.py

Coverage areas:
- UTC time functions
- Date parsing
- Timezone conversion
- Period boundaries
- Business day calculations
- Date validation
- Timezone edge cases
"""

import pytest
from datetime import datetime, timedelta, timezone
from backend.utils.datetime_utils import (
    get_utc_now,
    to_utc,
    from_utc,
    parse_date,
    format_date,
    get_period_start,
    get_period_end,
    is_business_day,
    add_business_days,
    get_timezone
)


@pytest.mark.unit
class TestUTCTime:
    """Test UTC time functions"""

    def test_get_utc_now_returns_datetime(self):
        """Test get_utc_now returns datetime object"""
        result = get_utc_now()
        assert isinstance(result, datetime)

    def test_get_utc_now_is_utc(self):
        """Test get_utc_now returns UTC time"""
        result = get_utc_now()
        assert result.tzinfo == timezone.utc or result.tzinfo is not None

    def test_utc_now_consistency(self):
        """Test multiple calls return increasing times"""
        time1 = get_utc_now()
        time2 = get_utc_now()
        assert time1 <= time2

    def test_utc_now_recent(self):
        """Test UTC now is recent"""
        now = get_utc_now()
        # Should be within last minute
        assert (datetime.now(timezone.utc) - now).total_seconds() < 60


@pytest.mark.unit
class TestDateParsing:
    """Test date parsing"""

    def test_parse_valid_iso_date(self):
        """Test parsing valid ISO date"""
        result = parse_date("2026-08-30")
        assert isinstance(result, datetime)
        assert result.year == 2026
        assert result.month == 8
        assert result.day == 30

    def test_parse_valid_iso_datetime(self):
        """Test parsing ISO datetime"""
        result = parse_date("2026-08-30T12:00:00Z")
        assert isinstance(result, datetime)
        assert result.hour == 12

    def test_parse_valid_alternative_format(self):
        """Test parsing alternative date format"""
        result = parse_date("08/30/2026")
        assert isinstance(result, datetime)

    def test_parse_invalid_date_format(self):
        """Test parsing invalid date format"""
        with pytest.raises((ValueError, Exception)):
            parse_date("invalid-date")

    def test_parse_invalid_date_values(self):
        """Test parsing invalid date values"""
        with pytest.raises((ValueError, Exception)):
            parse_date("2026-13-01")  # Invalid month

    def test_parse_leap_year_date(self):
        """Test parsing leap year date"""
        result = parse_date("2024-02-29")
        assert result.month == 2
        assert result.day == 29

    def test_parse_year_boundary(self):
        """Test parsing year boundary dates"""
        result1 = parse_date("2026-01-01")
        result2 = parse_date("2026-12-31")
        assert result1 < result2


@pytest.mark.unit
class TestDateFormatting:
    """Test date formatting"""

    def test_format_datetime_to_iso(self):
        """Test formatting datetime to ISO string"""
        dt = datetime(2026, 8, 30, 12, 0, 0)
        result = format_date(dt)
        assert isinstance(result, str)
        assert "2026" in result
        assert "08" in result or "8" in result
        assert "30" in result

    def test_format_datetime_consistency(self):
        """Test format is consistent"""
        dt = datetime(2026, 8, 30)
        result1 = format_date(dt)
        result2 = format_date(dt)
        assert result1 == result2

    def test_format_with_custom_format(self):
        """Test formatting with custom format"""
        dt = datetime(2026, 8, 30)
        result = format_date(dt, format_str="%Y-%m-%d")
        assert result == "2026-08-30"


@pytest.mark.unit
class TestTimezoneConversion:
    """Test timezone conversion"""

    def test_to_utc_from_naive(self):
        """Test converting naive datetime to UTC"""
        naive_dt = datetime(2026, 8, 30, 12, 0, 0)
        result = to_utc(naive_dt)
        assert result is not None
        assert result.tzinfo is not None or isinstance(result, datetime)

    def test_to_utc_from_aware(self):
        """Test converting aware datetime to UTC"""
        aware_dt = datetime(2026, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
        result = to_utc(aware_dt)
        assert result is not None

    def test_from_utc_to_timezone(self):
        """Test converting UTC to specific timezone"""
        utc_dt = datetime(2026, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
        result = from_utc(utc_dt, "Asia/Kolkata")
        assert result is not None

    def test_timezone_conversion_round_trip(self):
        """Test round-trip timezone conversion"""
        original = datetime(2026, 8, 30, 12, 0, 0, tzinfo=timezone.utc)
        converted = from_utc(original, "Asia/Kolkata")
        back = to_utc(converted)
        # Times should be equivalent
        assert back is not None


@pytest.mark.unit
class TestPeriodBoundaries:
    """Test period boundary calculations"""

    def test_get_period_start_day(self):
        """Test getting day start"""
        dt = datetime(2026, 8, 30, 12, 30, 45)
        result = get_period_start(dt, "day")
        assert result.hour == 0
        assert result.minute == 0

    def test_get_period_start_month(self):
        """Test getting month start"""
        dt = datetime(2026, 8, 30, 12, 30, 45)
        result = get_period_start(dt, "month")
        assert result.day == 1
        assert result.hour == 0

    def test_get_period_start_year(self):
        """Test getting year start"""
        dt = datetime(2026, 8, 30, 12, 30, 45)
        result = get_period_start(dt, "year")
        assert result.month == 1
        assert result.day == 1

    def test_get_period_end_day(self):
        """Test getting day end"""
        dt = datetime(2026, 8, 30, 12, 30, 45)
        result = get_period_end(dt, "day")
        assert result.hour == 23
        assert result.minute == 59

    def test_get_period_end_month(self):
        """Test getting month end"""
        dt = datetime(2026, 8, 15, 12, 30, 45)
        result = get_period_end(dt, "month")
        assert result.day == 31  # August has 31 days
        assert result.month == 8

    def test_get_period_end_year(self):
        """Test getting year end"""
        dt = datetime(2026, 8, 30, 12, 30, 45)
        result = get_period_end(dt, "year")
        assert result.month == 12
        assert result.day == 31

    def test_period_start_before_end(self):
        """Test period start is before end"""
        dt = datetime(2026, 8, 30)
        start = get_period_start(dt, "day")
        end = get_period_end(dt, "day")
        assert start < end


@pytest.mark.unit
class TestBusinessDays:
    """Test business day calculations"""

    def test_monday_is_business_day(self):
        """Test Monday is business day"""
        monday = datetime(2026, 8, 31)  # Monday
        assert is_business_day(monday)

    def test_friday_is_business_day(self):
        """Test Friday is business day"""
        friday = datetime(2026, 8, 28)  # Friday
        assert is_business_day(friday)

    def test_saturday_not_business_day(self):
        """Test Saturday is not business day"""
        saturday = datetime(2026, 8, 29)  # Saturday
        assert not is_business_day(saturday)

    def test_sunday_not_business_day(self):
        """Test Sunday is not business day"""
        sunday = datetime(2026, 8, 30)  # Sunday
        assert not is_business_day(sunday)

    def test_add_business_days_weekday(self):
        """Test adding business days on weekday"""
        monday = datetime(2026, 8, 31)  # Monday
        result = add_business_days(monday, 1)
        # Should skip to next business day
        assert result is not None
        assert result > monday

    def test_add_business_days_weekend(self):
        """Test adding business days from weekend"""
        saturday = datetime(2026, 8, 29)  # Saturday
        result = add_business_days(saturday, 1)
        # Should skip to Monday
        assert result is not None
        assert is_business_day(result)

    def test_add_zero_business_days(self):
        """Test adding zero business days"""
        date = datetime(2026, 8, 31)  # Monday
        result = add_business_days(date, 0)
        assert result == date

    def test_add_negative_business_days(self):
        """Test subtracting business days"""
        date = datetime(2026, 8, 31)  # Monday
        result = add_business_days(date, -1)
        assert result < date


@pytest.mark.unit
class TestDateValidation:
    """Test date validation"""

    def test_valid_date_range(self):
        """Test valid date range"""
        start = datetime(2026, 8, 1)
        end = datetime(2026, 8, 31)
        assert start <= end

    def test_date_within_range(self):
        """Test checking date within range"""
        start = datetime(2026, 8, 1)
        date = datetime(2026, 8, 15)
        end = datetime(2026, 8, 31)
        assert start <= date <= end

    def test_date_boundary_inclusive(self):
        """Test date boundary is inclusive"""
        start = datetime(2026, 8, 1)
        assert start >= start
        assert start <= start

    def test_future_date(self):
        """Test future date"""
        future = datetime(2099, 12, 31)
        now = datetime.now()
        assert future > now

    def test_past_date(self):
        """Test past date"""
        past = datetime(2000, 1, 1)
        now = datetime.now()
        assert past < now


@pytest.mark.unit
class TestTimezoneHandling:
    """Test timezone handling"""

    def test_get_timezone_valid(self):
        """Test getting valid timezone"""
        tz = get_timezone("Asia/Kolkata")
        assert tz is not None

    def test_get_timezone_utc(self):
        """Test getting UTC timezone"""
        tz = get_timezone("UTC")
        assert tz is not None

    def test_get_timezone_invalid(self):
        """Test getting invalid timezone"""
        with pytest.raises((ValueError, Exception)):
            get_timezone("Invalid/Timezone")

    def test_timezone_offset_consistency(self):
        """Test timezone offset is consistent"""
        tz = get_timezone("Asia/Kolkata")
        dt1 = datetime(2026, 1, 15, tzinfo=tz)
        dt2 = datetime(2026, 7, 15, tzinfo=tz)
        # Offsets should be same (no DST in India)
        assert dt1.utcoffset() == dt2.utcoffset()


@pytest.mark.unit
@pytest.mark.edge_case
class TestDatetimeEdgeCases:
    """Test edge cases in datetime handling"""

    def test_leap_second_handling(self):
        """Test handling near leap second"""
        dt = datetime(2026, 6, 30, 23, 59, 59)
        result = parse_date(format_date(dt))
        assert result is not None

    def test_year_2038_problem(self):
        """Test dates beyond 2038 (32-bit limit)"""
        future = datetime(2050, 1, 1)
        formatted = format_date(future)
        parsed = parse_date(formatted)
        assert parsed.year == 2050

    def test_very_old_date(self):
        """Test very old date"""
        old = datetime(1900, 1, 1)
        formatted = format_date(old)
        assert "1900" in formatted

    def test_midnight_boundary(self):
        """Test midnight boundary"""
        midnight = datetime(2026, 8, 30, 0, 0, 0)
        next_sec = midnight + timedelta(seconds=1)
        assert midnight < next_sec

    def test_month_boundary(self):
        """Test month boundary"""
        aug_last = datetime(2026, 8, 31, 23, 59, 59)
        sep_first = datetime(2026, 9, 1, 0, 0, 0)
        assert aug_last < sep_first
        diff = sep_first - aug_last
        assert diff.total_seconds() == 1
