# Security Implementation Guide

Implement the feature with focus on **security**: security-first design, best practices, and vulnerability prevention.

## Implementation Philosophy

Prioritize:
- **Input validation** - Never trust user input
- **Secure defaults** - Safe behavior out of the box
- **Principle of least privilege** - Minimal permissions
- **Defense in depth** - Multiple security layers
- **Fail securely** - Errors don't leak information

## Implementation Requirements

### File Structure

Create this structure:
```
src/
├── __init__.py          # Make src a package
└── calculator.py        # Your security-focused Calculator implementation

features/
└── steps/
    └── calculator_steps.py  # Update to import from src.calculator
```

### Steps

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see expected interface
3. Create `src/__init__.py` and `src/calculator.py`
4. Update `features/steps/calculator_steps.py` to import and use Calculator
5. Run `uv run behave` to verify all tests pass

## Security Patterns to Apply

### 1. Strict Input Validation
```python
import math

def _validate_operand(self, value: any, name: str) -> float:
    """Validate and sanitize numeric input.

    Args:
        value: The input value to validate.
        name: Parameter name for error messages.

    Returns:
        Validated float value.

    Raises:
        TypeError: If value is not numeric.
        ValueError: If value is NaN or infinite.
    """
    if value is None:
        raise TypeError(f"{name} cannot be None")

    if not isinstance(value, (int, float)):
        raise TypeError(
            f"{name} must be numeric, got {type(value).__name__}"
        )

    result = float(value)

    if math.isnan(result):
        raise ValueError(f"{name} cannot be NaN")
    if math.isinf(result):
        raise ValueError(f"{name} cannot be infinite")

    return result
```

### 2. Safe Error Handling
```python
# Don't leak internal details
def divide(self, a: float, b: float) -> float:
    a = self._validate_operand(a, "dividend")
    b = self._validate_operand(b, "divisor")

    if b == 0:
        # Safe error message - no internal details
        raise ZeroDivisionError("Division by zero is not allowed")

    return a / b
```

### 3. Type Safety
```python
from typing import Union

Numeric = Union[int, float]

def add(self, a: Numeric, b: Numeric) -> float:
    """Type-safe addition with validation."""
    validated_a = self._validate_operand(a, "first_operand")
    validated_b = self._validate_operand(b, "second_operand")
    return validated_a + validated_b
```

### 4. Immutable Where Possible
```python
class Calculator:
    """Calculator with immutable operation results."""

    __slots__ = ['_last_result']  # Prevent attribute injection

    def __init__(self):
        self._last_result: float = 0.0

    @property
    def last_result(self) -> float:
        """Read-only access to last result."""
        return self._last_result
```

### 5. Bounds Checking
```python
import sys

MAX_VALUE = sys.float_info.max
MIN_VALUE = -sys.float_info.max

def _check_overflow(self, result: float) -> float:
    """Check for numeric overflow."""
    if result > MAX_VALUE or result < MIN_VALUE:
        raise OverflowError("Result exceeds safe numeric bounds")
    return result
```

### 6. Secure Defaults
- Operations validate all inputs by default
- No implicit type coercion
- Explicit error handling

## Verification Checklist

Before reporting completion:
- [ ] `src/__init__.py` exists
- [ ] `src/calculator.py` exists with Calculator class
- [ ] `features/steps/calculator_steps.py` imports from src.calculator
- [ ] `uv run behave` shows all 5 scenarios passing
- [ ] All inputs are validated before use
- [ ] Error messages don't leak internal details
- [ ] Type checking is implemented
- [ ] `__slots__` prevents attribute injection
