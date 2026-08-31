"""
Backend configuration module
"""

from backend.config.kpi_config import (
    CommissionRates,
    ROIThresholds,
    ProfitabilityMargins,
    ConversionMetrics,
    InventoryThresholds,
    ShippingMetrics,
    AdvertisingMetrics,
    CompetitorMetrics,
    CustomerMetrics,
    get_commission_rate,
    log_config_change,
    get_config_history,
)

__all__ = [
    'CommissionRates',
    'ROIThresholds',
    'ProfitabilityMargins',
    'ConversionMetrics',
    'InventoryThresholds',
    'ShippingMetrics',
    'AdvertisingMetrics',
    'CompetitorMetrics',
    'CustomerMetrics',
    'get_commission_rate',
    'log_config_change',
    'get_config_history',
]
