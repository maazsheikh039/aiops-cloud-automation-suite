import os
import sys


def calculate_sum(a, b):
    """
    Calculate sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    result = a + b
    return result


def process_data(x):
    """
    Process data and print result.

    Args:
        x: Number to process
    """
    if x > 0:
        print("Positive")
    else:
        print("Negative")


if __name__ == "__main__":
    print(calculate_sum(5, 10))
