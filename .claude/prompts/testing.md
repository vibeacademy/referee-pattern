# Testing Implementation Guide

Implement the feature with focus on **testability**: designed from the ground up to be easily testable, with comprehensive test coverage.

## Implementation Philosophy

Prioritize:
- **Testability first** - Design for easy testing
- **Dependency injection** - Mock-friendly interfaces
- **Pure functions** - Predictable, side-effect free
- **Clear interfaces** - Well-defined inputs and outputs
- **Test coverage** - Every path has a test

## Implementation Requirements

### File Structure

Create this structure:
```
src/
├── __init__.py          # Make src a package
└── calculator.py        # Your testable Calculator implementation

features/
└── steps/
    └── calculator_steps.py  # Update to import from src.calculator

tests/                   # Optional but recommended
├── __init__.py
└── test_calculator.py   # Unit tests for Calculator
```

### Steps

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see expected interface
3. Create `src/__init__.py` and `src/calculator.py`
4. Update `features/steps/calculator_steps.py` to import and use Calculator
5. Run `uv run behave` to verify all tests pass
6. Optionally create `tests/test_calculator.py` with pytest unit tests

## Testability Patterns to Apply

### 1. Dependency Injection
```python
from typing import Protocol, Dict

class OperationProvider(Protocol):
    """Protocol for operation providers - enables mocking."""

    def get_operation(self, name: str) -> callable:
        ...

class Calculator:
    def __init__(self, operations: OperationProvider = None):
        """Create calculator with injectable operations.

        Args:
            operations: Optional custom operation provider.
                       Defaults to built-in operations.
        """
        self._operations = operations or DefaultOperations()
```

### 2. Pure Functions Where Possible
```python
# Good: Pure function - easy to test
def add(a: float, b: float) -> float:
    """Pure addition - no side effects."""
    return a + b

# Test is simple:
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

### 3. Clear Interfaces
```python
class Calculator:
    """Calculator with well-defined interface for testing."""

    def add(self, a: float, b: float) -> float:
        """Add two numbers. Returns sum."""
        ...

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a. Returns difference."""
        ...
```

### 4. Isolated Side Effects
```python
class Calculator:
    def __init__(self, logger: Logger = None):
        """Logger is injectable for testing."""
        self._logger = logger or NullLogger()

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            self._logger.warning("Division by zero attempted")
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
```

### 5. Factory Methods for Test Fixtures
```python
class Calculator:
    @classmethod
    def create_for_testing(cls, mock_operations=None):
        """Factory method for creating test instances."""
        return cls(operations=mock_operations)
```

### 6. Optional Unit Tests
```python
# tests/test_calculator.py
import pytest
from src.calculator import Calculator

class TestCalculator:
    """Unit tests for Calculator class."""

    def setup_method(self):
        """Create fresh calculator for each test."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        assert self.calc.add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert self.calc.add(-2, -3) == -5

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (9, 3, 3.0),
        (7, 2, 3.5),
    ])
    def test_divide_various_inputs(self, a, b, expected):
        assert self.calc.divide(a, b) == expected
```

## Verification Checklist

Before reporting completion:
- [ ] `src/__init__.py` exists
- [ ] `src/calculator.py` exists with Calculator class
- [ ] `features/steps/calculator_steps.py` imports from src.calculator
- [ ] `uv run behave` shows all 5 scenarios passing
- [ ] Dependencies are injectable
- [ ] Clear interface for each public method
- [ ] Type hints throughout for clarity
- [ ] (Optional) `tests/test_calculator.py` with pytest tests
