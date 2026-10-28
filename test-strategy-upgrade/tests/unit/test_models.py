import pytest
from decimal import Decimal
from src.order_system.models import Product, OrderItem, Order

@pytest.mark.unit
class TestProduct:
    """Unit tests for Product model"""
    
    def test_product_creation(self):
        """Test product instantiation with valid data"""
        product = Product(id="P001", name="Laptop", price=Decimal('999.99'), stock=10)
        assert product.id == "P001", "Product ID mismatch"
        assert product.name == "Laptop", "Product name mismatch"
        assert product.price == Decimal('999.99'), "Product price mismatch"
        assert product.stock == 10, "Product stock mismatch"
    
    def test_product_price_type(self):
        """Test that price is stored as Decimal"""
        product = Product(id="P002", name="Mouse", price=Decimal('25.50'), stock=50)
        assert isinstance(product.price, Decimal), "Price must be of type Decimal"
        assert product.price == Decimal('25.50')

@pytest.mark.unit
class TestOrderItem:
    """Unit tests for OrderItem model"""
    
    @pytest.fixture
    def sample_product(self):
        return Product(id="P001", name="Test Product", price=Decimal('29.99'), stock=100)
    
    def test_order_item_subtotal(self, sample_product):
        """Test subtotal calculation for order item"""
        item = OrderItem(product=sample_product, quantity=3)
        expected_subtotal = Decimal('89.97')
        assert item.get_subtotal() == expected_subtotal, f"Expected subtotal {expected_subtotal}, got {item.get_subtotal()}"
    
    def test_order_item_subtotal_single_quantity(self, sample_product):
        """Test subtotal with quantity of 1"""
        item = OrderItem(product=sample_product, quantity=1)
        assert item.get_subtotal() == sample_product.price, "Subtotal for single quantity must equal unit price"

@pytest.mark.unit
class TestOrder:
    """Unit tests for Order model"""
    
    @pytest.fixture
    def sample_order_items(self):
        p1 = Product("P001", "Item A", Decimal('10.00'), 10)
        p2 = Product("P002", "Item B", Decimal('20.00'), 10)
        return [OrderItem(p1, 2), OrderItem(p2, 1)] # 20 + 20 = 40
    
    def test_order_total_no_discount(self, sample_order_items):
        """Test order total calculation without discount"""
        order = Order(order_id="ORD-1", items=sample_order_items)
        assert order.calculate_total() == Decimal('40.00')
    
    def test_order_total_with_discount(self, sample_order_items):
        """Test order total with discount applied"""
        order = Order(order_id="ORD-2", items=sample_order_items, discount_percent=Decimal('10'))
        # 40 - 10% = 36.00
        assert order.calculate_total() == Decimal('36.00')
    
    def test_order_empty_items(self):
        """Test order with no items"""
        order = Order(order_id="ORD-3", items=[])
        assert order.calculate_total() == Decimal('0.00')
