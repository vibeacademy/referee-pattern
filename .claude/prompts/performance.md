# Performance Implementation Guide

Implement the feature with focus on **performance**: maximum efficiency, minimal overhead, and optimal resource usage.

## Implementation Philosophy

Prioritize:
- **Speed** - Minimize execution time
- **Memory efficiency** - Use `__slots__`, avoid unnecessary objects
- **Minimal abstraction overhead** - Direct operations over indirection
- **Algorithmic efficiency** - O(1) operations where possible
- **Zero-cost abstractions** - Only add structure that doesn't slow things down

## Implementation Requirements

### File Structure

Create this structure (lean, single-file preferred):
```
src/
├── __init__.py          # Make src a package
└── calculator.py        # Your optimized Calculator implementation

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

## Performance Patterns to Apply

### 1. Use `__slots__` for Memory Efficiency
```python
class Calculator:
    __slots__ = ['_result']

    def __init__(self):
        self._result: float = 0.0
```

### 2. Direct Method Calls (Avoid Indirection)
```python
# Good: Direct operation
def add(self, a: float, b: float) -> float:
    return a + b

# Avoid: Unnecessary indirection
def add(self, a: float, b: float) -> float:
    return self._operations['add'].execute(a, b)
```

### 3. Minimize Object Creation
- Reuse objects where possible
- Avoid creating exceptions for control flow
- Use primitive types when sufficient

### 4. Integer Operations When Possible
```python
# Use integer division when result should be integer
def integer_divide(self, a: int, b: int) -> int:
    return a // b
```

### 5. Early Returns and Short-Circuit Evaluation
```python
def divide(self, a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

### 6. Type Hints for Performance
- Type hints enable better optimization
- Use `float` over `Union[int, float]` when possible

### 7. Single File Design
- Minimize import overhead
- Keep everything in one module for fastest loading
- Inline small helper functions

## Verification Checklist

Before reporting completion:
- [ ] `src/__init__.py` exists
- [ ] `src/calculator.py` exists with Calculator class
- [ ] `features/steps/calculator_steps.py` imports from src.calculator
- [ ] `uv run behave` shows all 5 scenarios passing
- [ ] `__slots__` is used on Calculator class
- [ ] No unnecessary abstraction layers
- [ ] Direct method implementations (not dispatched through dict/strategy)
