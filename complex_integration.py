"""
Complex Function Integration Module

This module provides functions for integrating complex mathematical functions
using numerical methods. It supports both real and complex-valued functions.
"""

import cmath
import math
from typing import Callable, Union, Tuple, Optional


def complex_integrate(
    func: Callable[[complex], complex],
    a: Union[float, complex],
    b: Union[float, complex],
    n: int = 1000,
    method: str = "simpson"
) -> complex:
    """
    Integrate a complex function over a path in the complex plane.
    
    Args:
        func: Function to integrate (takes complex, returns complex)
        a: Starting point of integration path
        b: Ending point of integration path
        n: Number of subdivisions (must be even for Simpson's rule)
        method: Integration method ("simpson", "trapezoidal", or "midpoint")
    
    Returns:
        Complex number representing the integral value
    
    Raises:
        ValueError: If n is not even for Simpson's rule or method is invalid
    """
    if method == "simpson" and n % 2 != 0:
        raise ValueError("Number of subdivisions must be even for Simpson's rule")
    
    if method not in ["simpson", "trapezoidal", "midpoint"]:
        raise ValueError("Method must be 'simpson', 'trapezoidal', or 'midpoint'")
    
    # Convert to complex numbers
    a = complex(a)
    b = complex(b)
    
    # Calculate step size
    h = (b - a) / n
    
    if method == "simpson":
        return _simpson_complex(func, a, h, n)
    elif method == "trapezoidal":
        return _trapezoidal_complex(func, a, h, n)
    else:  # midpoint
        return _midpoint_complex(func, a, h, n)


def _simpson_complex(func: Callable[[complex], complex], a: complex, h: complex, n: int) -> complex:
    """Simpson's 1/3 rule for complex integration."""
    result = func(a) + func(a + n * h)
    
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            result += 2 * func(x)
        else:
            result += 4 * func(x)
    
    return result * h / 3


def _trapezoidal_complex(func: Callable[[complex], complex], a: complex, h: complex, n: int) -> complex:
    """Trapezoidal rule for complex integration."""
    result = (func(a) + func(a + n * h)) / 2
    
    for i in range(1, n):
        result += func(a + i * h)
    
    return result * h


def _midpoint_complex(func: Callable[[complex], complex], a: complex, h: complex, n: int) -> complex:
    """Midpoint rule for complex integration."""
    result = 0
    
    for i in range(n):
        midpoint = a + (i + 0.5) * h
        result += func(i)
    
    return result * h


def line_integral(
    func: Callable[[complex], complex],
    start: complex,
    end: complex,
    n: int = 1000
) -> complex:
    """
    Compute line integral of a complex function along a straight line.
    
    Args:
        func: Complex function to integrate
        start: Starting point in complex plane
        end: Ending point in complex plane
        n: Number of subdivisions
    
    Returns:
        Value of the line integral
    """
    def parametric_func(t: float) -> complex:
        z = start + t * (end - start)
        return func(z) * (end - start)
    
    # Convert to real integration from 0 to 1
    h = 1.0 / n
    result = 0
    
    for i in range(n):
        t = (i + 0.5) * h
        result += parametric_func(t)
    
    return result * h


def contour_integral(
    func: Callable[[complex], complex],
    center: complex,
    radius: float,
    n: int = 1000
) -> complex:
    """
    Compute contour integral around a circle.
    
    Args:
        func: Complex function to integrate
        center: Center of the circular contour
        radius: Radius of the circular contour
        n: Number of subdivisions
    
    Returns:
        Value of the contour integral
    """
    def parametric_func(theta: float) -> complex:
        z = center + radius * cmath.exp(1j * theta)
        return func(z) * 1j * radius * cmath.exp(1j * theta)
    
    # Integrate from 0 to 2π
    h = 2 * math.pi / n
    result = 0
    
    for i in range(n):
        theta = (i + 0.5) * h
        result += parametric_func(theta)
    
    return result * h


# Example functions for testing
def example_polynomial(z: complex) -> complex:
    """Example: z^2 + 2z + 1"""
    return z**2 + 2*z + 1


def example_exponential(z: complex) -> complex:
    """Example: e^z"""
    return cmath.exp(z)


def example_rational(z: complex) -> complex:
    """Example: 1/(z^2 + 1)"""
    return 1 / (z**2 + 1)


if __name__ == "__main__":
    # Example usage
    print("Complex Function Integration Examples")
    print("=" * 40)
    
    # Example 1: Integrate z^2 from 0 to 1+i
    result1 = complex_integrate(example_polynomial, 0, 1+1j, n=1000)
    print(f"∫(z² + 2z + 1)dz from 0 to 1+i = {result1}")
    
    # Example 2: Line integral
    result2 = line_integral(example_exponential, 0, 1j*math.pi, n=1000)
    print(f"Line integral of e^z from 0 to iπ = {result2}")
    
    # Example 3: Contour integral around unit circle
    result3 = contour_integral(example_rational, 0, 1, n=1000)
    print(f"Contour integral of 1/(z²+1) around unit circle = {result3}")