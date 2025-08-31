"""
Test script for complex integration functions
"""

from complex_integration import (
    complex_integrate, 
    line_integral, 
    contour_integral,
    example_polynomial,
    example_exponential,
    example_rational
)
import cmath
import math


def test_basic_integration():
    """Test basic complex integration functionality."""
    print("Testing Basic Integration...")
    
    # Test real function integration
    def real_func(z):
        return z.real**2
    
    result = complex_integrate(real_func, 0, 2, n=1000, method="simpson")
    expected = 8/3  # ∫x²dx from 0 to 2 = 8/3
    print(f"Real integration test: {result.real:.6f} (expected: {expected:.6f})")
    
    # Test complex polynomial
    result = complex_integrate(example_polynomial, 0, 1+1j, n=1000)
    print(f"Polynomial integration: {result}")
    
    return True


def test_line_integral():
    """Test line integral functionality."""
    print("\nTesting Line Integrals...")
    
    # Simple constant function
    def constant_func(z):
        return 1
    
    result = line_integral(constant_func, 0, 1+1j, n=1000)
    expected = 1+1j  # Length of path times constant
    print(f"Constant line integral: {result} (expected: {expected})")
    
    return True


def test_contour_integral():
    """Test contour integral functionality."""
    print("\nTesting Contour Integrals...")
    
    # Test 1/z around unit circle (should be 2πi)
    def inverse_func(z):
        if abs(z) < 1e-10:
            return 0
        return 1/z
    
    result = contour_integral(inverse_func, 0, 1, n=2000)
    expected = 2j * math.pi
    print(f"1/z contour integral: {result} (expected: {expected})")
    print(f"Difference: {abs(result - expected)}")
    
    return True


def main():
    """Run all tests."""
    print("Complex Function Integration Test Suite")
    print("=" * 50)
    
    try:
        test_basic_integration()
        test_line_integral()
        test_contour_integral()
        
        print("\n" + "=" * 50)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    main()