# Readability Implementation Guide

Implement the feature with focus on **readability**: crystal-clear code that any developer can understand at first glance.

## Implementation Philosophy

Prioritize:
- **Self-documenting code** - Names tell the story
- **Clear intent** - Why, not just what
- **Minimal cognitive load** - Easy to understand
- **Consistent style** - Predictable patterns
- **Progressive disclosure** - Simple surface, details underneath

## Implementation Requirements

### File Structure

Create this structure:
```
src/
├── __init__.py          # Make src a package
└── calculator.py        # Your readable Calculator implementation

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

## Readability Patterns to Apply

### 1. Descriptive Naming
```python
# Good: Clear, descriptive names
def divide_numbers(self, dividend: float, divisor: float) -> float:
    """Divide dividend by divisor, returning the quotient."""
    ...

# Avoid: Cryptic abbreviations
def div(self, a: float, b: float) -> float:
    ...
```

### 2. Comprehensive Docstrings
```python
class Calculator:
    """A simple calculator for basic arithmetic operations.

    This calculator supports addition, subtraction, multiplication,
    and division operations. Division by zero raises a descriptive
    error.

    Example:
        calc = Calculator()
        result = calc.add(5, 3)  # Returns 8
    """
```

### 3. Method Documentation
```python
def add(self, first_number: float, second_number: float) -> float:
    """Add two numbers together.

    Args:
        first_number: The first operand.
        second_number: The second operand.

    Returns:
        The sum of the two numbers.

    Example:
        >>> calc.add(5, 3)
        8
    """
    return first_number + second_number
```

### 4. Logical Code Organization
- Group related methods together
- Order methods by frequency of use or logical flow
- Separate public API from implementation details

### 5. Meaningful Error Messages
```python
if divisor == 0:
    raise ZeroDivisionError(
        f"Cannot divide {dividend} by zero. "
        "Please provide a non-zero divisor."
    )
```

### 6. Type Hints as Documentation
```python
def multiply(self, factor_a: float, factor_b: float) -> float:
```

### 7. Consistent Formatting
- Follow PEP 8 conventions
- Consistent spacing and indentation
- Reasonable line lengths (88-100 chars)

## Verification Checklist

Before reporting completion:
- [ ] `src/__init__.py` exists
- [ ] `src/calculator.py` exists with Calculator class
- [ ] `features/steps/calculator_steps.py` imports from src.calculator
- [ ] `uv run behave` shows all 5 scenarios passing
- [ ] All public methods have docstrings
- [ ] Class has comprehensive docstring with examples
- [ ] Variable/method names are descriptive
- [ ] Type hints are present throughout
