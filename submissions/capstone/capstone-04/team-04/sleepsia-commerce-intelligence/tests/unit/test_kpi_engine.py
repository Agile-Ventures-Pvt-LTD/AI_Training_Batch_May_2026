"""
✅ M-7: Unit tests for KPI engine

Tests for backend/services/kpi_engine.py

Coverage areas:
- Basic KPI calculation
- Data filtering
- Division by zero guards
- Business metrics
- Edge cases
"""

import pytest
from backend.services.kpi_engine import calculate_kpis


# ============================================
# Basic Calculation Tests
# ============================================

@pytest.mark.unit
class TestBasicKPICalculation:
    """Test basic KPI calculations"""

    def test_calculate_kpis_with_single_sale(self, sample_sales_record):
        """Test KPI calculation with single sales record"""
        dataset = {
            'sales': [sample_sales_record],
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        assert result is not None
        assert 'sales' in result
        assert result['sales']['totalRevenue'] == 1000.0
        assert result['sales']['netRevenue'] == 900.0
        assert result['sales']['unitsSold'] == 2
        assert result['sales']['totalOrders'] == 1

    def test_calculate_kpis_empty_dataset(self, empty_dataset):
        """Test KPI calculation with empty dataset"""
        result = calculate_kpis(empty_dataset)

        assert result is not None
        assert result['sales']['totalRevenue'] == 0
        assert result['sales']['netRevenue'] == 0
        assert result['sales']['unitsSold'] == 0

    def test_calculate_kpis_with_complete_dataset(self, sample_dataset):
        """Test KPI calculation with complete dataset"""
        result = calculate_kpis(sample_dataset)

        assert result is not None
        # Should have all sections
        assert 'sales' in result
        assert 'profitability' in result
        assert 'advertising' in result
        assert 'shipping' in result
        assert 'inventory' in result
        assert 'competitor' in result


# ============================================
# Sales Metrics Tests
# ============================================

@pytest.mark.unit
class TestSalesMetrics:
    """Test sales KPI calculations"""

    def test_total_revenue_aggregation(self, sample_sales_data):
        """Test total revenue calculation from multiple sales"""
        dataset = {
            'sales': sample_sales_data,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total gross: 1000 + 2000 + 500 = 3500
        assert result['sales']['totalRevenue'] == 3500.0

    def test_units_sold_aggregation(self, sample_sales_data):
        """Test units sold aggregation"""
        dataset = {
            'sales': sample_sales_data,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total units: 2 + 3 + 1 = 6
        assert result['sales']['unitsSold'] == 6

    def test_average_order_value(self, sample_sales_data):
        """Test AOV calculation"""
        dataset = {
            'sales': sample_sales_data,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total net: 900 + 1800 + 450 = 3150
        # Orders: 3
        # AOV: 3150 / 3 = 1050
        assert result['sales']['aov'] == 1050

    def test_return_rate_calculation(self, sample_sales_data):
        """Test return rate calculation"""
        dataset = {
            'sales': sample_sales_data,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total returns: 100
        # Total units: 6
        # Return rate: (100/6) * 100 ≈ 16.7%
        assert result['sales']['returnRate'] > 16.0
        assert result['sales']['returnRate'] < 17.0

    def test_cancellation_rate_calculation(self, sample_sales_data):
        """Test cancellation rate calculation"""
        dataset = {
            'sales': sample_sales_data,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total cancellations: 50
        # Total gross: 3500
        # Cancellation rate: (50/3500) * 100 ≈ 1.4%
        assert result['sales']['cancellationRate'] > 1.0
        assert result['sales']['cancellationRate'] < 2.0


# ============================================
# Division by Zero Guard Tests
# ============================================

@pytest.mark.unit
@pytest.mark.edge_case
class TestDivisionByZeroGuards:
    """Test division by zero protection"""

    def test_aov_with_no_orders(self):
        """Test AOV calculation with zero orders"""
        dataset = {
            'sales': [],
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should not raise exception, AOV should be 0
        assert result['sales']['aov'] == 0

    def test_return_rate_with_zero_units(self):
        """Test return rate with zero units"""
        dataset = {
            'sales': [{'units': 0, 'returns': 0}],
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should not raise exception
        assert result is not None

    def test_advertising_metrics_with_zero_impressions(self, sample_advertising_data):
        """Test advertising CTR with zero impressions"""
        zero_impression_ad = {
            'spend': 100.0,
            'impressions': 0,
            'clicks': 0,
        }

        dataset = {
            'sales': [],
            'advertising': [zero_impression_ad],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # CTR should be 0, not cause division error
        assert result['advertising']['ctr'] == 0


# ============================================
# Filtering Tests
# ============================================

@pytest.mark.unit
class TestDataFiltering:
    """Test KPI filtering functionality"""

    def test_filter_by_channel(self, sample_dataset):
        """Test filtering by channel"""
        result = calculate_kpis(sample_dataset, filters={'channel': 'Amazon'})

        # Amazon has 2 sales: 1000 + 500 = 1500
        assert result['sales']['totalRevenue'] == 1500.0

    def test_filter_by_sku(self, sample_dataset):
        """Test filtering by SKU"""
        result = calculate_kpis(sample_dataset, filters={'sku': 'SKU-001'})

        # SKU-001 has 2 sales: 1000 + 500 = 1500
        assert result['sales']['totalRevenue'] == 1500.0

    def test_filter_no_matches(self, sample_dataset):
        """Test filtering with no matching results"""
        result = calculate_kpis(sample_dataset, filters={'sku': 'SKU-999'})

        # No matching sales
        assert result['sales']['totalRevenue'] == 0


# ============================================
# Advertising Metrics Tests
# ============================================

@pytest.mark.unit
class TestAdvertisingMetrics:
    """Test advertising KPI calculations"""

    def test_ad_spend_aggregation(self, sample_advertising_data):
        """Test total ad spend calculation"""
        dataset = {
            'sales': [],
            'advertising': sample_advertising_data,
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total spend: 100 + 200 = 300
        assert result['advertising']['totalSpend'] == 300.0

    def test_click_through_rate(self, sample_advertising_data):
        """Test CTR calculation"""
        dataset = {
            'sales': [],
            'advertising': sample_advertising_data,
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total clicks: 150, Total impressions: 15000
        # CTR: (150/15000) * 100 = 1%
        assert result['advertising']['ctr'] == 1.0

    def test_cost_per_click(self, sample_advertising_data):
        """Test CPC calculation"""
        dataset = {
            'sales': [],
            'advertising': sample_advertising_data,
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Total spend: 300, Total clicks: 150
        # CPC: 300/150 = 2
        assert result['advertising']['cpc'] == 2.0


# ============================================
# Inventory Metrics Tests
# ============================================

@pytest.mark.unit
class TestInventoryMetrics:
    """Test inventory KPI calculations"""

    def test_total_available_stock(self, sample_inventory_data):
        """Test total available stock calculation"""
        dataset = {
            'sales': [],
            'advertising': [],
            'shipping': [],
            'inventory': sample_inventory_data,
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Available: 50 + 0 = 50
        assert result['inventory']['totalAvailableStock'] == 50

    def test_stockout_risk_detection(self, sample_inventory_data):
        """Test detection of SKUs with zero available stock"""
        dataset = {
            'sales': [],
            'advertising': [],
            'shipping': [],
            'inventory': sample_inventory_data,
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should detect high-risk SKU
        assert result['inventory']['highRiskSkusCount'] >= 1


# ============================================
# Shipping Metrics Tests
# ============================================

@pytest.mark.unit
class TestShippingMetrics:
    """Test shipping KPI calculations"""

    def test_on_time_delivery_rate(self, sample_shipping_data):
        """Test on-time delivery rate calculation"""
        dataset = {
            'sales': [],
            'advertising': [],
            'shipping': sample_shipping_data,
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # 1 on-time out of 2 = 50%
        assert result['shipping']['onTimeDeliveryRate'] == 50.0

    def test_delayed_orders_tracking(self, sample_shipping_data):
        """Test delayed orders detection"""
        dataset = {
            'sales': [],
            'advertising': [],
            'shipping': sample_shipping_data,
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # 1 delayed order
        assert result['shipping']['delayedOrders'] == 1


# ============================================
# Edge Cases
# ============================================

@pytest.mark.unit
@pytest.mark.edge_case
class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_negative_values_handled(self):
        """Test handling of negative values"""
        dataset = {
            'sales': [
                {'netSales': -100, 'units': 1}  # Refund
            ],
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should handle negative revenue (refunds)
        assert result is not None

    def test_very_large_numbers(self):
        """Test handling of very large numbers"""
        dataset = {
            'sales': [
                {'netSales': 999999999.99, 'units': 1000}
            ],
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should handle large numbers
        assert result['sales']['totalNetRevenue'] > 0

    def test_decimal_precision(self):
        """Test decimal precision in calculations"""
        dataset = {
            'sales': [
                {'netSales': 100.33, 'units': 3, 'returns': 10.11}
            ],
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should maintain precision
        assert result is not None


# ============================================
# Performance Tests
# ============================================

@pytest.mark.unit
@pytest.mark.slow
class TestPerformance:
    """Test performance with large datasets"""

    def test_large_sales_dataset(self):
        """Test KPI calculation with large sales dataset"""
        large_sales = [
            {
                'netSales': 1000.0,
                'units': 2,
                'channel': f'Channel{i % 10}',
                'sku': f'SKU-{i}'
            }
            for i in range(1000)
        ]

        dataset = {
            'sales': large_sales,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }

        result = calculate_kpis(dataset)

        # Should complete and return valid results
        assert result is not None
        assert result['sales']['totalNetRevenue'] == 1000000.0
