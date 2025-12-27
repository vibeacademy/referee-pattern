Implement features/calculator.feature with focus on **security**: input validation, type safety, and secure defaults.

## Requirements

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see the expected interface
3. Create `src/__init__.py` and `src/calculator.py` with security-first design
4. Update `features/steps/calculator_steps.py` to import and use your Calculator
5. Run `uv run behave` to verify all 5 scenarios pass

## File Structure

```
src/
├── __init__.py
└── calculator.py

features/steps/
└── calculator_steps.py  (update this)
```

## Security Patterns to Apply

- **Strict input validation**: Check type, None, NaN, Infinity before any operation
- **`__slots__`**: Prevent attribute injection
- **Safe error messages**: No internal details leaked
- **Type checking**: `isinstance()` checks on all inputs
- **Bounds checking**: Check for overflow conditions
- **No implicit coercion**: Explicit type conversion only

Example validation:
```python
def _validate(self, value: any, name: str) -> float:
    if value is None:
        raise TypeError(f"{name} cannot be None")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if math.isnan(result) or math.isinf(result):
        raise ValueError(f"{name} must be finite")
    return result
```

## Verification

Before reporting done:
- [ ] `src/` directory exists with `__init__.py` and `calculator.py`
- [ ] All inputs validated before use
- [ ] `__slots__` used
- [ ] Error messages don't leak internals
- [ ] `features/steps/calculator_steps.py` imports from `src.calculator`
- [ ] `uv run behave` shows 5 scenarios passed
