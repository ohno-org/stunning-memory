"""Tests for the core module."""

from stunning_memory.core import example_function, ExampleClass


class TestExampleFunction:
    """Test cases for example_function."""

    def test_default_greeting(self) -> None:
        """Test the default greeting."""
        result = example_function()
        assert result == "Hello, World!"

    def test_custom_greeting(self) -> None:
        """Test greeting with a custom name."""
        result = example_function("Python")
        assert result == "Hello, Python!"

    def test_empty_string(self) -> None:
        """Test greeting with an empty string."""
        result = example_function("")
        assert result == "Hello, !"


class TestExampleClass:
    """Test cases for ExampleClass."""

    def test_initialization_default(self) -> None:
        """Test default initialization."""
        obj = ExampleClass()
        assert obj.get_value() == 0

    def test_initialization_with_value(self) -> None:
        """Test initialization with a custom value."""
        obj = ExampleClass(42)
        assert obj.get_value() == 42

    def test_increment_default(self) -> None:
        """Test increment with default amount."""
        obj = ExampleClass(10)
        result = obj.increment()
        assert result == 11
        assert obj.get_value() == 11

    def test_increment_custom_amount(self) -> None:
        """Test increment with custom amount."""
        obj = ExampleClass(10)
        result = obj.increment(5)
        assert result == 15
        assert obj.get_value() == 15

    def test_multiple_increments(self) -> None:
        """Test multiple increment operations."""
        obj = ExampleClass(0)
        obj.increment(1)
        obj.increment(2)
        obj.increment(3)
        assert obj.get_value() == 6
