import math
from typing import List, Tuple, Union

Vector = Union[List[float], Tuple[float, ...]]


def magnitude(vector: Vector) -> float:
    """
    Calculate the magnitude (length) of a vector.
    
    Args:
        vector: A list or tuple of numeric values representing the vector
        
    Returns:
        The magnitude of the vector
        
    Example:
        >>> magnitude([3, 4])
        5.0
        >>> magnitude([1, 2, 2])
        3.0
    """
    return math.sqrt(sum(x ** 2 for x in vector))


def dot_product(vector1: Vector, vector2: Vector) -> float:
    """
    Calculate the dot product of two vectors.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        The dot product of the two vectors
        
    Raises:
        ValueError: If vectors have different dimensions
        
    Example:
        >>> dot_product([1, 2], [3, 4])
        11.0
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32.0
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimensions")
    
    return sum(a * b for a, b in zip(vector1, vector2))


def cross_product_2d(vector1: Vector, vector2: Vector) -> float:
    """
    Calculate the cross product of two 2D vectors (returns scalar).
    
    Args:
        vector1: First 2D vector
        vector2: Second 2D vector
        
    Returns:
        The scalar cross product (z-component of the 3D cross product)
        
    Raises:
        ValueError: If vectors are not 2D
        
    Example:
        >>> cross_product_2d([1, 2], [3, 4])
        -2.0
    """
    if len(vector1) != 2 or len(vector2) != 2:
        raise ValueError("Both vectors must be 2D")
    
    return vector1[0] * vector2[1] - vector1[1] * vector2[0]


def cross_product_3d(vector1: Vector, vector2: Vector) -> List[float]:
    """
    Calculate the cross product of two 3D vectors.
    
    Args:
        vector1: First 3D vector
        vector2: Second 3D vector
        
    Returns:
        The cross product as a 3D vector
        
    Raises:
        ValueError: If vectors are not 3D
        
    Example:
        >>> cross_product_3d([1, 0, 0], [0, 1, 0])
        [0.0, 0.0, 1.0]
    """
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Both vectors must be 3D")
    
    return [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]


def distance(vector1: Vector, vector2: Vector) -> float:
    """
    Calculate the Euclidean distance between two vectors.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        The Euclidean distance between the vectors
        
    Raises:
        ValueError: If vectors have different dimensions
        
    Example:
        >>> distance([0, 0], [3, 4])
        5.0
        >>> distance([1, 2, 3], [4, 5, 6])
        5.196152422706632
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimensions")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vector1, vector2)))


def angle_between_vectors(vector1: Vector, vector2: Vector, degrees: bool = False) -> float:
    """
    Calculate the angle between two vectors.
    
    Args:
        vector1: First vector
        vector2: Second vector
        degrees: If True, return angle in degrees; otherwise in radians
        
    Returns:
        The angle between the vectors
        
    Raises:
        ValueError: If vectors have different dimensions or if either vector is zero
        
    Example:
        >>> angle_between_vectors([1, 0], [0, 1])
        1.5707963267948966
        >>> angle_between_vectors([1, 0], [0, 1], degrees=True)
        90.0
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimensions")
    
    mag1 = magnitude(vector1)
    mag2 = magnitude(vector2)
    
    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot calculate angle with zero vector")
    
    cos_angle = dot_product(vector1, vector2) / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to avoid numerical errors
    
    angle_rad = math.acos(cos_angle)
    
    return math.degrees(angle_rad) if degrees else angle_rad


def normalize(vector: Vector) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: The vector to normalize
        
    Returns:
        The normalized vector
        
    Raises:
        ValueError: If the vector is a zero vector
        
    Example:
        >>> normalize([3, 4])
        [0.6, 0.8]
        >>> normalize([1, 1, 1])
        [0.5773502691896258, 0.5773502691896258, 0.5773502691896258]
    """
    mag = magnitude(vector)
    
    if mag == 0:
        raise ValueError("Cannot normalize zero vector")
    
    return [x / mag for x in vector]


def add_vectors(vector1: Vector, vector2: Vector) -> List[float]:
    """
    Add two vectors element-wise.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        The sum of the two vectors
        
    Raises:
        ValueError: If vectors have different dimensions
        
    Example:
        >>> add_vectors([1, 2], [3, 4])
        [4, 6]
        >>> add_vectors([1, 2, 3], [4, 5, 6])
        [5, 7, 9]
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimensions")
    
    return [a + b for a, b in zip(vector1, vector2)]


def subtract_vectors(vector1: Vector, vector2: Vector) -> List[float]:
    """
    Subtract the second vector from the first vector element-wise.
    
    Args:
        vector1: First vector (minuend)
        vector2: Second vector (subtrahend)
        
    Returns:
        The difference of the two vectors (vector1 - vector2)
        
    Raises:
        ValueError: If vectors have different dimensions
        
    Example:
        >>> subtract_vectors([5, 7], [2, 3])
        [3, 4]
        >>> subtract_vectors([1, 2, 3], [4, 5, 6])
        [-3, -3, -3]
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimensions")
    
    return [a - b for a, b in zip(vector1, vector2)]


def scalar_multiply(vector: Vector, scalar: float) -> List[float]:
    """
    Multiply a vector by a scalar value.
    
    Args:
        vector: The vector to multiply
        scalar: The scalar value
        
    Returns:
        The vector multiplied by the scalar
        
    Example:
        >>> scalar_multiply([1, 2, 3], 2)
        [2, 4, 6]
        >>> scalar_multiply([3, 4], 0.5)
        [1.5, 2.0]
    """
    return [x * scalar for x in vector]


def projection(vector1: Vector, vector2: Vector) -> List[float]:
    """
    Calculate the projection of vector1 onto vector2.
    
    Args:
        vector1: The vector to project
        vector2: The vector to project onto
        
    Returns:
        The projection of vector1 onto vector2
        
    Raises:
        ValueError: If vectors have different dimensions or vector2 is zero
        
    Example:
        >>> projection([3, 4], [1, 0])
        [3.0, 0.0]
        >>> projection([2, 3], [1, 1])
        [2.5, 2.5]
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimensions")
    
    mag2_squared = sum(x ** 2 for x in vector2)
    
    if mag2_squared == 0:
        raise ValueError("Cannot project onto zero vector")
    
    scalar = dot_product(vector1, vector2) / mag2_squared
    
    return [x * scalar for x in vector2]


if __name__ == "__main__":
    # Example usage and tests
    print("Vector Math Library Examples:")
    print("=" * 40)
    
    # Test vectors
    v1 = [3, 4]
    v2 = [1, 2]
    v3 = [1, 0, 0]
    v4 = [0, 1, 0]
    
    print(f"Vector 1: {v1}")
    print(f"Vector 2: {v2}")
    print(f"Magnitude of v1: {magnitude(v1)}")
    print(f"Dot product: {dot_product(v1, v2)}")
    print(f"Distance between v1 and v2: {distance(v1, v2)}")
    print(f"Angle between v1 and v2 (degrees): {angle_between_vectors(v1, v2, degrees=True)}")
    print(f"Normalized v1: {normalize(v1)}")
    print(f"v1 + v2: {add_vectors(v1, v2)}")
    print(f"v1 - v2: {subtract_vectors(v1, v2)}")
    print(f"v1 * 2: {scalar_multiply(v1, 2)}")
    print(f"Projection of v1 onto v2: {projection(v1, v2)}")
    
    print(f"\n3D vectors: {v3}, {v4}")
    print(f"Cross product (3D): {cross_product_3d(v3, v4)}")
    
    print(f"\n2D cross product: {cross_product_2d(v1, v2)}")