from typing import Any

def my_function(*, x: Any) -> None:
    """
    Adds 25 to the input and prints the result.

    Args:
        x (Any): The value to which 25 will be added.

    Returns:
        None

    Raises:
        TypeError: If x is not a numeric type.

    Example:
        >>> my_function(x=3)
        28
    """
    # TODO: Add type checking for x to ensure it's a numeric type
    # TODO: Consider returning the result instead of printing it
    print(x + 25)

# TODO: Fix the function call to use keyword argument
my_function(3)
