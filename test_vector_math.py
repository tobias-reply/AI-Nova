#!/usr/bin/env python3
"""
Test script for vector_math.py functions.
"""

import math
from vector_math import *

def test_vector_magnitude():
    """Test vector magnitude calculation."""
    print("Testing vector_magnitude...")
    
    # Test 2D vector
    assert abs(vector_magnitude([3, 4]) - 5.0) < 1e-10
    
    # Test 3D vector
    assert abs(vector_magnitude([1, 2, 2]) - 3.0) < 1e-10
    
    # Test zero vector
    assert vector_magnitude([0, 0, 0]) == 0.0
    
    print("✓ vector_magnitude tests passed")


def test_dot_product():
    """Test dot product calculation."""
    print("Testing dot_product...")
    
    # Basic test
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32
    
    # Perpendicular vectors
    assert dot_product([1, 0], [0, 1]) == 0
    
    # Same vector
    assert dot_product([2, 3], [2, 3]) == 13
    
    print("✓ dot_product tests passed")


def test_cross_product_3d():
    """Test 3D cross product calculation."""
    print("Testing cross_product_3d...")
    
    # Standard basis vectors
    result = cross_product_3d([1, 0, 0], [0, 1, 0])
    assert result == [0, 0, 1]
    
    # Another test
    result = cross_product_3d([1, 2, 3], [4, 5, 6])
    assert result == [-3, 6, -3]
    
    print("✓ cross_product_3d tests passed")


def test_normalize_vector():
    """Test vector normalization."""
    print("Testing normalize_vector...")
    
    # Test with [3, 4]
    normalized = normalize_vector([3, 4])
    assert abs(normalized[0] - 0.6) < 1e-10
    assert abs(normalized[1] - 0.8) < 1e-10
    assert abs(vector_magnitude(normalized) - 1.0) < 1e-10
    
    print("✓ normalize_vector tests passed")


def test_vector_angle():
    """Test angle calculation between vectors."""
    print("Testing vector_angle...")
    
    # 90 degree angle
    angle = vector_angle([1, 0], [0, 1])
    assert abs(angle - math.pi/2) < 1e-10
    
    # 0 degree angle (same direction)
    angle = vector_angle([1, 1], [2, 2])
    assert abs(angle) < 1e-10
    
    # 180 degree angle (opposite direction)
    angle = vector_angle([1, 0], [-1, 0])
    assert abs(angle - math.pi) < 1e-10
    
    print("✓ vector_angle tests passed")


def test_vector_operations():
    """Test basic vector operations."""
    print("Testing vector operations...")
    
    # Addition
    result = vector_add([1, 2, 3], [4, 5, 6])
    assert result == [5, 7, 9]
    
    # Subtraction
    result = vector_subtract([4, 5, 6], [1, 2, 3])
    assert result == [3, 3, 3]
    
    # Scalar multiplication
    result = scalar_multiply([1, 2, 3], 2)
    assert result == [2, 4, 6]
    
    print("✓ vector operations tests passed")


def test_distance_between_points():
    """Test distance calculation."""
    print("Testing distance_between_points...")
    
    # 3-4-5 triangle
    distance = distance_between_points([0, 0], [3, 4])
    assert abs(distance - 5.0) < 1e-10
    
    # Same point
    distance = distance_between_points([1, 2, 3], [1, 2, 3])
    assert distance == 0.0
    
    print("✓ distance_between_points tests passed")


def test_vector_projection():
    """Test vector projection."""
    print("Testing vector_projection...")
    
    # Project [2, 3] onto [1, 0]
    projection = vector_projection([2, 3], [1, 0])
    assert projection == [2, 0]
    
    # Project onto same vector
    projection = vector_projection([3, 4], [3, 4])
    assert projection == [3, 4]
    
    print("✓ vector_projection tests passed")


def test_parallel_and_perpendicular():
    """Test parallel and perpendicular checks."""
    print("Testing parallel and perpendicular checks...")
    
    # Parallel vectors
    assert are_vectors_parallel([1, 2], [2, 4])
    assert are_vectors_parallel([1, 0], [-2, 0])  # Anti-parallel
    
    # Perpendicular vectors
    assert are_vectors_perpendicular([1, 0], [0, 1])
    assert are_vectors_perpendicular([3, 4], [-4, 3])
    
    # Not parallel or perpendicular
    assert not are_vectors_parallel([1, 0], [0, 1])
    assert not are_vectors_perpendicular([1, 1], [1, 0])
    
    print("✓ parallel and perpendicular tests passed")


def main():
    """Run all tests."""
    print("Running vector math tests...\n")
    
    test_vector_magnitude()
    test_dot_product()
    test_cross_product_3d()
    test_normalize_vector()
    test_vector_angle()
    test_vector_operations()
    test_distance_between_points()
    test_vector_projection()
    test_parallel_and_perpendicular()
    
    print("\n🎉 All tests passed! Vector math functions are working correctly.")


if __name__ == "__main__":
    main()