#!/usr/bin/env python3
"""
Simple test for the Documentation Agent.

This module contains sample functions and a class to demonstrate
the documentation improvement capabilities of the Documentation Agent.
"""

from typing import List, Union

def calculate_sum(a: float, b: float) -> float:
    """
    Calculate the sum of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    return a + b

def process_data(data: List[float]) -> List[float]:
    """
    Process a list of numbers, doubling positive values.

    Args:
        data (List[float]): A list of numbers to process.

    Returns:
        List[float]: A new list containing doubled positive values from the input.
    """
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result

class DataProcessor:
    """
    A class for processing data items and tracking the number of processed items.
    """

    def __init__(self, name: str):
        """
        Initialize a DataProcessor instance.

        Args:
            name (str): The name of the data processor.
        """
        self.name = name
        self.processed_count = 0
    
    def process_item(self, item: Union[str, int, float]) -> str:
        """
        Process a single item by converting it to uppercase if it's a string,
        or converting it to a string if it's a number.

        Args:
            item (Union[str, int, float]): The item to process.

        Returns:
            str: The processed item as a string.
        """
        self.processed_count += 1
        return item.upper() if isinstance(item, str) else str(item)

# TODO: Consider adding error handling for invalid input types in process_item method