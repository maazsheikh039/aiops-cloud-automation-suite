import pytest
from legacy_calculator import calculate_total, process_order

SAMPLE_ITEMS = [
    {'category': 'electronics', 'price': 1200},
    {'category': 'clothing', 'price': 50},
    {'category': 'books', 'price': 30}
]

def test_calculate_total_basic(benchmark):
    benchmark(calculate_total, SAMPLE_ITEMS, 'SUMMER', 'premium', True)

def test_process_order_benchmark(benchmark):
    order = {
        'items': SAMPLE_ITEMS,
        'customer': {'type': 'premium'},
        'discount_code': 'SUMMER',
        'is_holiday': True
    }
    benchmark(process_order, order)
