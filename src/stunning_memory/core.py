"""Core functionality for stunning_memory package."""


def example_function(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message string.

    Examples:
        >>> example_function()
        'Hello, World!'
        >>> example_function("Python")
        'Hello, Python!'
    """
    return f"Hello, {name}!"


class ExampleClass:
    """An example class demonstrating basic structure.

    Attributes:
        value: An integer value stored in the instance.
    """

    def __init__(self, value: int = 0) -> None:
        """Initialize the ExampleClass.

        Args:
            value: Initial value for the instance. Defaults to 0.
        """
        self.value = value

    def increment(self, amount: int = 1) -> int:
        """Increment the value by the specified amount.

        Args:
            amount: The amount to increment by. Defaults to 1.

        Returns:
            The new value after incrementing.
        """
        self.value += amount
        return self.value

    def get_value(self) -> int:
        """Get the current value.

        Returns:
            The current value.
        """
        return self.value
