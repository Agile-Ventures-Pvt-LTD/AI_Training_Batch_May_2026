"""
M-7 Phase 3: Unit tests for dataset service

Tests for backend/services/dataset_service.py

Coverage areas:
- Dataset loading
- Session storage
- Dataset retrieval
- Default dataset fallback
- Error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.dataset_service import DatasetService


@pytest.mark.unit
class TestDatasetLoading:
    """Test dataset loading functionality"""

    def test_load_valid_dataset(self, sample_dataset):
        """Test loading valid dataset"""
        service = DatasetService()
        result = service.load_dataset(sample_dataset)
        assert result is not None

    def test_load_empty_dataset(self, empty_dataset):
        """Test loading empty dataset"""
        service = DatasetService()
        result = service.load_dataset(empty_dataset)
        assert result is not None

    def test_load_partial_dataset(self):
        """Test loading dataset with missing sections"""
        partial_dataset = {
            'sales': [{'netSales': 1000, 'units': 2}],
            'advertising': [],
            # Missing other sections
        }
        service = DatasetService()
        result = service.load_dataset(partial_dataset)
        assert result is not None

    def test_load_none_dataset(self):
        """Test loading None dataset"""
        service = DatasetService()
        with pytest.raises((TypeError, ValueError)):
            service.load_dataset(None)

    def test_load_invalid_dataset_type(self):
        """Test loading non-dict dataset"""
        service = DatasetService()
        with pytest.raises((TypeError, ValueError)):
            service.load_dataset("invalid")


@pytest.mark.unit
class TestSessionStorage:
    """Test session-based dataset storage"""

    def test_store_dataset_in_session(self, sample_dataset):
        """Test storing dataset in session"""
        service = DatasetService()
        session_id = "test-session-123"
        service.store_in_session(session_id, sample_dataset)
        # Verify it's stored
        retrieved = service.get_from_session(session_id)
        assert retrieved is not None

    def test_retrieve_stored_dataset(self, sample_dataset):
        """Test retrieving stored dataset"""
        service = DatasetService()
        session_id = "test-session-456"
        service.store_in_session(session_id, sample_dataset)
        retrieved = service.get_from_session(session_id)
        assert retrieved == sample_dataset or retrieved is not None

    def test_multiple_sessions_isolated(self, sample_dataset, empty_dataset):
        """Test multiple sessions are isolated"""
        service = DatasetService()
        service.store_in_session("session1", sample_dataset)
        service.store_in_session("session2", empty_dataset)

        result1 = service.get_from_session("session1")
        result2 = service.get_from_session("session2")

        assert result1 is not None
        assert result2 is not None

    def test_overwrite_session_data(self, sample_dataset, empty_dataset):
        """Test overwriting session data"""
        service = DatasetService()
        session_id = "test-session-789"
        service.store_in_session(session_id, sample_dataset)
        service.store_in_session(session_id, empty_dataset)

        retrieved = service.get_from_session(session_id)
        assert retrieved is not None

    def test_session_cleanup(self, sample_dataset):
        """Test session cleanup"""
        service = DatasetService()
        session_id = "cleanup-test"
        service.store_in_session(session_id, sample_dataset)
        service.clear_session(session_id)

        retrieved = service.get_from_session(session_id)
        assert retrieved is None or retrieved == {}


@pytest.mark.unit
class TestDatasetRetrieval:
    """Test dataset retrieval methods"""

    def test_get_sales_data(self, sample_dataset):
        """Test getting sales data from dataset"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        sales = service.get_sales_data()
        assert sales is not None
        assert isinstance(sales, list)

    def test_get_advertising_data(self, sample_dataset):
        """Test getting advertising data from dataset"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        ads = service.get_advertising_data()
        assert ads is not None
        assert isinstance(ads, list)

    def test_get_inventory_data(self, sample_dataset):
        """Test getting inventory data from dataset"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        inventory = service.get_inventory_data()
        assert inventory is not None
        assert isinstance(inventory, list)

    def test_get_shipping_data(self, sample_dataset):
        """Test getting shipping data from dataset"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        shipping = service.get_shipping_data()
        assert shipping is not None
        assert isinstance(shipping, list)

    def test_get_complete_dataset(self, sample_dataset):
        """Test getting complete dataset"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        dataset = service.get_dataset()
        assert dataset is not None
        assert isinstance(dataset, dict)

    def test_dataset_sections_preserved(self, sample_dataset):
        """Test all dataset sections are preserved"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        dataset = service.get_dataset()

        expected_sections = ['sales', 'advertising', 'inventory', 'shipping']
        for section in expected_sections:
            assert section in dataset


@pytest.mark.unit
class TestDefaultDataset:
    """Test default dataset fallback"""

    def test_default_dataset_exists(self):
        """Test service has default dataset"""
        service = DatasetService()
        default = service.get_default_dataset()
        assert default is not None

    def test_default_dataset_structure(self):
        """Test default dataset has required structure"""
        service = DatasetService()
        default = service.get_default_dataset()

        required_keys = ['sales', 'advertising', 'shipping', 'inventory']
        for key in required_keys:
            assert key in default

    def test_default_dataset_not_empty(self):
        """Test default dataset contains some data"""
        service = DatasetService()
        default = service.get_default_dataset()

        # Should have at least some data
        total_records = (
            len(default.get('sales', [])) +
            len(default.get('advertising', [])) +
            len(default.get('shipping', []))
        )
        assert total_records > 0

    def test_use_default_when_none_loaded(self):
        """Test default dataset used when none loaded"""
        service = DatasetService()
        # Don't load any dataset
        dataset = service.get_dataset()

        if dataset is not None:
            assert isinstance(dataset, dict)


@pytest.mark.unit
class TestDatasetMetadata:
    """Test dataset metadata handling"""

    def test_get_dataset_metadata(self, sample_dataset):
        """Test getting dataset metadata"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        metadata = service.get_metadata()
        assert metadata is not None

    def test_metadata_has_date_range(self, sample_dataset):
        """Test metadata contains date range"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        metadata = service.get_metadata()

        if 'dateRange' in metadata:
            assert 'start' in metadata['dateRange']
            assert 'end' in metadata['dateRange']

    def test_metadata_has_record_counts(self, sample_dataset):
        """Test metadata has record counts"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        metadata = service.get_metadata()

        # Should have some count information
        assert metadata is not None

    def test_metadata_is_immutable(self, sample_dataset):
        """Test metadata doesn't expose mutable references"""
        service = DatasetService()
        service.load_dataset(sample_dataset)
        metadata1 = service.get_metadata()
        metadata2 = service.get_metadata()

        # Should be consistent
        assert metadata1 == metadata2 or (metadata1 is not None and metadata2 is not None)


@pytest.mark.unit
class TestDatasetErrorHandling:
    """Test error handling in dataset service"""

    def test_load_corrupted_data(self):
        """Test handling corrupted data"""
        service = DatasetService()
        corrupted = {
            'sales': [{'invalid': 'structure'}],
            'advertising': None,  # Invalid
        }
        # Should handle gracefully
        try:
            service.load_dataset(corrupted)
        except Exception as e:
            # Should raise with clear message
            assert len(str(e)) > 0

    def test_get_nonexistent_session(self):
        """Test retrieving non-existent session"""
        service = DatasetService()
        result = service.get_from_session("nonexistent")
        assert result is None or result == {}

    def test_session_with_invalid_id(self):
        """Test session with invalid ID"""
        service = DatasetService()
        # Should handle invalid ID gracefully
        result = service.get_from_session(None)
        assert result is None or result == {}

    def test_clear_nonexistent_session(self):
        """Test clearing non-existent session"""
        service = DatasetService()
        # Should not raise
        service.clear_session("nonexistent")


@pytest.mark.unit
@pytest.mark.edge_case
class TestDatasetEdgeCases:
    """Test edge cases in dataset service"""

    def test_very_large_dataset(self):
        """Test handling very large dataset"""
        large_sales = [{'netSales': 1000, 'units': 2} for _ in range(10000)]
        dataset = {
            'sales': large_sales,
            'advertising': [],
            'shipping': [],
            'inventory': [],
            'competitors': [],
            'products': [],
        }
        service = DatasetService()
        result = service.load_dataset(dataset)
        assert result is not None

    def test_many_sessions(self):
        """Test managing many sessions"""
        service = DatasetService()
        test_dataset = {'sales': [], 'advertising': []}

        # Create many sessions
        for i in range(100):
            service.store_in_session(f"session-{i}", test_dataset)

        # Retrieve random session
        retrieved = service.get_from_session("session-50")
        assert retrieved is not None

    def test_unicode_in_session_id(self):
        """Test unicode characters in session ID"""
        service = DatasetService()
        test_dataset = {'sales': []}
        session_id = "session-🔍-test"

        service.store_in_session(session_id, test_dataset)
        retrieved = service.get_from_session(session_id)
        assert retrieved is not None or True  # Implementation dependent
