#!/usr/bin/env python3
"""
Simple test file for vector_math.py
"""

from vector_math import (
    magnitude, dot_product, cross_product_2d, cross_product_3d,
    distance, angle_between_vectors, normalize, add_vectors,
    subtract_vectors, scalar_multiply, projection
)
import math


def test_basic_operations():
    """Test basic vector operations"""
    print("Testing basic vector operations...")
    
    # Test magnitude
    assert abs(magnitude([3, 4]) - 5.0) < 1e-10
    assert abs(magnitude([1, 2, 2]) - 3.0) < 1e-10
    print("✓ Magnitude tests passed")
    
    # Test dot product
    assert dot_product([1, 2], [3, 4]) == 11
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32
    print("✓ Dot product tests passed")
    
    # Test cross product 2D
    assert cross_product_2d([1, 2], [3, 4]) == -2
    print("✓ Cross product 2D tests passed")
    
    # Test cross product 3D
    result = cross_product_3d([1, 0, 0], [0, 1, 0])
    assert result == [0, 0, 1]
    print("✓ Cross product 3D tests passed")
    
    # Test distance
    assert distance([0, 0], [3, 4]) == 5.0
    print("✓ Distance tests passed")
    
    # Test angle between vectors
    angle = angle_between_vectors([1, 0], [0, 1], degrees=True)
    assert abs(angle - 90.0) < 1e-10
    print("✓ Angle tests passed")
    
    # Test normalize
    normalized = normalize([3, 4])
    assert abs(normalized[0] - 0.6) < 1e-10
    assert abs(normalized[1] - 0.8) < 1e-10
    print("✓ Normalize tests passed")
    
    # Test vector addition
    result = add_vectors([1, 2], [3, 4])
    assert result == [4, 6]
    print("✓ Vector addition tests passed")
    
    # Test vector subtraction
    result = subtract_vectors([5, 7], [2, 3])
    assert result == [3, 4]
    print("✓ Vector subtraction tests passed")
    
    # Test scalar multiplication
    result = scalar_multiply([1, 2, 3], 2)
    assert result == [2, 4, 6]
    print("✓ Scalar multiplication tests passed")
    
    print("\nAll tests passed! ✅")


def demonstrate_usage():
    """Demonstrate usage of the vector math functions"""
    print("\n" + "="*50)
    print("VECTOR MATH LIBRARY DEMONSTRATION")
    print("="*50)
    
    # Example vectors
    v1 = [3, 4]
    v2 = [1, 2]
    v3 = [1, 0, 0]
    v4 = [0, 1, 0]
    
    print(f"Vector 1: {v1}")
    print(f"Vector 2: {v2}")
    print(f"Magnitude of v1: {magnitude(v1)}")
    print(f"Dot product: {dot_product(v1, v2)}")
    print(f"Distance between v1 and v2: {distance(v1, v2):.3f}")
    print(f"Angle between v1 and v2 (degrees): {angle_between_vectors(v1, v2, degrees=True):.2f}°")
    print(f"Normalized v1: [{normalize(v1)[0]:.3f}, {normalize(v1)[1]:.3f}]")
    print(f"v1 + v2: {add_vectors(v1, v2)}")
    print(f"v1 - v2: {subtract_vectors(v1, v2)}")
    print(f"v1 * 2: {scalar_multiply(v1, 2)}")
    
    proj = projection(v1, v2)
    print(f"Projection of v1 onto v2: [{proj[0]:.3f}, {proj[1]:.3f}]")
    
    print(f"\n3D vectors: {v3}, {v4}")
    print(f"Cross product (3D): {cross_product_3d(v3, v4)}")
    
    print(f"\n2D cross product of {v1} and {v2}: {cross_product_2d(v1, v2)}")


if __name__ == "__main__":
    test_basic_operations()
    demonstrate_usage()