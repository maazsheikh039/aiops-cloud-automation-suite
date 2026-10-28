from typing import List, Tuple
from .models import Order, OrderItem, Product
from .inventory import InventoryManager

class OrderProcessor:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory = inventory_manager
        self.processed_orders: List[Order] = []
    
    def validate_order(self, order: Order) -> Tuple[bool, str]:
        """Validate order items against inventory"""
        if not order.items:
            return False, "Order contains no items."
            
        for item in order.items:
            product_id = item.product.id
            if not self.inventory.check_availability(product_id, item.quantity):
                stock = self.inventory.get_product(product_id)
                stock_amt = stock.stock if stock else 0
                return False, f"Insufficient stock for product {product_id}. Requested: {item.quantity}, Available: {stock_amt}"
                
        return True, ""
    
    def process_order(self, order: Order) -> Tuple[bool, str]:
        """Process an order: validate and update inventory"""
        is_valid, error_msg = self.validate_order(order)
        if not is_valid:
            return False, error_msg
            
        # Reduce stock for each item
        for item in order.items:
            success = self.inventory.reduce_stock(item.product.id, item.quantity)
            if not success:
                return False, f"Failed to reduce stock for product {item.product.id}"
                
        self.processed_orders.append(order)
        return True, "Order processed successfully."
