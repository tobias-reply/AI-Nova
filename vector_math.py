import math
from typing import List, Tuple, Union

def vector_magnitude(vector: List[float]) -> float:
    """
    Calculate the magnitude (length) of a vector.
    
    Args:
        vector: List of vector components
        
    Returns:
        The magnitude of the vector
    """
    return math.sqrt(sum(component ** 2 for component in vector))


def dot_product(vector1: List[float], vector2: List[float]) -> float:
    """
    Calculate the dot product of two vectors.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        The dot product of the two vectors
        
    Raises:
        ValueError: If vectors have different dimensions
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimension")
    
    return sum(a * b for a, b in zip(vector1, vector2))


def cross_product_3d(vector1: List[float], vector2: List[float]) -> List[float]:
    """
    Calculate the cross product of two 3D vectors.
    
    Args:
        vector1: First 3D vector [x, y, z]
        vector2: Second 3D vector [x, y, z]
        
    Returns:
        The cross product as a 3D vector
        
    Raises:
        ValueError: If vectors are not 3-dimensional
    """
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Cross product is only defined for 3D vectors")
    
    x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
    y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
    z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    
    return [x, y, z]


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.
    
    Args:
        vector: Input vector
        
    Returns:
        Normalized vector with magnitude 1
        
    Raises:
        ValueError: If vector is zero vector
    """
    magnitude = vector_magnitude(vector)
    if magnitude == 0:
        raise ValueError("Cannot normalize zero vector")
    
    return [component / magnitude for component in vector]


def vector_angle(vector1: List[float], vector2: List[float]) -> float:
    """
    Calculate the angle between two vectors in radians.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        Angle between vectors in radians
        
    Raises:
        ValueError: If vectors have different dimensions or are zero vectors
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimension")
    
    dot_prod = dot_product(vector1, vector2)
    mag1 = vector_magnitude(vector1)
    mag2 = vector_magnitude(vector2)
    
    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot calculate angle with zero vector")
    
    cos_angle = dot_prod / (mag1 * mag2)
    # Clamp to avoid numerical errors
    cos_angle = max(-1, min(1, cos_angle))
    
    return math.acos(cos_angle)


def vector_angle_degrees(vector1: List[float], vector2: List[float]) -> float:
    """
    Calculate the angle between two vectors in degrees.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        Angle between vectors in degrees
    """
    angle_rad = vector_angle(vector1, vector2)
    return math.degrees(angle_rad)


def vector_add(vector1: List[float], vector2: List[float]) -> List[float]:
    """
    Add two vectors component-wise.
    
    Args:
        vector1: First vector
        vector2: Second vector
        
    Returns:
        Sum of the two vectors
        
    Raises:
        ValueError: If vectors have different dimensions
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimension")
    
    return [a + b for a, b in zip(vector1, vector2)]


def vector_subtract(vector1: List[float], vector2: List[float]) -> List[float]:
    """
    Subtract vector2 from vector1 component-wise.
    
    Args:
        vector1: First vector (minuend)
        vector2: Second vector (subtrahend)
        
    Returns:
        Difference vector1 - vector2
        
    Raises:
        ValueError: If vectors have different dimensions
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimension")
    
    return [a - b for a, b in zip(vector1, vector2)]


def scalar_multiply(vector: List[float], scalar: float) -> List[float]:
    """
    Multiply a vector by a scalar.
    
    Args:
        vector: Input vector
        scalar: Scalar value to multiply by
        
    Returns:
        Vector multiplied by scalar
    """
    return [component * scalar for component in vector]


def distance_between_points(point1: List[float], point2: List[float]) -> float:
    """
    Calculate the Euclidean distance between two points.
    
    Args:
        point1: First point coordinates
        point2: Second point coordinates
        
    Returns:
        Distance between the two points
        
    Raises:
        ValueError: If points have different dimensions
    """
    if len(point1) != len(point2):
        raise ValueError("Points must have the same dimension")
    
    difference_vector = vector_subtract(point2, point1)
    return vector_magnitude(difference_vector)


def vector_projection(vector_a: List[float], vector_b: List[float]) -> List[float]:
    """
    Calculate the projection of vector_a onto vector_b.
    
    Args:
        vector_a: Vector to be projected
        vector_b: Vector to project onto
        
    Returns:
        Projection of vector_a onto vector_b
        
    Raises:
        ValueError: If vectors have different dimensions or vector_b is zero
    """
    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimension")
    
    dot_prod = dot_product(vector_a, vector_b)
    magnitude_b_squared = sum(component ** 2 for component in vector_b)
    
    if magnitude_b_squared == 0:
        raise ValueError("Cannot project onto zero vector")
    
    scalar_proj = dot_prod / magnitude_b_squared
    return scalar_multiply(vector_b, scalar_proj)


def are_vectors_parallel(vector1: List[float], vector2: List[float], tolerance: float = 1e-10) -> bool:
    """
    Check if two vectors are parallel (or anti-parallel).
    
    Args:
        vector1: First vector
        vector2: Second vector
        tolerance: Tolerance for floating point comparison
        
    Returns:
        True if vectors are parallel, False otherwise
    """
    try:
        angle = vector_angle(vector1, vector2)
        return abs(angle) < tolerance or abs(angle - math.pi) < tolerance
    except ValueError:
        return False


def are_vectors_perpendicular(vector1: List[float], vector2: List[float], tolerance: float = 1e-10) -> bool:
    """
    Check if two vectors are perpendicular.
    
    Args:
        vector1: First vector
        vector2: Second vector
        tolerance: Tolerance for floating point comparison
        
    Returns:
        True if vectors are perpendicular, False otherwise
    """
    try:
        dot_prod = dot_product(vector1, vector2)
        return abs(dot_prod) < tolerance
    except ValueError:
        return False