"""
✅ M-7: Pytest configuration and shared test fixtures

Provides reusable fixtures for all test modules including:
- Sample data generators
- Mock objects
- Common test data
- Database fixtures
"""

import pytest
from datetime import datetime, timedelta


# ============================================
# Sample Data Fixtures
# ============================================

@pytest.fixture
def sample_sales_record():
    """Single sales transaction for testing"""
    return {
        'date': '2026-08-30',
        'channel': 'Amazon',
        'marketplace': 'Amazon',
        'sku': 'SKU-001',
        'grossSales': 1000.0,
        'netSales': 900.0,
        'netRealizedRevenue': 900.0,
        'units': 2,
        'unitsSold': 2,
        'returns': 0,
        'returnUnits': 0,
        'cancellations': 0,
    }


@pytest.fixture
def sample_sales_data():
    """Multiple sales records for aggregation testing"""
    return [
        {
            'date': '2026-08-30',
            'channel': 'Amazon',
            'marketplace': 'Amazon',
            'sku': 'SKU-001',
            'grossSales': 1000.0,
            'netSales': 900.0,
            'units': 2,
            'returns': 0,
            'cancellations': 0,
        },
        {
            'date': '2026-08-30',
            'channel': 'Flipkart',
            'marketplace': 'Flipkart',
            'sku': 'SKU-002',
            'grossSales': 2000.0,
            'netSales': 1800.0,
            'units': 3,
            'returns': 100.0,
            'cancellations': 0,
        },
        {
            'date': '2026-08-30',
            'channel': 'Amazon',
            'marketplace': 'Amazon',
            'sku': 'SKU-001',
            'grossSales': 500.0,
            'netSales': 450.0,
            'units': 1,
            'returns': 0,
            'cancellations': 50.0,
        },
    ]


@pytest.fixture
def sample_advertising_data():
    """Sample advertising campaign data"""
    return [
        {
            'date': '2026-08-30',
            'platform': 'Amazon',
            'marketplace': 'Amazon',
            'sku': 'SKU-001',
            'spend': 100.0,
            'impressions': 5000,
            'clicks': 50,
            'attributedRevenue': 500.0,
        },
        {
            'date': '2026-08-30',
            'platform': 'Google',
            'marketplace': 'Google',
            'sku': 'SKU-002',
            'spend': 200.0,
            'impressions': 10000,
            'clicks': 100,
            'attributedRevenue': 1000.0,
        },
    ]


@pytest.fixture
def sample_inventory_data():
    """Sample inventory records"""
    return [
        {
            'date': '2026-08-30',
            'sku': 'SKU-001',
            'available': 50,
            'reserved': 10,
            'inbound': 100,
            'damaged': 2,
        },
        {
            'date': '2026-08-30',
            'sku': 'SKU-002',
            'available': 0,  # Stockout risk
            'reserved': 5,
            'inbound': 0,
            'damaged': 0,
        },
    ]


@pytest.fixture
def sample_shipping_data():
    """Sample shipping records"""
    return [
        {
            'date': '2026-08-30',
            'sku': 'SKU-001',
            'carrier': 'FedEx',
            'status': 'delivered',
            'deliveredAt': '2026-08-28',
            'scheduledDelivery': '2026-08-28',
            'shippingCost': 50.0,
            'transitDays': 2,
            'delayedDays': 0,
        },
        {
            'date': '2026-08-30',
            'sku': 'SKU-002',
            'carrier': 'DHL',
            'status': 'delayed',
            'deliveredAt': '2026-08-31',
            'scheduledDelivery': '2026-08-29',
            'shippingCost': 75.0,
            'transitDays': 3,
            'delayedDays': 2,
        },
    ]


@pytest.fixture
def sample_product_data():
    """Sample product master data"""
    return [
        {
            'sku': 'SKU-001',
            'name': 'Product A',
            'category': 'Electronics',
            'mrp': 500.0,
            'cost': 250.0,
        },
        {
            'sku': 'SKU-002',
            'name': 'Product B',
            'category': 'Home',
            'mrp': 1000.0,
            'cost': 600.0,
        },
    ]


@pytest.fixture
def sample_competitor_data():
    """Sample competitor intelligence data"""
    return [
        {
            'date': '2026-08-30',
            'category': 'Electronics',
            'competitorBrand': 'BrandX',
            'competitorProductName': 'Product XA',
            'competitorPrice': 450.0,
            'sleepsiaTargetSku': 'SKU-001',
            'discountPercent': 10.0,
            'activePromotion': 'Summer Sale',
            'threatLevel': 'High',
        },
    ]


@pytest.fixture
def sample_metadata():
    """Sample dataset metadata"""
    return {
        'loadedAt': '2026-08-30 12:00:00',
        'totalOrders': 3,
        'dateRange': {'start': '2026-08-30', 'end': '2026-08-30'},
        'totalSkus': 2,
        'activeChannels': 3,
        'sourceFileName': 'test_data.xlsx',
    }


@pytest.fixture
def sample_dataset(
    sample_sales_data,
    sample_advertising_data,
    sample_inventory_data,
    sample_shipping_data,
    sample_product_data,
    sample_competitor_data,
    sample_metadata,
):
    """Complete sample dataset for integration testing"""
    return {
        'sales': sample_sales_data,
        'advertising': sample_advertising_data,
        'inventory': sample_inventory_data,
        'shipping': sample_shipping_data,
        'products': sample_product_data,
        'competitors': sample_competitor_data,
        'metadata': sample_metadata,
    }


@pytest.fixture
def empty_dataset():
    """Empty dataset for edge case testing"""
    return {
        'sales': [],
        'advertising': [],
        'inventory': [],
        'shipping': [],
        'products': [],
        'competitors': [],
        'metadata': {},
    }


# ============================================
# Filter Fixtures
# ============================================

@pytest.fixture
def filter_by_date():
    """Filter by single date"""
    return {'date': '2026-08-30'}


@pytest.fixture
def filter_by_channel():
    """Filter by sales channel"""
    return {'channel': 'Amazon'}


@pytest.fixture
def filter_by_sku():
    """Filter by product SKU"""
    return {'sku': 'SKU-001'}


@pytest.fixture
def filter_by_category():
    """Filter by product category"""
    return {'category': 'Electronics'}


@pytest.fixture
def filter_all():
    """No filters (default)"""
    return {}


# ============================================
# Mock Fixtures
# ============================================

@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response"""
    return {
        'content': [
            {
                'text': '{"metric": "Revenue", "value": 2700, "finding": "Strong sales"}'
            }
        ]
    }


@pytest.fixture
def mock_database_connection(monkeypatch):
    """Mock database connection"""
    from unittest.mock import MagicMock
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value.fetchall.return_value = []
    return mock_conn


# ============================================
# Configuration Fixtures
# ============================================

@pytest.fixture
def test_config():
    """Test configuration"""
    return {
        'DEBUG': True,
        'TESTING': True,
        'CACHE_TTL': 60,
        'MAX_RETRIES': 3,
    }


# ============================================
# Markers
# ============================================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "edge_case: mark test as edge case"
    )
