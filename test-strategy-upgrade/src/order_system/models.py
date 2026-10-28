from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class Product:
    id: str
    name: str
    price: Decimal
    stock: int

@dataclass
class OrderItem:
    product: Product
    quantity: int
    
    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this order item"""
        return self.product.price * Decimal(str(self.quantity))

@dataclass
class Order:
    order_id: str
    items: List[OrderItem]
    discount_percent: Decimal = Decimal('0')
    
    def calculate_total(self) -> Decimal:
        """Calculate order total with discount applied"""
        if not self.items:
            return Decimal('0.00')
        
        subtotal_sum = sum((item.get_subtotal() for item in self.items), Decimal('0.00'))
        
        if self.discount_percent > 0:
            discount_amount = subtotal_sum * (self.discount_percent / Decimal('100'))
            total = subtotal_sum - discount_amount
            return total.quantize(Decimal('0.01'))
            
        return subtotal_sum.quantize(Decimal('0.01'))
