# stunning-memory

A Python project scaffold with a clean structure and best practices.

## Features

- Modern Python project structure with `src` layout
- Configuration using `pyproject.toml` (PEP 517/518)
- Testing setup with pytest
- Code formatting with black
- Linting with flake8
- Type checking with mypy
- Comprehensive `.gitignore` for Python projects

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/ohno-org/stunning-memory.git
cd stunning-memory

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Using pip

```bash
pip install -r requirements.txt
```

## Usage

```python
from stunning_memory import example_function, ExampleClass

# Use the example function
greeting = example_function("World")
print(greeting)  # Output: Hello, World!

# Use the example class
obj = ExampleClass(10)
obj.increment(5)
print(obj.get_value())  # Output: 15
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=stunning_memory --cov-report=term-missing

# Run specific test file
pytest tests/test_core.py
```

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Check formatting without making changes
black --check src/ tests/
```

### Linting

```bash
# Run flake8
flake8 src/ tests/
```

### Type Checking

```bash
# Run mypy
mypy src/
```

## Project Structure

```
stunning-memory/
├── src/
│   └── stunning_memory/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
└── setup.py
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.