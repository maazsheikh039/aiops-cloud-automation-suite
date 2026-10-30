"""
Refactored version using Strategy Pattern and early returns to minimize complexity.
"""

from typing import List, Dict, Optional
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""
    
    @abstractmethod
    def calculate_discount(self, price: float, customer_type: str, is_holiday: bool) -> float:
        pass

class ElectronicsDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, price: float, customer_type: str, is_holiday: bool) -> float:
        if price > 1000:
            if customer_type == 'premium':
                return price * (0.7 if is_holiday else 0.8)
            return price * (0.85 if is_holiday else 0.9)
        return price * (0.9 if customer_type == 'premium' else 0.95)

class ClothingDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, price: float, customer_type: str, is_holiday: bool) -> float:
        # Clothing discount strategy logic
        return price * 0.85

class DefaultDiscountStrategy(DiscountStrategy):
    def calculate_discount(self, price: float, customer_type: str, is_holiday: bool) -> float:
        return price

def get_discount_strategy(category: str) -> DiscountStrategy:
    strategies = {
        'electronics': ElectronicsDiscountStrategy(),
        'clothing': ClothingDiscountStrategy()
    }
    return strategies.get(category, DefaultDiscountStrategy())

def calculate_total(items: List[Dict], discount_code: Optional[str], 
                   customer_type: str, is_holiday: bool) -> float:
    total = 0.0
    for item in items:
        strategy = get_discount_strategy(item.get('category'))
        item_total = strategy.calculate_discount(item.get('price', 0.0), customer_type, is_holiday)
        if item.get('category') not in ['electronics', 'clothing'] and discount_code:
            item_total *= 0.9
        total += item_total
    
    if discount_code == 'VIP20':
        total *= 0.8
        
    return total

def process_order(order_data: Optional[Dict]) -> Optional[float]:
    if not order_data:
        return None
    items = order_data.get('items')
    if not items:
        return 0 if items is not None else None
    customer = order_data.get('customer')
    if not customer:
        return None
        
    return calculate_total(
        items,
        order_data.get('discount_code'),
        customer.get('type', 'regular'),
        order_data.get('is_holiday', False)
    )
