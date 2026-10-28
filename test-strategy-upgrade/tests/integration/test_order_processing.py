import pytest
from decimal import Decimal
from src.order_system.models import Product, OrderItem, Order
from src.order_system.inventory import InventoryManager
from src.order_system.processor import OrderProcessor

@pytest.mark.integration
class TestOrderProcessingIntegration:
    """Integration tests for complete order processing workflow"""
    
    @pytest.fixture
    def setup_system(self):
        inventory = InventoryManager()
        processor = OrderProcessor(inventory)
        
        products = [
            Product("P001", "Laptop", Decimal('999.99'), 5),
            Product("P002", "Mouse", Decimal('29.99'), 20),
            Product("P003", "Keyboard", Decimal('79.99'), 15)
        ]
        
        for product in products:
            inventory.add_product(product)
            
        return {
            'inventory': inventory,
            'processor': processor,
            'products': products
        }
    
    def test_successful_order_processing(self, setup_system):
        """Test complete successful order flow"""
        inventory = setup_system['inventory']
        processor = setup_system['processor']
        
        item = OrderItem(product=inventory.get_product("P001"), quantity=2)
        order = Order(order_id="ORD-100", items=[item])
        
        success, msg = processor.process_order(order)
        assert success is True, f"Order processing failed: {msg}"
        assert inventory.get_product("P001").stock == 3, "Stock should be reduced from 5 to 3"
        assert order in processor.processed_orders, "Order must be recorded in processed orders"
    
    def test_order_validation_failure_out_of_stock(self, setup_system):
        """Test order validation fails for out-of-stock items"""
        inventory = setup_system['inventory']
        processor = setup_system['processor']
        
        item = OrderItem(product=inventory.get_product("P001"), quantity=10) # Only 5 available
        order = Order(order_id="ORD-101", items=[item])
        
        success, msg = processor.process_order(order)
        assert success is False, "Order processing should fail due to stock limit"
        assert "Insufficient stock" in msg
    
    def test_order_processing_failure_maintains_inventory(self, setup_system):
        """Test that failed orders don't modify inventory"""
        inventory = setup_system['inventory']
        processor = setup_system['processor']
        
        initial_stock = inventory.get_product("P002").stock
        item = OrderItem(product=inventory.get_product("P002"), quantity=25) # Exceeds 20
        order = Order(order_id="ORD-102", items=[item])
        
        success, _ = processor.process_order(order)
        assert success is False
        assert inventory.get_product("P002").stock == initial_stock, "Inventory stock must remain untouched on failure"
    
    def test_multiple_orders_sequential_processing(self, setup_system):
        """Test processing multiple orders sequentially"""
        inventory = setup_system['inventory']
        processor = setup_system['processor']
        
        order1 = Order(order_id="ORD-201", items=[OrderItem(inventory.get_product("P003"), 5)])
        order2 = Order(order_id="ORD-202", items=[OrderItem(inventory.get_product("P003"), 5)])
        
        s1, _ = processor.process_order(order1)
        s2, _ = processor.process_order(order2)
        
        assert s1 is True and s2 is True
        assert inventory.get_product("P003").stock == 5 # 15 - 5 - 5 = 5
        assert len(processor.processed_orders) == 2
    
    def test_order_with_discount_integration(self, setup_system):
        """Test order processing with discount applied"""
        inventory = setup_system['inventory']
        processor = setup_system['processor']
        
        item = OrderItem(product=inventory.get_product("P002"), quantity=2) # 2 * 29.99 = 59.98
        order = Order(order_id="ORD-301", items=[item], discount_percent=Decimal('20')) # 20% off -> 47.98
        
        success, _ = processor.process_order(order)
        assert success is True
        assert order.calculate_total() == Decimal('47.98')
