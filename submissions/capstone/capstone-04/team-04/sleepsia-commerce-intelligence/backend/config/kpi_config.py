"""
KPI Configuration Constants

All business logic values should be defined here for easy modification
and audit trail tracking. Update these values when business requirements change.
"""


class CommissionRates:
    """Commission rate percentages by marketplace/channel"""

    # Standard marketplace commission rates
    AMAZON_COMMISSION = 0.14  # 14% for Amazon India
    FLIPKART_COMMISSION = 0.15  # 15% for Flipkart
    MEESHO_COMMISSION = 0.12  # 12% for Meesho
    MYNTRA_COMMISSION = 0.10  # 10% for Myntra
    WEBSITE_COMMISSION = 0.0  # 0% for own website

    # Default fallback rate
    DEFAULT_COMMISSION = 0.14


class ROIThresholds:
    """ROI calculation thresholds and multipliers"""

    INVESTMENT_MULTIPLIER = 0.7  # Multiplier for investment calculations
    MIN_PROFIT_THRESHOLD = 1000.0  # Minimum profit in dollars
    MAX_ROI_RATIO = 1.5  # Maximum acceptable ROI ratio


class ProfitabilityMargins:
    """Profit margin calculations for SKUs and marketplaces"""

    # Commission margin for profit calculation
    SKU_COMMISSION_MARGIN = 0.15  # 15% commission margin per SKU
    MARKETPLACE_COMMISSION_MARGIN = 0.15  # 15% commission margin per marketplace

    # Minimum margins
    MIN_GROSS_MARGIN = 0.30  # 30% minimum gross margin target
    MIN_PROFIT_MARGIN = 0.10  # 10% minimum profit margin target


class ConversionMetrics:
    """Conversion rate targets and thresholds"""

    TARGET_CONVERSION_RATE = 0.08  # 8% target conversion rate
    GOOD_CONVERSION_RATE = 0.06  # 6% considered good
    POOR_CONVERSION_RATE = 0.03  # 3% considered poor


class InventoryThresholds:
    """Inventory management thresholds"""

    DAYS_OF_INVENTORY_HIGH_RISK = 7  # Critical stock level (7 days)
    DAYS_OF_INVENTORY_WARNING = 14  # Warning level (14 days)
    DAYS_OF_INVENTORY_OPTIMAL = 30  # Optimal level (30 days)

    DEFAULT_LEAD_TIME_DAYS = 7  # Default supplier lead time


class ShippingMetrics:
    """Shipping performance thresholds"""

    STANDARD_SLA_DAYS = 3  # Standard delivery SLA
    EXPECTED_TRANSIT_TIME = 2.1  # Base transit time in days
    DELAY_PENALTY_MULTIPLIER = 1.0  # Multiplier for delay calculations

    # On-time delivery targets
    ON_TIME_DELIVERY_TARGET = 0.95  # 95% on-time delivery


class AdvertisingMetrics:
    """Advertising performance benchmarks"""

    TARGET_ROAS = 3.0  # 3x Return on Ad Spend target
    TARGET_ACOS = 30.0  # 30% Ad Cost of Sale target
    TARGET_TACOS = 10.0  # 10% Total Ad Cost of Sale target
    TARGET_CTR = 0.02  # 2% Click-through rate target


class CompetitorMetrics:
    """Competitor comparison thresholds"""

    # Price positioning
    SLEEPSIA_PRICE_DISCOUNT_FACTOR = 0.7  # Sleepsia sells at 70% of MRP
    PRICE_GAP_WARNING_THRESHOLD = 0.20  # 20% price gap warning


class CustomerMetrics:
    """Customer metrics thresholds"""

    CUSTOMER_AT_RISK_DAYS = 90  # Days since last purchase to mark as at-risk
    HIGH_VALUE_MULTIPLIER = 2.0  # High-value customer is 2x average LTV


# Configuration management for tracking changes
CONFIG_CHANGE_LOG = []


def log_config_change(constant_name: str, old_value: float, new_value: float, reason: str) -> None:
    """
    Log configuration changes for audit trail.

    Args:
        constant_name: Name of the constant changed
        old_value: Previous value
        new_value: New value
        reason: Reason for change (e.g., "Business requirement update")
    """
    from datetime import datetime

    change_record = {
        'timestamp': datetime.utcnow().isoformat(),
        'constant': constant_name,
        'old_value': old_value,
        'new_value': new_value,
        'reason': reason,
    }
    CONFIG_CHANGE_LOG.append(change_record)


def get_commission_rate(marketplace: str) -> float:
    """
    Get commission rate for a specific marketplace.

    Args:
        marketplace: Marketplace name (amazon, flipkart, etc.)

    Returns:
        Commission rate as decimal (0.14 = 14%)
    """
    marketplace_lower = marketplace.lower() if marketplace else ''

    commission_map = {
        'amazon': CommissionRates.AMAZON_COMMISSION,
        'flipkart': CommissionRates.FLIPKART_COMMISSION,
        'meesho': CommissionRates.MEESHO_COMMISSION,
        'myntra': CommissionRates.MYNTRA_COMMISSION,
        'website': CommissionRates.WEBSITE_COMMISSION,
    }

    return commission_map.get(marketplace_lower, CommissionRates.DEFAULT_COMMISSION)


def get_config_history():
    """Retrieve audit trail of all configuration changes"""
    return CONFIG_CHANGE_LOG
