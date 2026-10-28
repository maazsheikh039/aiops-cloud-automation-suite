import pytest
from decimal import Decimal
from src.order_system.models import Product
from src.order_system.inventory import InventoryManager

@pytest.mark.unit
class TestInventoryManager:
    """Unit tests for InventoryManager"""
    
    @pytest.fixture
    def inventory(self):
        return InventoryManager()
    
    @pytest.fixture
    def sample_product(self):
        return Product(id="P001", name="Laptop", price=Decimal('999.99'), stock=10)
    
    def test_add_product(self, inventory, sample_product):
        """Test adding product to inventory"""
        inventory.add_product(sample_product)
        assert inventory.get_product("P001") == sample_product
    
    def test_get_product_exists(self, inventory, sample_product):
        """Test retrieving existing product"""
        inventory.add_product(sample_product)
        retrieved = inventory.get_product("P001")
        assert retrieved is not None
        assert retrieved.name == "Laptop"
    
    def test_get_product_not_exists(self, inventory):
        """Test retrieving non-existent product"""
        assert inventory.get_product("UNKNOWN") is None
    
    def test_check_availability_sufficient_stock(self, inventory, sample_product):
        """Test availability check with sufficient stock"""
        inventory.add_product(sample_product)
        assert inventory.check_availability("P001", 5) is True
    
    def test_check_availability_insufficient_stock(self, inventory, sample_product):
        """Test availability check with insufficient stock"""
        inventory.add_product(sample_product)
        assert inventory.check_availability("P001", 15) is False
    
    def test_reduce_stock_success(self, inventory, sample_product):
        """Test successful stock reduction"""
        inventory.add_product(sample_product)
        success = inventory.reduce_stock("P001", 3)
        assert success is True
        assert inventory.get_product("P001").stock == 7
    
    def test_reduce_stock_failure(self, inventory, sample_product):
        """Test stock reduction failure with insufficient stock"""
        inventory.add_product(sample_product)
        success = inventory.reduce_stock("P001", 15)
        assert success is False
        assert inventory.get_product("P001").stock == 10
