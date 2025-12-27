# Robustness Implementation Guide

Implement the feature with focus on **robustness**: exceptional reliability, comprehensive error handling, edge case coverage, and resilience.

## Implementation Philosophy

Prioritize:
- **Bulletproof error handling** - Nothing fails silently
- **Defensive programming** - Assume inputs can be malformed
- **Edge case coverage** - Handle nulls, boundaries, and unexpected states
- **Graceful degradation** - Fail safely with clear error messages
- **Resource safety** - Always clean up, never leak

## Implementation Requirements

### File Structure

Create this structure:
```
src/
├── __init__.py          # Make src a package
└── calculator.py        # Your Calculator implementation

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

## Robustness Patterns to Apply

### 1. Custom Exception Hierarchy
```python
class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass

class InvalidOperandError(CalculatorError):
    """Raised when operands are invalid."""
    pass
```

### 2. Input Validation
- Validate all inputs before operations
- Check types (must be numeric)
- Check for None/null values
- Validate ranges if applicable

### 3. Comprehensive Error Handling
- Wrap operations in try-except
- Provide clear, actionable error messages
- Log errors for debugging
- Never expose internal details in user-facing errors

### 4. Defensive Programming
- Use assertions for programmer errors
- Use exceptions for runtime errors
- Fail fast on invalid states
- Document preconditions and postconditions

### 5. Edge Cases to Handle
- Division by zero (required by feature spec)
- Very large numbers (overflow)
- Very small numbers (underflow)
- Floating point precision issues
- None/null inputs

## Verification Checklist

Before reporting completion:
- [ ] `src/__init__.py` exists
- [ ] `src/calculator.py` exists with Calculator class
- [ ] `features/steps/calculator_steps.py` imports from src.calculator
- [ ] `uv run behave` shows all 5 scenarios passing
- [ ] Custom exception for division by zero is implemented
- [ ] Input validation is present
