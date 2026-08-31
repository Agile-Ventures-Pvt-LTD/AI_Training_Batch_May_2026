"""
M-7 Phase 2: Unit tests for KPI configuration

Tests for backend/config/kpi_config.py

Coverage areas:
- Commission rates
- ROI thresholds
- Profitability margins
- Conversion metrics
"""

import pytest
from backend.config.kpi_config import (
    CommissionRates,
    ROIThresholds,
    ProfitabilityMargins,
    ConversionMetrics
)


@pytest.mark.unit
class TestCommissionRates:
    """Test commission rate configurations"""

    def test_standard_commission_rate_exists(self):
        """Test standard commission rate is defined"""
        assert hasattr(CommissionRates, 'STANDARD')
        assert CommissionRates.STANDARD > 0
        assert CommissionRates.STANDARD < 1

    def test_premium_commission_rate_exists(self):
        """Test premium commission rate is defined"""
        assert hasattr(CommissionRates, 'PREMIUM')
        assert CommissionRates.PREMIUM > CommissionRates.STANDARD

    def test_enterprise_commission_rate_exists(self):
        """Test enterprise commission rate is defined"""
        assert hasattr(CommissionRates, 'ENTERPRISE')
        assert CommissionRates.ENTERPRISE > CommissionRates.PREMIUM

    def test_commission_rates_ordered(self):
        """Test commission rates are properly ordered"""
        assert CommissionRates.STANDARD < CommissionRates.PREMIUM < CommissionRates.ENTERPRISE

    def test_all_commission_rates_valid_percentages(self):
        """Test all rates are valid percentages (0-1)"""
        for attr in ['STANDARD', 'PREMIUM', 'ENTERPRISE']:
            rate = getattr(CommissionRates, attr)
            assert 0 < rate < 1

    def test_commission_rate_values_reasonable(self):
        """Test commission rates are reasonable business values"""
        assert CommissionRates.STANDARD >= 0.05  # At least 5%
        assert CommissionRates.ENTERPRISE <= 0.30  # At most 30%


@pytest.mark.unit
class TestROIThresholds:
    """Test ROI threshold configurations"""

    def test_investment_multiplier_exists(self):
        """Test ROI investment multiplier is defined"""
        assert hasattr(ROIThresholds, 'INVESTMENT_MULTIPLIER')
        assert ROIThresholds.INVESTMENT_MULTIPLIER > 0

    def test_min_profit_exists(self):
        """Test minimum profit threshold is defined"""
        assert hasattr(ROIThresholds, 'MIN_PROFIT')
        assert ROIThresholds.MIN_PROFIT >= 0

    def test_max_ratio_exists(self):
        """Test maximum ROI ratio is defined"""
        assert hasattr(ROIThresholds, 'MAX_RATIO')
        assert ROIThresholds.MAX_RATIO > 0

    def test_roi_thresholds_consistency(self):
        """Test ROI thresholds are consistent"""
        # MAX_RATIO should be greater than INVESTMENT_MULTIPLIER
        assert ROIThresholds.MAX_RATIO >= ROIThresholds.INVESTMENT_MULTIPLIER

    def test_investment_multiplier_reasonable(self):
        """Test investment multiplier is reasonable"""
        assert 1.0 <= ROIThresholds.INVESTMENT_MULTIPLIER <= 5.0

    def test_min_profit_reasonable(self):
        """Test minimum profit is reasonable"""
        assert ROIThresholds.MIN_PROFIT >= 0
        assert ROIThresholds.MIN_PROFIT <= 10000


@pytest.mark.unit
class TestProfitabilityMargins:
    """Test profitability margin configurations"""

    def test_good_margin_exists(self):
        """Test good profitability margin is defined"""
        assert hasattr(ProfitabilityMargins, 'GOOD')
        assert ProfitabilityMargins.GOOD > 0

    def test_excellent_margin_exists(self):
        """Test excellent profitability margin is defined"""
        assert hasattr(ProfitabilityMargins, 'EXCELLENT')
        assert ProfitabilityMargins.EXCELLENT > ProfitabilityMargins.GOOD

    def test_critical_margin_exists(self):
        """Test critical profitability margin is defined"""
        assert hasattr(ProfitabilityMargins, 'CRITICAL')
        assert ProfitabilityMargins.CRITICAL > 0

    def test_profitability_margins_ordered(self):
        """Test profitability margins are properly ordered"""
        assert (ProfitabilityMargins.CRITICAL <
                ProfitabilityMargins.GOOD <
                ProfitabilityMargins.EXCELLENT)

    def test_all_margins_valid_percentages(self):
        """Test all margins are valid percentages"""
        for attr in ['GOOD', 'EXCELLENT', 'CRITICAL']:
            margin = getattr(ProfitabilityMargins, attr)
            assert 0 < margin < 1

    def test_profitability_margins_reasonable(self):
        """Test profitability margins are reasonable business values"""
        assert ProfitabilityMargins.CRITICAL >= 0.05  # At least 5%
        assert ProfitabilityMargins.EXCELLENT <= 0.50  # At most 50%


@pytest.mark.unit
class TestConversionMetrics:
    """Test conversion metrics configurations"""

    def test_conversion_rate_target_exists(self):
        """Test conversion rate target is defined"""
        assert hasattr(ConversionMetrics, 'RATE_TARGET')
        assert ConversionMetrics.RATE_TARGET > 0

    def test_aov_multiplier_exists(self):
        """Test AOV multiplier is defined"""
        assert hasattr(ConversionMetrics, 'AOV_MULTIPLIER')
        assert ConversionMetrics.AOV_MULTIPLIER > 0

    def test_conversion_rate_valid_percentage(self):
        """Test conversion rate is valid percentage"""
        assert 0 < ConversionMetrics.RATE_TARGET < 1

    def test_aov_multiplier_reasonable(self):
        """Test AOV multiplier is reasonable"""
        assert ConversionMetrics.AOV_MULTIPLIER >= 1.0
        assert ConversionMetrics.AOV_MULTIPLIER <= 10.0

    def test_conversion_rate_realistic(self):
        """Test conversion rate is realistic for e-commerce"""
        # Typical e-commerce conversion is 1-5%
        assert ConversionMetrics.RATE_TARGET >= 0.01
        assert ConversionMetrics.RATE_TARGET <= 0.10


@pytest.mark.unit
class TestAllConfigValuesConsistent:
    """Test consistency across all config values"""

    def test_no_config_value_is_zero(self):
        """Test no critical config value is zero"""
        assert CommissionRates.STANDARD > 0
        assert ROIThresholds.INVESTMENT_MULTIPLIER > 0
        assert ProfitabilityMargins.GOOD > 0
        assert ConversionMetrics.RATE_TARGET > 0

    def test_no_config_value_is_negative(self):
        """Test no config value is negative"""
        assert CommissionRates.STANDARD > 0
        assert CommissionRates.PREMIUM > 0
        assert CommissionRates.ENTERPRISE > 0
        assert ROIThresholds.MIN_PROFIT >= 0
        assert ProfitabilityMargins.GOOD > 0
        assert ProfitabilityMargins.EXCELLENT > 0
        assert ProfitabilityMargins.CRITICAL > 0

    def test_config_matches_business_logic(self):
        """Test config values support business logic"""
        # Standard commission should be less than premium
        assert CommissionRates.STANDARD < CommissionRates.PREMIUM

        # Good margin should be less than excellent
        assert ProfitabilityMargins.GOOD < ProfitabilityMargins.EXCELLENT

        # ROI max should be greater than minimum threshold
        assert ROIThresholds.MAX_RATIO > ROIThresholds.INVESTMENT_MULTIPLIER
